# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='schoolprofile',
            old_name='school_name',
            new_name='name',
        ),
    ]
