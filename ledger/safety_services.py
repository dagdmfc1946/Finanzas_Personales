from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.deletion import ProtectedError
from .backups import write_backup
from .models import Activity, Account, Category, Entry, Salary, SalaryReceipt, AuditEvent
from .services import entry_state
from .salary_services import salary_state

DELETABLE = {"actividad": Activity, "cuenta": Account, "categoria": Category, "movimiento": Entry, "sueldo": Salary}


@transaction.atomic
def remove_record(user, kind, pk, version, reason):
    item = DELETABLE[kind].objects.select_for_update().filter(pk=pk, owner=user).first()
    if item is None:
        raise ValidationError("El registro ya no existe en tu espacio. Recarga la página.")
    if not reason.strip():
        raise ValidationError("Escribe un motivo.")
    if hasattr(item, "revision") and item.revision != version:
        raise ValidationError("El registro cambió. Recarga antes de eliminarlo.")
    previous, _ = write_backup(user)
    identifier = str(item.pk)
    if kind == "movimiento":
        before = entry_state(item)
        SalaryReceipt.objects.filter(owner=user, entry=item).delete()
    elif kind == "sueldo":
        before = salary_state(item)
        SalaryReceipt.objects.filter(owner=user, salary=item).delete()
    else:
        before = {"nombre": item.name, "tipo": kind}
    try:
        item.delete()
    except ProtectedError as error:
        raise ValidationError("Este elemento tiene registros asociados. Corrige o elimina primero sus movimientos o planes; no se eliminó ningún dato.") from error
    AuditEvent.objects.create(owner=user, action="eliminación", entity=identifier, before=before, after={"tipo": kind}, reason=reason)
    return previous


@transaction.atomic
def reset_finances(user, reason):
    if not reason.strip():
        raise ValidationError("Escribe el motivo del reinicio.")
    previous, _ = write_backup(user)
    for model in (SalaryReceipt, Salary, Entry, Category, Account, Activity, AuditEvent):
        model.objects.filter(owner=user).delete()
    Activity.objects.create(owner=user, name="Personal / trabajo principal")
    AuditEvent.objects.create(owner=user, action="reinicio personal", reason=reason, after={"estado": "Finanzas vacías; acceso y perfil conservados"})
    return previous


@transaction.atomic
def remove_user(actor, pk, reason):
    from django.contrib.auth import get_user_model
    from .models import Installation
    if not actor.is_staff or not reason.strip():
        raise ValidationError("Solo el administrador puede eliminar usuarios, con un motivo.")
    person = get_user_model().objects.select_for_update().filter(pk=pk).first()
    if person is None:
        raise ValidationError("El usuario ya no existe. Recarga la lista.")
    if person.pk == actor.pk or person.is_staff or person.is_superuser or Installation.objects.filter(user=person).exists():
        raise ValidationError("El administrador inicial y las cuentas administrativas están protegidos contra eliminación.")
    previous, _ = write_backup(person)
    username = person.username
    for model in (SalaryReceipt, Salary, Entry, Category, Account, Activity, AuditEvent):
        model.objects.filter(owner=person).delete()
    person.delete()
    AuditEvent.objects.create(owner=actor, action="eliminar usuario", entity=str(pk), before={"usuario": username}, reason=reason)
    return previous
