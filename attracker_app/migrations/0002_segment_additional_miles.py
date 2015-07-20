# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attracker_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='segment',
            name='additional_miles',
            field=models.FloatField(default=0, verbose_name='Non-AT miles hiked with the segment'),
        ),
    ]
