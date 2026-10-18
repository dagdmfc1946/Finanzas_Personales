from collections import defaultdict
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Account, AuditEvent, Entry

ENTRY_FIELDS = ("date", "description", "kind", "cents", "activity_id", "account_id", "category_id", "destination_activity_id", "destination_account_id", "void", "revision")


def entry_state(entry):
    return {key: str(value) if key.endswith("_id") or key == "date" else value
            for key in ENTRY_FIELDS if (value := getattr(entry, key)) is not None}


@transaction.atomic
def save_entry(entry, user, expected_revision=None, reason=""):
    entry.owner = user
    before = {}
    if expected_revision is not None:
        old = Entry.objects.get(pk=entry.pk, owner=user)
        if old.void:
            raise ValidationError("Un movimiento anulado no se puede corregir.")
        if old.revision != expected_revision:
            raise ValidationError("Este movimiento cambió en otra ventana. Recarga antes de corregirlo.")
        if not reason.strip():
            raise ValidationError("Indica el motivo de la corrección.")
        before = entry_state(old)
        entry.revision = old.revision + 1
    entry.full_clean()
    if expected_revision is None:
        entry.save(force_insert=True)
    else:
        updated = Entry.objects.filter(pk=entry.pk, owner=user, revision=expected_revision).update(
            **{field: getattr(entry, field) for field in ENTRY_FIELDS})
        if updated != 1:
            raise ValidationError("La edición ya no es vigente. Recarga el movimiento.")
    AuditEvent.objects.create(owner=user, action="corrección" if before else "registro", entity=str(entry.pk), before=before, after=entry_state(entry), reason=reason)
    return entry


@transaction.atomic
def void_entry(entry, user, expected_revision, reason):
    if not reason.strip():
        raise ValidationError("Indica el motivo de la anulación.")
    current = Entry.objects.get(pk=entry.pk, owner=user)
    if current.void or current.revision != expected_revision:
        raise ValidationError("El movimiento cambió o ya estaba anulado. Recarga la página.")
    before = entry_state(current)
    changed = Entry.objects.filter(pk=current.pk, owner=user, revision=expected_revision, void=False).update(void=True, revision=expected_revision + 1)
    if changed != 1:
        raise ValidationError("El movimiento cambió. Recarga la página.")
    current.refresh_from_db()
    AuditEvent.objects.create(owner=user, action="anulación", entity=str(current.pk), before=before, after=entry_state(current), reason=reason)


def summary(user, activity=None):
    accounts = list(Account.objects.filter(owner=user))
    balances = defaultdict(int)
    income = expenses = opening = transfers_in = transfers_out = 0
    for entry in Entry.objects.filter(owner=user, void=False).iterator():
        source = activity is None or entry.activity_id == activity.pk
        destination = activity is None or entry.destination_activity_id == activity.pk
        if source:
            if entry.kind in ("ingreso", "inicial"):
                balances[entry.account_id] += entry.cents
                if entry.kind == "ingreso":
                    income += entry.cents
                else:
                    opening += entry.cents
            elif entry.kind == "gasto":
                balances[entry.account_id] -= entry.cents
                expenses += entry.cents
            else:
                balances[entry.account_id] -= entry.cents
                transfers_out += entry.cents
        if entry.kind == "transferencia" and destination:
            balances[entry.destination_account_id] += entry.cents
            transfers_in += entry.cents
    return {"accounts": [{"account": account, "balance": balances[account.pk]} for account in accounts],
            "income": income, "expenses": expenses, "opening": opening,
            "balance": sum(balances.values()), "transfers_in": transfers_in, "transfers_out": transfers_out}
