# Generated by Django 3.2.5 on 2021-09-06 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeapp', '0013_alter_keprof_keprof'),
    ]

    operations = [
        migrations.AddField(
            model_name='bobot',
            name='kuotadosen',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
