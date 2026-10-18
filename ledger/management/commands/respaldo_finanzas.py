from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import OperationalError
from ledger.backups import write_backup
from ledger.models import Installation


class Command(BaseCommand):
    help = "Crea una copia financiera privada sin incluir contraseñas."

    def handle(self, *args, **options):
        installation = Installation.objects.select_related("user").first()
        if installation is None:
            raise CommandError("Primero configura tu usuario desde el aplicativo.")
        try:
            path, _ = write_backup(installation.user)
        except (OSError, ValidationError, OperationalError) as error:
            raise CommandError("No se pudo crear la copia. Comprueba límites, espacio y permisos.") from error
        self.stdout.write(str(path))
