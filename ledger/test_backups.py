import json
import hashlib
from tempfile import TemporaryDirectory
from pathlib import Path
from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError
from django.test import override_settings
from .backups import canonical, export_backup, restore_backup
from .models import Activity, AuditEvent, Entry, Installation
from .services import summary
from .tests import MoneyTests


class BackupTests(MoneyTests):
    def setUp(self):
        super().setUp()
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.override = override_settings(BACKUP_DIR=self.folder.name)
        self.override.enable()
        self.addCleanup(self.override.disable)

    def test_restore_command_requires_confirmation_and_recovers_own_copy(self):
        Installation.objects.create(user=self.user)
        self.entry("ingreso", 300)
        output = StringIO()
        call_command("respaldo_finanzas", stdout=output)
        path = Path(output.getvalue().strip())
        self.assertTrue(path.exists())
        self.entry("gasto", 100)
        with self.assertRaises(CommandError):
            call_command("restaurar_finanzas", str(path), stdout=StringIO())
        self.assertEqual(summary(self.user)["balance"], 200)
        call_command("restaurar_finanzas", str(path), confirmar=True, stdout=StringIO())
        self.assertEqual(summary(self.user)["balance"], 300)

    def test_roundtrip_preserves_money_and_does_not_replace_password(self):
        self.entry("ingreso", 12345)
        password = self.user.password
        raw = export_backup(self.user)
        self.entry("gasto", 321)
        previous = restore_backup(self.user, raw)
        self.assertTrue(previous.exists())
        self.assertEqual(summary(self.user)["balance"], 12345)
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, password)
        self.assertNotIn(password.encode(), raw)
        self.assertTrue(AuditEvent.objects.filter(action="restauración").exists())

    def test_damaged_or_unknown_data_does_not_erase_existing_records(self):
        self.entry("ingreso", 200)
        raw = export_backup(self.user)
        for invalid in (b'{}', b'[]', raw.replace(b'200', b'201', 1)):
            with self.subTest(invalid=invalid[:12]), self.assertRaises(ValidationError):
                restore_backup(self.user, invalid)
            self.assertEqual(summary(self.user)["balance"], 200)

    def test_valid_hash_with_invalid_reference_rolls_back(self):
        self.entry("ingreso", 200)
        payload = json.loads(export_backup(self.user))
        payload["objects"]["entries"][0]["fields"]["account_id"] = "00000000-0000-0000-0000-000000000001"
        payload.pop("sha256")
        payload["sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
        with self.assertRaises(ValidationError):
            restore_backup(self.user, canonical(payload))
        self.assertEqual(Entry.objects.filter(owner=self.user).count(), 1)
        self.assertEqual(Activity.objects.filter(owner=self.user).count(), 2)
        self.assertEqual(summary(self.user)["balance"], 200)

    def test_invalid_revision_with_recomputed_hash_is_rejected(self):
        self.entry("ingreso", 200)
        payload = json.loads(export_backup(self.user))
        payload["objects"]["entries"][0]["fields"]["revision"] = 0
        payload.pop("sha256")
        payload["sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
        with self.assertRaises(ValidationError):
            restore_backup(self.user, canonical(payload))
        self.assertEqual(summary(self.user)["balance"], 200)
