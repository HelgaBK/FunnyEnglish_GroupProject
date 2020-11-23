# Generated by Django 2.2 on 2019-04-30 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kelime', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kelime',
            name='engWord',
            field=models.CharField(max_length=25, verbose_name='İngilizce'),
        ),
        migrations.AlterField(
            model_name='kelime',
            name='sentence',
            field=models.TextField(verbose_name='Cümle'),
        ),
        migrations.AlterField(
            model_name='kelime',
            name='structure',
            field=models.CharField(max_length=25, verbose_name='Yapısı'),
        ),
        migrations.AlterField(
            model_name='kelime',
            name='trWord',
            field=models.CharField(max_length=25, verbose_name='Türkçe'),
        ),
        migrations.CreateModel(
            name='KelimeBilgi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateTimeField(verbose_name='Sorulacak Tarih')),
                ('Level', models.IntegerField(verbose_name='Seviyesi')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
                ('Word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kelime.Kelime', verbose_name='Kelime')),
            ],
        ),
    ]
