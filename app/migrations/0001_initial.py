# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=12, serialize=False)),
                ('url', models.URLField(max_length=2048)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('clicks', models.IntegerField(default=0)),
                ('ip', models.GenericIPAddressField(null=True)),
            ],
        ),
    ]
