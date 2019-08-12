
from __future__ import unicode_literals

from django.db import migrations


def insert_sample_user_information():
    from django.conf import settings
    import os
    sql_statements = open(os.path.join(
        settings.BASE_DIR, 'payment/sql/information.sql'), 'r').read()
    return sql_statements


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [

        migrations.RunSQL(insert_sample_user_information()),
    ]
