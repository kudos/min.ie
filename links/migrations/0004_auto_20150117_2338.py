# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_auto_20150117_2306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='link',
            new_name='url',
        ),
    ]
