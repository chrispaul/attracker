# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attracker_app', '0005_auto_20150810_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='additional_miles',
            field=models.FloatField(verbose_name='Non-AT miles hiked with the segment', blank=True, default=0),
        ),
    ]
