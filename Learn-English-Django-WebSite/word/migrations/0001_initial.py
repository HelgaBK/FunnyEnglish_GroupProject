# Generated by Django 3.1.3 on 2020-11-25 23:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=25, unique=True, verbose_name='English')),
                ('img', models.ImageField(height_field=100, upload_to='static/img', width_field=100)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engWord', models.CharField(max_length=25, verbose_name='English')),
                ('trWord', models.CharField(max_length=25, verbose_name='Ukrainian')),
                ('sentence', models.TextField(verbose_name='Sentence')),
                ('structure', models.CharField(max_length=25, verbose_name='Structure')),
                ('img', models.ImageField(height_field=100, upload_to='static/img/words', width_field=100)),
                ('word', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='word.theme', verbose_name='Theme')),
            ],
        ),
        migrations.CreateModel(
            name='WordKnowledge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='Date to ask')),
                ('level', models.IntegerField(verbose_name='Level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='word.word', verbose_name='Word')),
            ],
        ),
        migrations.CreateModel(
            name='QuizModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='word.word', verbose_name='Answer')),
                ('option1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option1', to='word.word', verbose_name='Choice1')),
                ('option2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option2', to='word.word', verbose_name='Choice2')),
                ('option3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option3', to='word.word', verbose_name='Choice3')),
                ('option4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option4', to='word.word', verbose_name='Choice4')),
            ],
        ),
        migrations.CreateModel(
            name='CompletedWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='Memorization Date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='word.word', verbose_name='Word')),
            ],
        ),
    ]
