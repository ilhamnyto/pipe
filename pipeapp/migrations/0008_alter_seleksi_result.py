# Generated by Django 3.2.5 on 2021-08-01 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pipeapp', '0007_alter_batch_batchnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seleksi',
            name='result',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='result_peminatan', to='pipeapp.peminatan'),
        ),
    ]
