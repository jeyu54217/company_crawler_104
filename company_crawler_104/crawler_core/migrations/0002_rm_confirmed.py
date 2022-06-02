# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RM_Confirmed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('RM_confirmed_id', models.CharField(max_length=255)),
                ('RM_channel_chi_desc', models.CharField(max_length=255)),
            ],
        ),
    ]
