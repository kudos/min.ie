# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_auto_20150117_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='base62',
        ),
        migrations.AlterField(
            model_name='link',
            name='id',
            field=models.CharField(max_length=12, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
