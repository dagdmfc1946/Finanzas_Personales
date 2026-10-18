from pathlib import Path
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, OperationalError
from ledger.backups import LIMIT, restore_backup
from ledger.models import Installation


class Command(BaseCommand):
    help = "Restaura una copia financiera propia y crea respaldo previo."

    def add_arguments(self, parser):
        parser.add_argument("archivo")
        parser.add_argument("--confirmar", action="store_true")

    def handle(self, *args, **options):
        if not options["confirmar"]:
            raise CommandError("La restauración reemplaza tus datos financieros. Revisa el archivo y utiliza --confirmar.")
        installation = Installation.objects.select_related("user").first()
        if installation is None:
            raise CommandError("Primero crea tu usuario local. La copia no contiene contraseñas.")
        try:
            path = Path(options["archivo"])
            with path.open("rb") as stream:
                raw = stream.read(LIMIT + 1)
            previous = restore_backup(installation.user, raw)
        except (OSError, ValidationError, IntegrityError, OperationalError) as error:
            raise CommandError("No se restauró la copia. Comprueba formato, referencias y permisos; los datos previos se conservan.") from error
        self.stdout.write(f"Datos restaurados. Copia previa: {previous}")
