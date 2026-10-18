from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CurrentPasswordMixin:
    def clean_current_password(self):
        password = self.cleaned_data["current_password"]
        if not self.actor.check_password(password):
            raise forms.ValidationError("La contraseña actual no es correcta.")
        return password


class ProfileForm(CurrentPasswordMixin, forms.ModelForm):
    current_password = forms.CharField(label="Tu contraseña actual", widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name"]
        labels = {"first_name": "Nombres (opcional)", "last_name": "Apellidos (opcional)"}

    def __init__(self, *args, actor, **kwargs):
        self.actor = actor
        super().__init__(*args, instance=actor, **kwargs)


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "first_name", "last_name"]


class UserCreateForm(CurrentPasswordMixin, UserCreationForm):
    current_password = forms.CharField(label="Tu contraseña de administrador", widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "first_name", "last_name"]

    def __init__(self, *args, actor, **kwargs):
        self.actor = actor
        super().__init__(*args, **kwargs)


class UserAccessForm(CurrentPasswordMixin, forms.ModelForm):
    current_password = forms.CharField(label="Tu contraseña de administrador", widget=forms.PasswordInput)
    confirm = forms.BooleanField(label="Confirmo editar los datos y el acceso de este usuario")

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "is_active"]
        labels = {"is_active": "Acceso activo"}

    def __init__(self, *args, actor, **kwargs):
        self.actor = actor
        super().__init__(*args, **kwargs)


class DestructiveForm(CurrentPasswordMixin, forms.Form):
    reason = forms.CharField(label="Motivo", max_length=240)
    current_password = forms.CharField(label="Tu contraseña actual", widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))
    phrase = forms.CharField(label="Texto de confirmación", max_length=180)
    confirm = forms.BooleanField(label="Entiendo el efecto indicado y confirmo la operación sobre mis datos")
    version = forms.IntegerField(widget=forms.HiddenInput, min_value=0, initial=0)

    def __init__(self, *args, actor, phrase, **kwargs):
        self.actor = actor
        self.expected_phrase = phrase
        super().__init__(*args, **kwargs)
        self.fields["phrase"].help_text = f"Escribe exactamente: {phrase}"

    def clean_phrase(self):
        if self.cleaned_data["phrase"] != self.expected_phrase:
            raise forms.ValidationError("El texto no coincide con la confirmación indicada.")
        return self.cleaned_data["phrase"]
