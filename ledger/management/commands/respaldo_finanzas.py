from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import OperationalError
from ledger.backups import write_backup
from ledger.management.backup_owner import backup_owner


class Command(BaseCommand):
    help = "Crea una copia financiera privada sin incluir contraseñas."

    def add_arguments(self, parser):
        parser.add_argument("--usuario")

    def handle(self, *args, **options):
        user = backup_owner(options.get("usuario"))
        try:
            path, _ = write_backup(user)
        except (OSError, ValidationError, OperationalError) as error:
            raise CommandError("No se pudo crear la copia. Comprueba límites, espacio y permisos.") from error
        self.stdout.write(str(path))
