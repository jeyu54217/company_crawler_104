# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company_info_closed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('not_open_id', models.CharField(max_length=255)),
                ('not_open_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Company_info_gov',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tax_id', models.CharField(max_length=255)),
                ('company_tax_name', models.CharField(max_length=255)),
                ('company_address', models.CharField(max_length=255, blank=True)),
                ('company_capital', models.CharField(max_length=255, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='result_list',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('company_id', models.CharField(max_length=255, null=True)),
                ('company_name', models.CharField(max_length=255)),
                ('company_profile', models.TextField(blank=True)),
                ('company_product', models.TextField(blank=True, null=True)),
                ('user_note', models.TextField(blank=True, null=True, default='')),
                ('checked', models.BooleanField(default=False)),
            ],
        ),
    ]
