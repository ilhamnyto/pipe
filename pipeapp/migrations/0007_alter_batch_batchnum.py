# Generated by Django 3.2.5 on 2021-08-01 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeapp', '0006_auto_20210801_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batchnum',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
