from pathlib import Path
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from . import test_user_safety
from .models import Installation, Entry, AuditEvent

class RegistrationAdminTests(TestCase):
    setUp = test_user_safety.UserSafetyTests.setUp
    confirmation = test_user_safety.UserSafetyTests.confirmation
    def registration(self,**changes):
        return {"username":"nuevo_registro","first_name":"Persona","last_name":"Ensayo","password1":"Alta-personal!963","password2":"Alta-personal!963",**changes}

    def test_signup_is_available_and_never_grants_admin(self):
        self.client.logout()
        self.assertContains(self.client.get("/acceso/"),"Crear usuario")
        response=self.client.post("/registro/",self.registration(is_staff="on",is_superuser="on",role="admin"))
        self.assertEqual(response.status_code,302)
        person=get_user_model().objects.get(username="nuevo_registro")
        self.assertFalse(person.is_staff or person.is_superuser)
        self.assertEqual(get_user_model().objects.filter(is_staff=True).count(),1)
        self.assertFalse(Entry.objects.filter(owner=person).exists())
        self.assertEqual(self.client.get("/app/usuarios/").status_code,403)

    def test_signup_requires_csrf_and_before_installation_goes_to_setup(self):
        public=Client(enforce_csrf_checks=True)
        self.assertEqual(public.post("/registro/",self.registration()).status_code,403)
        Installation.objects.all().delete()
        self.client.logout()
        self.assertRedirects(self.client.get("/registro/"),"/configurar/",fetch_redirect_response=False)

    def test_admin_edits_user_metadata_without_promoting(self):
        self.client.force_login(self.admin)
        response=self.client.post(f"/app/usuarios/{self.user.pk}/",{"username":"usuario_editado","first_name":"Nombre editado","last_name":"Ensayo","is_active":"on","role":"admin","is_staff":"on","confirm":"on","current_password":"Ensayo-local!837"})
        self.assertEqual(response.status_code,302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username,"usuario_editado")
        self.assertEqual(self.user.first_name,"Nombre editado")
        self.assertFalse(self.user.is_staff)
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())

    def test_user_deletion_is_admin_only_and_preserves_backup(self):
        url=f"/app/usuarios/{self.user.pk}/eliminar/"
        self.assertEqual(self.client.get(url).status_code,403)
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(url).status_code,200)
        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())
        bad=self.confirmation("ELIMINAR USUARIO usuario_ensayo",current_password="mal")
        self.assertEqual(self.client.post(url,bad).status_code,400)
        response=self.client.post(url,self.confirmation("ELIMINAR USUARIO usuario_ensayo"))
        self.assertEqual(response.status_code,302)
        self.assertFalse(get_user_model().objects.filter(pk=self.user.pk).exists())
        self.assertFalse(Entry.objects.filter(pk=self.entry.pk).exists())
        self.assertTrue(get_user_model().objects.filter(pk=self.admin.pk,is_staff=True).exists())
        self.assertEqual(len(list((Path(self.folder.name)/f"usuario-{self.user.pk}").glob("*.json"))),1)
        self.assertTrue(AuditEvent.objects.filter(owner=self.admin,action="eliminar usuario").exists())

    def test_admin_is_protected_and_failed_backup_preserves_user(self):
        self.client.force_login(self.admin)
        root_url=f"/app/usuarios/{self.admin.pk}/eliminar/"
        self.assertEqual(self.client.post(root_url,self.confirmation("ELIMINAR USUARIO admin_ensayo")).status_code,400)
        with patch("ledger.safety_services.write_backup",side_effect=OSError("ensayo")):
            response=self.client.post(f"/app/usuarios/{self.user.pk}/eliminar/",self.confirmation("ELIMINAR USUARIO usuario_ensayo"))
        self.assertEqual(response.status_code,400)
        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())

    def test_admin_new_account_is_always_normal(self):
        self.client.force_login(self.admin)
        response=self.client.post("/app/usuarios/nuevo/",self.registration(role="admin",is_staff="on",current_password="Ensayo-local!837"))
        self.assertEqual(response.status_code,302)
        self.assertFalse(get_user_model().objects.get(username="nuevo_registro").is_staff)
