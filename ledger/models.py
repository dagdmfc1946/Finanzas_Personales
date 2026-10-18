import uuid
from datetime import date
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q


class Installation(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class Owned(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Activity(Owned):
    name = models.CharField("Nombre", max_length=80)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["owner", "name"], name="actividad_unica")]

    def __str__(self):
        return self.name


class Account(Owned):
    name = models.CharField("Nombre", max_length=80)
    kind = models.CharField("Tipo", max_length=12, choices=[("banco", "Banco"), ("billetera", "Billetera"), ("efectivo", "Efectivo"), ("ahorro", "Ahorros")])

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["owner", "name"], name="cuenta_unica")]

    def __str__(self):
        return self.name


class Category(Owned):
    name = models.CharField("Nombre", max_length=80)
    kind = models.CharField("Tipo", max_length=10, choices=[("ingreso", "Ingreso"), ("gasto", "Gasto")])

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["owner", "name", "kind"], name="categoria_unica")]

    def __str__(self):
        return f"{self.name} · {self.get_kind_display()}"


class Entry(Owned):
    KINDS = [("ingreso", "Ingreso"), ("gasto", "Gasto"), ("inicial", "Saldo inicial"), ("transferencia", "Transferencia")]
    date = models.DateField("Fecha")
    description = models.CharField("Concepto", max_length=160)
    kind = models.CharField("Tipo", max_length=14, choices=KINDS)
    cents = models.BigIntegerField()
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT, related_name="outgoing")
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="outgoing")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.PROTECT)
    destination_activity = models.ForeignKey(Activity, null=True, blank=True, on_delete=models.PROTECT, related_name="incoming")
    destination_account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.PROTECT, related_name="incoming")
    void = models.BooleanField(default=False)
    revision = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-date", "-id"]
        constraints = [models.CheckConstraint(condition=Q(cents__gt=0) & Q(cents__lte=99999999999999), name="importe_valido")]

    def clean(self):
        super().clean()
        related_values = {}
        for field in ("activity", "account", "category", "destination_activity", "destination_account"):
            try:
                related = getattr(self, field, None)
            except ObjectDoesNotExist:
                # full_clean ya informa la referencia ausente; no convertirla en 500.
                continue
            related_values[field] = related
            if related and related.owner_id != self.owner_id:
                raise ValidationError("Selecciona elementos de tu propio espacio.")
        receipt = SalaryReceipt.objects.filter(entry_id=self.pk).select_related("salary").first() if not self._state.adding else None
        if receipt and (self.kind != "ingreso" or self.activity_id != receipt.salary.activity_id):
            raise ValidationError("Desvincula primero este cobro de su sueldo para cambiar su tipo o actividad.")
        if self.kind == "transferencia":
            if not self.destination_account_id or not self.destination_activity_id:
                raise ValidationError("Indica cuenta y actividad de destino para la transferencia.")
            if (self.account_id, self.activity_id) == (self.destination_account_id, self.destination_activity_id):
                raise ValidationError("El origen y el destino deben ser diferentes.")
        elif self.destination_account_id or self.destination_activity_id:
            raise ValidationError("Solo las transferencias tienen destino.")
        if related_values.get("category") and related_values["category"].kind != self.kind:
            raise ValidationError("La categoría debe corresponder al tipo de ingreso o gasto.")


class AuditEvent(Owned):
    at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=30)
    entity = models.CharField(max_length=36, blank=True)
    before = models.JSONField(default=dict, blank=True)
    after = models.JSONField(default=dict, blank=True)
    reason = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ["-at", "-id"]


MONEY_LIMIT=99999999999999
MONEY_VALIDATORS=[MinValueValidator(0),MaxValueValidator(MONEY_LIMIT)]


class Salary(Owned):
    title=models.CharField("Concepto",max_length=120)
    activity=models.ForeignKey(Activity,on_delete=models.PROTECT)
    mode=models.CharField("Modalidad",max_length=10,choices=[("neto","Neto"),("detalle","Bruto y deducciones")],default="neto")
    earned_month=models.DateField("Mes trabajado")
    budget_month=models.DateField("Mes presupuestado")
    expected_date=models.DateField("Fecha prevista de cobro")
    net_cents=models.BigIntegerField(validators=[MinValueValidator(1),MaxValueValidator(MONEY_LIMIT)])
    gross_cents=models.BigIntegerField(null=True,blank=True,validators=MONEY_VALIDATORS)
    additions_cents=models.BigIntegerField(default=0,validators=MONEY_VALIDATORS)
    deductions_cents=models.BigIntegerField(default=0,validators=MONEY_VALIDATORS)
    active=models.BooleanField(default=True)
    revision=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])

    class Meta:
        ordering=["-budget_month","expected_date","title","id"]
        constraints=[models.CheckConstraint(condition=Q(net_cents__gt=0)&Q(net_cents__lte=MONEY_LIMIT),name="sueldo_neto_valido")]

    def clean(self):
        super().clean()
        try: activity=self.activity
        except ObjectDoesNotExist: activity=None
        if activity and activity.owner_id!=self.owner_id: raise ValidationError("Selecciona una actividad propia.")
        for field in ("earned_month","budget_month"):
            value=getattr(self,field)
            if isinstance(value,date) and value.day!=1: raise ValidationError("El mes debe representarse por su primer día.")
        if self.mode=="detalle":
            if self.gross_cents is None or not all(isinstance(value,int) for value in (self.net_cents,self.gross_cents,self.additions_cents,self.deductions_cents)) or self.net_cents!=self.gross_cents+self.additions_cents-self.deductions_cents:
                raise ValidationError("El neto debe ser bruto + adicionales − deducciones.")
        elif self.gross_cents is not None or self.additions_cents or self.deductions_cents:
            raise ValidationError("En modalidad neta deja el bruto vacío y los ajustes en cero.")
        if not self._state.adding and self.receipts.exclude(entry__activity_id=self.activity_id).exists():
            raise ValidationError("Desvincula los cobros antes de cambiar la actividad del sueldo.")

    def __str__(self): return self.title


class SalaryReceipt(Owned):
    salary=models.ForeignKey(Salary,on_delete=models.PROTECT,related_name="receipts")
    entry=models.OneToOneField(Entry,on_delete=models.PROTECT,related_name="salary_receipt")

    def clean(self):
        super().clean()
        related={}
        for field in ("salary","entry"):
            try: related[field]=getattr(self,field)
            except ObjectDoesNotExist: continue
            if related[field].owner_id!=self.owner_id: raise ValidationError("Solo puedes vincular registros propios.")
        if "salary" in related and "entry" in related:
            if self.entry.kind!="ingreso" or self.entry.activity_id!=self.salary.activity_id:
                raise ValidationError("Vincula un ingreso de la misma actividad del sueldo.")
