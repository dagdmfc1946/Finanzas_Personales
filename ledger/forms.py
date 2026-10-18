from decimal import Decimal
from django import forms
from django.utils import timezone
from .models import Activity, Account, Category, Entry


class OwnedForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.owner = user


class ActivityForm(OwnedForm):
    class Meta:
        model = Activity
        fields = ["name"]


class AccountForm(OwnedForm):
    initial_amount = forms.DecimalField(label="Saldo inicial COP (opcional)", max_digits=14, decimal_places=2, min_value=0, required=False)
    initial_activity = forms.ModelChoiceField(label="Actividad del saldo inicial", queryset=Activity.objects.none(), required=False)

    class Meta:
        model = Account
        fields = ["name", "kind"]

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, user=user, **kwargs)
        self.fields["initial_activity"].queryset = Activity.objects.filter(owner=user)
        if not self.instance._state.adding:
            del self.fields["initial_amount"]
            del self.fields["initial_activity"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("initial_amount") and not cleaned.get("initial_activity"):
            self.add_error("initial_activity", "Selecciona la actividad a la que pertenece ese saldo.")
        return cleaned


class CategoryForm(OwnedForm):
    class Meta:
        model = Category
        fields = ["name", "kind"]

    def clean(self):
        cleaned = super().clean()
        if not self.instance._state.adding and Entry.objects.filter(category=self.instance).exclude(kind=cleaned.get("kind")).exists():
            self.add_error("kind", "Esta categoría ya tiene movimientos de otro tipo. Crea una categoría nueva para ese uso.")
        return cleaned


class EntryForm(OwnedForm):
    amount = forms.DecimalField(label="Importe COP", max_digits=14, decimal_places=2, min_value=Decimal("0.01"), help_text="Sin separadores de miles; hasta dos decimales. Ejemplo: 25000.50.")
    version = forms.IntegerField(widget=forms.HiddenInput, min_value=0, initial=0)
    submission = forms.UUIDField(widget=forms.HiddenInput)
    reason = forms.CharField(label="Motivo de corrección", max_length=240, required=False)

    class Meta:
        model = Entry
        fields = ["kind", "date", "description", "activity", "account", "category", "destination_activity", "destination_account"]
        labels = {"activity": "Actividad de origen", "account": "Cuenta de origen", "category": "Categoría (ingreso/gasto)", "destination_activity": "Actividad de destino (solo transferencia)", "destination_account": "Cuenta de destino (solo transferencia)"}
        widgets = {"date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, user=user, **kwargs)
        for field, model in (("activity", Activity), ("account", Account), ("category", Category), ("destination_activity", Activity), ("destination_account", Account)):
            self.fields[field].queryset = model.objects.filter(owner=user)
        self.fields["submission"].initial = self.instance.pk
        self.fields["version"].initial = self.instance.revision if not self.instance._state.adding else 0
        if self.instance._state.adding:
            self.initial["date"] = timezone.localdate()
            del self.fields["reason"]
        else:
            self.fields["amount"].initial = Decimal(self.instance.cents) / 100
            self.fields["reason"].required = True
        self.order_fields(["kind", "date", "description", "amount", "activity", "account", "category", "destination_activity", "destination_account", "reason", "version", "submission"])

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("amount") is not None:
            self.instance.cents = int(cleaned["amount"] * 100)
        if cleaned.get("submission"):
            if self.instance._state.adding:
                self.instance.id = cleaned["submission"]
            elif self.instance.pk != cleaned["submission"]:
                self.add_error(None, "El identificador del formulario no coincide con el movimiento.")
        return cleaned


class EntryFilter(forms.Form):
    q = forms.CharField(label="Buscar concepto", required=False, max_length=80)
    activity = forms.ModelChoiceField(label="Actividad", queryset=Activity.objects.none(), required=False, empty_label="Todas las actividades")
    kind = forms.ChoiceField(label="Tipo", required=False, choices=[("", "Todos los tipos")] + Entry.KINDS)
    start = forms.DateField(label="Desde", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    end = forms.DateField(label="Hasta", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    void = forms.BooleanField(label="Incluir anulados", required=False)

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["activity"].queryset = Activity.objects.filter(owner=user)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("start") and cleaned.get("end") and cleaned["start"] > cleaned["end"]:
            raise forms.ValidationError("La fecha inicial no puede ser posterior a la final.")
        return cleaned


class VoidForm(forms.Form):
    version = forms.IntegerField(widget=forms.HiddenInput, min_value=1)
    reason = forms.CharField(label="Motivo de anulación", max_length=240)
    confirm = forms.BooleanField(label="Confirmo que deseo anular este movimiento y conservar su historial")
