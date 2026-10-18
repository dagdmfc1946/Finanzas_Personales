from datetime import date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Activity, Account, AuditEvent, Category, Entry
from .services import save_entry, summary, void_entry


class MoneyTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("prueba", password="solo-pruebas-483!")
        self.personal = Activity.objects.create(owner=self.user, name="Personal")
        self.business = Activity.objects.create(owner=self.user, name="Taller")
        self.bank = Account.objects.create(owner=self.user, name="Principal", kind="banco")
        self.wallet = Account.objects.create(owner=self.user, name="Billetera", kind="billetera")

    def entry(self, kind, cents, **kwargs):
        return save_entry(Entry(owner=self.user, kind=kind, cents=cents, account=self.bank,
            activity=self.personal, description="Ejemplo", date=date(2026, 9, 1), **kwargs), self.user)

    def test_opening_and_transfer_do_not_inflate_income(self):
        self.entry("inicial", 100000)
        self.entry("ingreso", 50000)
        self.entry("gasto", 10101)
        self.entry("transferencia", 20000, destination_account=self.wallet, destination_activity=self.business)
        self.assertEqual(summary(self.user)["income"], 50000)
        self.assertEqual(summary(self.user)["balance"], 139899)
        self.assertEqual(summary(self.user, self.personal)["balance"], 119899)
        self.assertEqual(summary(self.user, self.business)["balance"], 20000)

    def test_same_account_can_change_activity_without_changing_total(self):
        self.entry("inicial", 30000)
        self.entry("transferencia", 12345, destination_account=self.bank, destination_activity=self.business)
        self.assertEqual(summary(self.user)["balance"], 30000)
        self.assertEqual(summary(self.user, self.business)["balance"], 12345)

    def test_rejects_zero_negative_and_identical_transfer(self):
        for cents in (0, -1):
            with self.subTest(cents=cents), self.assertRaises(ValidationError):
                self.entry("ingreso", cents)
        with self.assertRaises(ValidationError):
            self.entry("transferencia", 100, destination_account=self.bank, destination_activity=self.personal)

    def test_rejects_foreign_ownership_and_wrong_category(self):
        other = get_user_model().objects.create_user("otro")
        foreign = Account.objects.create(owner=other, name="Ajena", kind="banco")
        with self.assertRaises(ValidationError):
            self.entry("transferencia", 100, destination_account=foreign, destination_activity=self.business)
        category = Category.objects.create(owner=self.user, name="Venta", kind="ingreso")
        with self.assertRaises(ValidationError):
            self.entry("gasto", 100, category=category)

    def test_correction_keeps_history_and_rejects_stale_edit(self):
        entry = self.entry("ingreso", 100)
        entry.cents = 501
        save_entry(entry, self.user, expected_revision=1, reason="Corrección de importe")
        self.assertEqual(summary(self.user)["balance"], 501)
        self.assertEqual(AuditEvent.objects.filter(entity=str(entry.pk)).count(), 2)
        with self.assertRaises(ValidationError):
            save_entry(entry, self.user, expected_revision=1, reason="Edición antigua")

    def test_void_is_audited_and_removes_effect_not_record(self):
        entry = self.entry("gasto", 200)
        void_entry(entry, self.user, 1, "Registro duplicado")
        self.assertEqual(summary(self.user)["expenses"], 0)
        self.assertTrue(Entry.objects.get(pk=entry.pk).void)
        self.assertEqual(AuditEvent.objects.get(action="anulación").before["cents"], 200)
        with self.assertRaises(ValidationError):
            void_entry(entry, self.user, 1, "Otra anulación")
