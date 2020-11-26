from django.db import models


# Create your models here.


class Theme(models.Model):
    theme = models.CharField(max_length=25, verbose_name="English", unique=True)
    img = models.ImageField(upload_to='static/img')


class Word(models.Model):
    engWord = models.CharField(max_length=25, verbose_name="English")
    trWord = models.CharField(max_length=25, verbose_name="Ukrainian")
    word = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name="Theme", default=None)
    sentence = models.TextField(verbose_name="Sentence")
    structure = models.CharField(max_length=25, verbose_name="Structure")
    img = models.ImageField(upload_to='static/img/words')

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


class QuizModel(models.Model):
    question = models.TextField()
    option1 = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name="Choice1",
                                related_name="option1")
    option2 = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name="Choice2",
                                related_name="option2")
    option3 = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name="Choice3",
                                related_name="option3")
    option4 = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name="Choice4",
                                related_name="option4")
    answer = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name="Answer",
                               related_name="answer")
