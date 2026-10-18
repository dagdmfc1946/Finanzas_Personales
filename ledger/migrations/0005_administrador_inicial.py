from django.conf import settings
from django.db import migrations

def promote_owner(apps, schema_editor):
    Installation = apps.get_model("ledger", "Installation")
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)
    owner = Installation.objects.using(schema_editor.connection.alias).first()
    if owner:
        User.objects.using(schema_editor.connection.alias).filter(pk=owner.user_id).update(is_staff=True)

class Migration(migrations.Migration):
    dependencies = [("ledger", "0004_alter_category_options_category_group"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.RunPython(promote_owner, migrations.RunPython.noop)]
