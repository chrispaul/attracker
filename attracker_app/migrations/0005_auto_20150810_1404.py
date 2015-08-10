# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attracker_app', '0004_auto_20150720_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='date',
            field=models.DateField(verbose_name='Date segment was hiked'),
        ),
    ]
