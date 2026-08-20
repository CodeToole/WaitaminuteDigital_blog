from django.db import migrations


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0002_alter_aboutpage_body_alter_homepage_body_and_more'),
        ('wagtailcore', '0097_baselogentry_uuid_action_timestamp_indexes'),
    ]

    operations = [
        migrations.RunPython(noop, noop),
    ]

