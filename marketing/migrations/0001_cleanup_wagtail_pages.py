from django.db import migrations


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunSQL(
            sql="""
                DROP TABLE IF EXISTS marketing_aboutpage;
                DROP TABLE IF EXISTS marketing_homepage;
                DROP TABLE IF EXISTS marketing_servicespage;
            """,
            reverse_sql="""
                -- Legacy Wagtail page tables were intentionally removed when the
                -- marketing app was converted back to plain Django.
            """,
        ),
    ]
