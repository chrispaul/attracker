# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attracker_app', '0002_segment_additional_miles'),
    ]

    operations = [
        migrations.AddField(
            model_name='segment',
            name='description',
            field=models.CharField(verbose_name='Comments on the section hiked', max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='segment',
            name='picture_url',
            field=models.CharField(verbose_name='Link to pictures', max_length=300, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='segment',
            name='video_url',
            field=models.CharField(verbose_name='Link to video from the section', max_length=300, null=True, blank=True),
        ),
    ]
