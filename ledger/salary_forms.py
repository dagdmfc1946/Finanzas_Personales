from .templatetags.ledger_money import pesos
from decimal import Decimal
from django import forms
from django.utils import timezone
from .models import Activity, Entry, Salary


class MonthField(forms.DateField):
    def __init__(self,**kwargs):
        super().__init__(input_formats=["%Y-%m"],widget=forms.DateInput(format="%Y-%m",attrs={"type":"month"}),**kwargs)


def money(label,required=False):
    return forms.DecimalField(label=label,required=required,max_digits=14,decimal_places=2,min_value=Decimal("0"),help_text="COP, sin separadores de miles; máximo dos decimales.")


class SalaryForm(forms.Form):
    title=forms.CharField(label="Concepto",max_length=120)
    activity=forms.ModelChoiceField(label="Actividad",queryset=Activity.objects.none())
    mode=forms.ChoiceField(label="Modalidad",choices=Salary._meta.get_field("mode").choices)
    earned_month=MonthField(label="Mes trabajado")
    expected_date=forms.DateField(label="Fecha prevista de cobro",widget=forms.DateInput(format="%Y-%m-%d",attrs={"type":"date"}))
    budget_month=MonthField(label="Mes presupuestado")
    net_amount=money("Sueldo neto (solo modalidad Neto)")
    gross_amount=money("Bruto (solo modalidad Bruto y deducciones)")
    additions_amount=money("Adicionales, opcional")
    deductions_amount=money("Deducciones, opcional")
    active=forms.BooleanField(label="Incluir este sueldo en la previsión",required=False,initial=True)
    reason=forms.CharField(label="Motivo de corrección",max_length=240,required=False)
    version=forms.IntegerField(widget=forms.HiddenInput,min_value=0,initial=0)
    submission=forms.UUIDField(widget=forms.HiddenInput)

    def __init__(self,*args,user,instance=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.instance=instance or Salary(owner=user)
        self.fields["activity"].queryset=Activity.objects.filter(owner=user)
        today=timezone.localdate()
        self.initial.update(submission=self.instance.pk,earned_month=today.replace(day=1),budget_month=today.replace(day=1),expected_date=today,mode="neto",version=0)
        if not self.instance._state.adding:
            item=self.instance
            self.initial.update({name:getattr(item,name) for name in ("title","activity","mode","earned_month","budget_month","expected_date","active","revision")})
            self.initial["activity"]=item.activity_id
            self.initial["version"]=item.revision
            for field,value in (("net_amount",item.net_cents if item.mode=="neto" else None),("gross_amount",item.gross_cents),("additions_amount",item.additions_cents),("deductions_amount",item.deductions_cents)):
                self.initial[field]=Decimal(value)/100 if value is not None else None
            self.fields["reason"].required=True
        else: del self.fields["reason"]

    def clean(self):
        cleaned=super().clean()
        if self.errors: return cleaned
        def cents(name): return int((cleaned.get(name) or 0)*100)
        gross=cents("gross_amount") if cleaned.get("gross_amount") is not None else None
        extra,deductions=cents("additions_amount"),cents("deductions_amount")
        if cleaned["mode"]=="detalle":
            if gross is None: raise forms.ValidationError("Introduce el bruto para calcular el neto.")
            if cleaned.get("net_amount") is not None: raise forms.ValidationError("En detalle deja el campo neto vacío; se calcula a partir del bruto.")
            net=gross+extra-deductions
        else:
            if cleaned.get("net_amount") is None: raise forms.ValidationError("Introduce el sueldo neto.")
            if gross is not None or extra or deductions: raise forms.ValidationError("Para sueldo neto deja el bruto vacío y los ajustes en cero.")
            net=cents("net_amount")
        if not 0<net<=99999999999999: raise forms.ValidationError("El neto debe ser positivo y no superar 999999999999.99 COP.")
        if self.instance._state.adding: self.instance.id=cleaned["submission"]
        elif self.instance.pk!=cleaned["submission"]: raise forms.ValidationError("El formulario no corresponde a este sueldo.")
        for name in ("title","activity","mode","earned_month","budget_month","expected_date","active"): setattr(self.instance,name,cleaned[name])
        self.instance.net_cents,self.instance.gross_cents,self.instance.additions_cents,self.instance.deductions_cents=net,gross,extra,deductions
        return cleaned


class SalaryFilter(forms.Form):
    month=MonthField(label="Mes presupuestado")
    activity=forms.ModelChoiceField(label="Actividad",queryset=Activity.objects.none(),required=False,empty_label="Todas las actividades")
    def __init__(self,*args,user,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["activity"].queryset=Activity.objects.filter(owner=user)


class ReceiptForm(forms.Form):
    entry=forms.ModelChoiceField(label="Ingreso ya registrado",queryset=Entry.objects.none(),help_text="Solo ingresos vigentes de esta actividad que aún no están vinculados a un sueldo.")
    def __init__(self,*args,user,salary,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["entry"].queryset=Entry.objects.filter(owner=user,kind="ingreso",void=False,activity=salary.activity,salary_receipt__isnull=True)
        self.fields["entry"].label_from_instance=lambda entry:f"{entry.date:%d/%m/%Y} · {entry.description} · {pesos(entry.cents)}"
