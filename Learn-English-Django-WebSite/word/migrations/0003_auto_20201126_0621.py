# Generated by Django 3.1.3 on 2020-11-26 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0002_auto_20201126_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='brainteaser',
            field=models.TextField(blank=True, default=None, verbose_name='Brainteaser'),
        ),
    ]
