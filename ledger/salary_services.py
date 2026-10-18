from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Prefetch
from .models import AuditEvent, Entry, SalaryReceipt

SALARY_FIELDS=("title","activity_id","mode","earned_month","budget_month","expected_date","net_cents","gross_cents","additions_cents","deductions_cents","active","revision")


def salary_state(salary):
    return {field:str(getattr(salary,field)) for field in SALARY_FIELDS}


@transaction.atomic
def save_salary(salary,user,expected_revision=None,reason=""):
    salary.owner=user
    before={}
    if expected_revision is not None:
        old=type(salary).objects.get(pk=salary.pk,owner=user)
        if old.revision!=expected_revision or not reason.strip():
            raise ValidationError("Recarga el sueldo e indica un motivo para corregirlo; otra ventana pudo cambiarlo.")
        before=salary_state(old)
        salary.revision=old.revision+1
    salary.full_clean()
    if expected_revision is None: salary.save(force_insert=True)
    elif type(salary).objects.filter(pk=salary.pk,owner=user,revision=expected_revision).update(**{field:getattr(salary,field) for field in SALARY_FIELDS})!=1:
        raise ValidationError("El sueldo cambió. Recarga antes de guardar.")
    AuditEvent.objects.create(owner=user,action="sueldo",entity=str(salary.pk),before=before,after=salary_state(salary),reason=reason)
    return salary


@transaction.atomic
def link_receipt(salary,entry,user):
    # Releer el movimiento: no confiar en valores de una pantalla antigua.
    if salary.owner_id!=user.pk or entry.owner_id!=user.pk: raise ValidationError("Vincula únicamente registros propios.")
    salary=type(salary).objects.get(pk=salary.pk,owner=user)
    entry=Entry.objects.get(pk=entry.pk,owner=user)
    if entry.void: raise ValidationError("No puedes vincular un ingreso anulado.")
    receipt=SalaryReceipt(owner=user,salary=salary,entry=entry)
    receipt.full_clean()
    receipt.save(force_insert=True)
    AuditEvent.objects.create(owner=user,action="cobro de sueldo",entity=str(salary.pk),after={"vínculo":str(receipt.pk),"movimiento":str(entry.pk),"centavos":entry.cents})
    return receipt


@transaction.atomic
def unlink_receipt(receipt,user,reason):
    if receipt.owner_id!=user.pk or not reason.strip(): raise ValidationError("Indica un motivo válido para desvincular un cobro propio.")
    state={"sueldo":str(receipt.salary_id),"movimiento":str(receipt.entry_id)}
    receipt.delete()
    AuditEvent.objects.create(owner=user,action="desvincular cobro",before=state,reason=reason)


def salary_totals(user,month,activity=None):
    from .models import Salary
    salaries=Salary.objects.filter(owner=user,budget_month=month).select_related("activity").prefetch_related(Prefetch("receipts",queryset=SalaryReceipt.objects.select_related("entry__account")))
    if activity: salaries=salaries.filter(activity=activity)
    rows=[]
    for salary in salaries:
        receipts=list(salary.receipts.all())
        received=sum(receipt.entry.cents for receipt in receipts if not receipt.entry.void)
        rows.append({"salary":salary,"receipts":receipts,"received":received,"pending":max(salary.net_cents-received,0) if salary.active else 0,"excess":max(received-salary.net_cents,0)})
    return {"rows":rows,"planned":sum(row["salary"].net_cents for row in rows if row["salary"].active),"received":sum(row["received"] for row in rows),"pending":sum(row["pending"] for row in rows)}
