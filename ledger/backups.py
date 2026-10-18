"""Copias de datos tipadas: no contienen usuarios, contraseñas ni sesiones."""
import hashlib
import json
import uuid
from pathlib import Path
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.utils import timezone
from .models import Account, Activity, AuditEvent, Category, Entry, Salary, SalaryReceipt
from .services import ENTRY_FIELDS
from .salary_services import SALARY_FIELDS

LIMIT = 5 * 1024 * 1024
TABLES = {
    "activities": (Activity, ("name",)),
    "accounts": (Account, ("name", "kind")),
    "categories": (Category, ("name", "kind", "group")),
    "entries": (Entry, ENTRY_FIELDS),
    "salaries": (Salary, SALARY_FIELDS),
    "salary_receipts": (SalaryReceipt, ("salary_id","entry_id")),
    "events": (AuditEvent, ("at", "action", "entity", "before", "after", "reason")),
}


def canonical(value):
    return json.dumps(value, cls=DjangoJSONEncoder, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


@transaction.atomic
def export_backup(user):
    objects = {}
    for key, (model, fields) in TABLES.items():
        objects[key] = [{"id": str(item.pk), "fields": {field: getattr(item, field) for field in fields}}
                        for item in model.objects.filter(owner=user)]
    payload = {"application": "Finanzas DAGD", "format": 3, "created": timezone.now().isoformat(), "software_version": settings.APP_VERSION, "objects": objects}
    payload["sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
    raw = canonical(payload)
    if len(raw) > LIMIT or sum(len(rows) for rows in objects.values()) > 10000:
        raise ValidationError("Esta copia supera el límite del respaldo básico (5 MiB o 10.000 registros).")
    return raw


def write_backup(user):
    raw = export_backup(user)
    folder = Path(settings.BACKUP_DIR) / f"usuario-{user.pk}"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"finanzas-{timezone.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:8]}.json"
    with path.open("xb") as stream:
        stream.write(raw)
    return path, raw


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Clave repetida en la copia")
        result[key] = value
    return result


def validate_backup(raw):
    try:
        if len(raw) > LIMIT:
            raise ValueError("Tamaño excedido")
        payload = json.loads(raw, object_pairs_hook=unique_keys)
        if set(payload) != {"application", "format", "created", "software_version", "objects", "sha256"}:
            raise ValueError("Formato desconocido")
        digest = payload.pop("sha256")
        if payload["application"] != "Finanzas DAGD" or type(payload["format"]) is not int or payload["format"] not in (1,2,3):
            raise ValueError("Aplicación o versión de formato incompatible")
        if not isinstance(digest, str) or hashlib.sha256(canonical(payload)).hexdigest() != digest:
            raise ValueError("La huella no coincide")
        objects = payload["objects"]
        allowed=set(TABLES) if payload["format"]>=2 else set(TABLES)-{"salaries","salary_receipts"}
        if not isinstance(objects, dict) or set(objects) != allowed:
            raise ValueError("Tablas inesperadas")
        if payload["format"]==1:
            objects={**objects,"salaries":[],"salary_receipts":[]}
        for key, (_, fields) in TABLES.items():
            rows = objects[key]
            if not isinstance(rows, list):
                raise ValueError("Lista inválida")
            ids = set()
            for row in rows:
                expected_fields = set(fields) - ({"group"} if key == "categories" and payload["format"] < 3 else set())
                if set(row) != {"id", "fields"} or set(row["fields"]) != expected_fields:
                    raise ValueError("Campos inesperados")
                if key == "categories" and payload["format"] < 3:
                    row["fields"]["group"] = ""
                identifier = uuid.UUID(row["id"])
                if identifier in ids:
                    raise ValueError("Identificadores repetidos")
                ids.add(identifier)
                if key == "entries":
                    values = row["fields"]
                    if type(values["cents"]) is not int or type(values["revision"]) is not int or values["revision"] < 1 or type(values["void"]) is not bool:
                        raise ValueError("Importe, versión o estado inválido")
                if key == "salaries":
                    values=row["fields"]
                    if any(type(values[field]) is not int for field in ("net_cents","additions_cents","deductions_cents","revision")) or (values["gross_cents"] is not None and type(values["gross_cents"]) is not int) or type(values["active"]) is not bool:
                        raise ValueError("Importes o estado de sueldo inválidos")
                if key == "events" and (not isinstance(row["fields"]["before"], dict) or not isinstance(row["fields"]["after"], dict)):
                    raise ValueError("Antecedentes inválidos")
        if sum(len(rows) for rows in objects.values()) > 10000:
            raise ValueError("Demasiados registros")
        return objects
    except (ValueError, TypeError, KeyError, AttributeError, OverflowError, RecursionError) as error:
        raise ValidationError("La copia está dañada o su formato no es compatible. No se restauró ningún dato.") from error


def restore_backup(user, raw):
    objects = validate_backup(raw)
    with transaction.atomic():
        previous, _ = write_backup(user)
        SalaryReceipt.objects.filter(owner=user).delete()
        Salary.objects.filter(owner=user).delete()
        Entry.objects.filter(owner=user).delete()
        Category.objects.filter(owner=user).delete()
        Account.objects.filter(owner=user).delete()
        Activity.objects.filter(owner=user).delete()
        for key, (model, _) in TABLES.items():
            for row in objects[key]:
                if key == "events" and AuditEvent.objects.filter(pk=row["id"], owner=user).exists():
                    continue
                item = model(pk=row["id"], owner=user, **row["fields"])
                item.full_clean()
                item.save(force_insert=True)
                if key == "events":
                    AuditEvent.objects.filter(pk=item.pk).update(at=item.at if not row["fields"].get("at") else row["fields"]["at"])
        AuditEvent.objects.create(owner=user, action="restauración", after={"registros": {key: len(rows) for key, rows in objects.items()}}, reason="Restauración de una copia propia; se conserva respaldo previo.")
    return previous
