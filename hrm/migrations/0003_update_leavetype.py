from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0002_leave_fields'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE hrm_leavetype 
            DROP COLUMN IF EXISTS number_of_days,
            DROP COLUMN IF EXISTS policy_name,
            DROP COLUMN IF EXISTS leave_type,
            ADD COLUMN IF NOT EXISTS default_days integer DEFAULT 0,
            ADD COLUMN IF NOT EXISTS created_at timestamp with time zone NULL,
            ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone NULL;
            """,
            reverse_sql="""
            ALTER TABLE hrm_leavetype 
            DROP COLUMN IF EXISTS default_days,
            DROP COLUMN IF EXISTS created_at,
            DROP COLUMN IF EXISTS updated_at,
            ADD COLUMN number_of_days integer,
            ADD COLUMN policy_name varchar(100),
            ADD COLUMN leave_type varchar(100);
            """
        ),
    ] 