from django.shortcuts import render, redirect
from word.models import Word, WordKnowledge, CompletedWord, Theme, QuizModel
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils import formats
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

lst = []
answers = QuizModel.objects.all()
anslist = []
for i in answers:
    anslist.append(i.answer)

def result(request):
    score = 0
    for i in range(len(lst)):
        if lst[i] == anslist[i]:
            score += 1
    return render(request, 'result.html', {'score': score, 'lst': lst})


def save_ans(request):
    ans = request.GET['ans']
    lst.append(ans)


# def welcome(request):
#     lst.clear()
#     return render(request, 'welcome.html')


# Create your views here.

def index(request):
    return render(request, "index.html")


@login_required(login_url="user:login")
def question(request):
    answer = request.GET.get("answer")
    question = request.GET.get("soru")

    if answer:
        dogru = Word.objects.filter(engWord=question).first()
        if dogru.trWord.upper() == answer.upper():
            messages.success(request, "Вітаємо! Правильна відповідь.")
            Kayit = WordKnowledge(user=request.user, word=dogru, level=1, date=timezone.now(
            ) + timedelta(days=1) + timedelta(hours=3))
            Kayit.save()
            return redirect("question")
        else:
            messages.info(request, "Ой! Неправильна відповідь.")

    control = True
    while control:
        word = Word.objects.order_by("?").first()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM word_theme WHERE id = %s', [word.word_id])
        theme = cursor.fetchone()
        inProgressCount = WordKnowledge.objects.filter(word=word, user=request.user).count()
        doneCount = CompletedWord.objects.filter(word=word, user=request.user).count()
        if inProgressCount == 0 and doneCount == 0:
            control = False

        kelimeSayisi = Word.objects.all().count()
        kayitliVeri = WordKnowledge.objects.filter(user=request.user).count()
        tamamlananVeri = CompletedWord.objects.filter(user=request.user).count()
        if kelimeSayisi == kayitliVeri + tamamlananVeri:
            messages.success(request, "Вітаємо! Ви знаєте всі слова")
            return redirect("index")

        oran = ((kayitliVeri + tamamlananVeri) * 100) / kelimeSayisi
        oran = int(oran)

    return render(request, "question.html",
                  {"word": word,"theme":theme[1], "oran": oran, "kelimeSayisi": kelimeSayisi, "kayitliVeri": kayitliVeri})


@login_required(login_url="user:login")
def testing(request):
    count = WordKnowledge.objects.filter(user=request.user).count()
    if count == 0:
        messages.info(request, "Спочатку слід вивчити словник")
        return redirect("index")

    cevap = request.GET.get("answer")
    soru = request.GET.get("soru")
    if cevap:
        dogru = Word.objects.filter(engWord=soru).first()
        kayit = WordKnowledge.objects.filter(
            user=request.user, word_id=dogru.id).first()
        if dogru.trWord.upper() == cevap.upper():
            messages.success(request, "Вітаємо! Правильна відповідь!")
            if kayit.level == 1:
                kayit.level = 2
                kayit.date = datetime.now() + timedelta(weeks=1)
                kayit.save()
            elif kayit.level == 2:
                kayit.level = 3
                kayit.date = datetime.now() + timedelta(days=30)
                kayit.save()
            elif kayit.level == 3:
                kayit.level = 4
                kayit.date = datetime.now() + timedelta(days=180)
                kayit.save()
            elif kayit.level == 4:
                messages.success(request, "Вітаємо! Ви запам'ятали слово " + soru)
                Tamamlanan = CompletedWord(
                    user=request.user, word=dogru, date=timezone.now())
                Tamamlanan.save()
                kayit.delete()
        else:
            messages.info(request, "Ой! Неправильна відповідь.")
            kayit.level = 1
            kayit.date = timezone.now() + timedelta(days=1) + timedelta(hours=3)
            kayit.save()

    count = WordKnowledge.objects.filter(user=request.user).count()
    if count == 0:
        return redirect("index")

    id = WordKnowledge.objects.filter(user=request.user).order_by("date").first()
    kelime = Word.objects.filter(id=id.word_id).first()
    if id.date.toordinal() > datetime.now().toordinal():
        messages.success(request, "Зараз у вас немає слів для перевірки.")
        return redirect("index")
    return render(request, "testing.html", {"word": kelime})


@login_required(login_url="user:login")
def statistics(request):
    yearCount = [0, 0, 0]
    yearName = ["", "", ""]
    for i in range(0, 3):
        yearCount[i] = CompletedWord.objects.filter(user=request.user, date__year=int(timezone.now().year) - i).count()
        yearName[i] = str(int(timezone.now().year) - i)

    mountCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 12):
        mountCount[i] = CompletedWord.objects.filter(user=request.user, date__year=timezone.now().year,
                                                     date__month=1 + i).count()

    dayCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 30):
        dayCount[i] = CompletedWord.objects.filter(user=request.user, date__year=timezone.now().year,
                                                   date__month=timezone.now().month, date__day=1 + i).count()

    current = timezone.now()
    current = formats.date_format(current, "DATE_FORMAT")
    current = current.split()
    currentMonth = current[1]
    currentYear = current[2]

    return render(request, "statistics.html",
                  {"yearCount": yearCount, "yearName": yearName, "mountCount": mountCount, "dayCount": dayCount,
                   "currentMonth": currentMonth, "currentYear": currentYear})


@login_required(login_url="user:login")
def themes(request):
    themes = Theme.objects.all()
    return render(request, "themes.html", {"themes": themes})


@login_required(login_url="user:login")
def theme(request, theme_name):
    words = Word.objects.filter(word_id=theme_name).all()
    return render(request, "theme.html", {"theme": theme_name, "words": words})

@login_required(login_url="user:login")
def quiz(request):
    return render(request, 'quiz.html')
    ans = request.GET.get("answer")
    soru = request.GET.get("soru")

    if ans:
        dogru = Word.objects.filter(engWord=soru).first()
        if dogru.trWord.upper() == ans.upper():
            messages.success(request, "Вітаємо! Правильна відповідь.")
            Kayit = WordKnowledge(user=request.user, word=dogru, level=1, date=timezone.now(
            ) + timedelta(days=1) + timedelta(hours=3))
            Kayit.save()
            return redirect("question")
        else:
            messages.info(request, "Ой! Неправильна відповідь.")

    control = True
    while control:
        word = Word.objects.order_by().first()
        theme = Theme.objects.all()
        inProgressCount = WordKnowledge.objects.filter(word=word, user=request.user).count()
        doneCount = CompletedWord.objects.filter(word=word, user=request.user).count()
        if inProgressCount == 0 and doneCount == 0:
            control = False

        kelimeSayisi = Word.objects.all().count()
        kayitliVeri = WordKnowledge.objects.filter(user=request.user).count()
        tamamlananVeri = CompletedWord.objects.filter(user=request.user).count()
        if kelimeSayisi == kayitliVeri + tamamlananVeri:
            messages.success(request, "Вітаємо! Ви знаєте всі слова")
            return redirect("index")

        oran = ((kayitliVeri + tamamlananVeri) * 100) / kelimeSayisi
        oran = int(oran)

    return render(request, "quiz.html",
                  {"word": word, "oran": oran, "kelimeSayisi": kelimeSayisi, "kayitliVeri": kayitliVeri})

