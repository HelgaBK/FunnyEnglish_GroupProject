from django.db import models

# Create your models here.


class Theme(models.Model):
    theme = models.CharField(max_length=25, verbose_name="English", unique=True, primary_key= True)
    img = models.ImageField(upload_to='static/img', height_field=100, width_field=100)


class Word(models.Model):
    engWord = models.CharField(max_length=25, verbose_name="English")
    trWord = models.CharField(max_length=25, verbose_name="Ukrainian")
    word = models.ForeignKey(Theme, to_field='theme', on_delete=models.CASCADE, verbose_name="Theme", default=None)
    sentence = models.TextField(verbose_name="Sentence")
    structure = models.CharField(max_length=25, verbose_name="Structure")
    img = models.ImageField(upload_to='static/img/word_img', null=True, blank=True)

    def __str__(self):
        return self.engWord


class WordKnowledge(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name="Word")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="User")
    date = models.DateTimeField(blank=True, null=True, verbose_name="Date to ask")
    level = models.IntegerField(verbose_name="Level")


class CompletedWord(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name="Word")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="User")
    date = models.DateTimeField(blank=True, null=True, verbose_name="Memorization Date")
