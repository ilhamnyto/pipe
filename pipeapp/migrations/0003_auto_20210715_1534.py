# Generated by Django 3.0.8 on 2021-07-15 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeapp', '0002_auto_20210715_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seleksi',
            name='score1',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='seleksi',
            name='score2',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
    ]