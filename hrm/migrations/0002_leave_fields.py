from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE hrm_leave 
            ADD COLUMN IF NOT EXISTS no_of_days integer DEFAULT 0,
            ADD COLUMN IF NOT EXISTS remaining_days integer DEFAULT 0,
            ADD COLUMN IF NOT EXISTS created_at timestamp with time zone NULL,
            ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone NULL;
            """,
            reverse_sql="""
            ALTER TABLE hrm_leave 
            DROP COLUMN IF EXISTS no_of_days,
            DROP COLUMN IF EXISTS remaining_days,
            DROP COLUMN IF EXISTS created_at,
            DROP COLUMN IF EXISTS updated_at;
            """
        ),
    ] 