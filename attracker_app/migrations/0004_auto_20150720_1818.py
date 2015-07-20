# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attracker_app', '0003_auto_20150720_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hiker',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('trail_name', models.CharField(null=True, max_length=200, blank=True, verbose_name='Trail name')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='segment',
            name='hiker',
            field=models.ForeignKey(to='attracker_app.Hiker', default=1),
            preserve_default=False,
        ),
    ]
