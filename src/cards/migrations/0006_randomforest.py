# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0009_satellite'),
        ('cards', '0005_auto_20160304_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='RandomForest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('aoi_name', models.CharField(max_length=200)),
                ('param_set', models.TextField()),
                ('run_set', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=200)),
                ('mvrf', models.CharField(max_length=200)),
                ('satellite', models.ForeignKey(to='gsi.Satellite')),
            ],
            options={
                'verbose_name_plural': 'Random Forest cards',
            },
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
    ]
