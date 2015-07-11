# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppalachianTrail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('miles', models.FloatField(default=2184.2, verbose_name='Total number of miles in AT')),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('start_mile', models.FloatField(default=0, verbose_name='Starting Nobo mile post')),
                ('end_mile', models.FloatField(default=0, verbose_name='Ending Nobo mile post')),
                ('date', models.DateTimeField(verbose_name='Date segment was hiked')),
            ],
        ),
    ]
