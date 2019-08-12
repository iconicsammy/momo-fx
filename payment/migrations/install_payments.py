
from __future__ import unicode_literals

from django.db import migrations


def insert_sample_payments_information():
    from django.conf import settings
    import os
    sql_statements = open(os.path.join(
        settings.BASE_DIR, 'payment/sql/payments.sql'), 'r').read()
    return sql_statements


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payment', 'install_data'),
    ]

    operations = [

        migrations.RunSQL(insert_sample_payments_information()),
    ]
