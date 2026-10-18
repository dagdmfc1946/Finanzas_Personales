from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from ledger.models import Installation

def backup_owner(username):
    User = get_user_model()
    if username:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as error:
            raise CommandError("El usuario indicado no existe.") from error
    installation = Installation.objects.select_related("user").first()
    if installation is None:
        raise CommandError("Primero configura tu usuario local.")
    if User.objects.count() != 1:
        raise CommandError("Hay varios usuarios. Indica --usuario NOMBRE para elegir de quién son los datos; no se modificó nada.")
    return installation.user
