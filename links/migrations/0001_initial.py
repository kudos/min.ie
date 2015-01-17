# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.URLField(max_length=2048)),
                ('base62', models.CharField(max_length=64, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('clicks', models.IntegerField(default=0)),
                ('ip', models.GenericIPAddressField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
