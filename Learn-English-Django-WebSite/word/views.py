import inspect

from django.shortcuts import render, redirect
from word.models import Word, WordKnowledge, CompletedWord, Theme
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils import formats
from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import random

lst = []
# answers = QuizModel.objects.all()
anslist = []


# for i in answers:
#     anslist.append(i.answer)

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
                  {"word": word, "theme": theme[1], "oran": oran, "kelimeSayisi": kelimeSayisi,
                   "kayitliVeri": kayitliVeri})


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
    theme = Theme.objects.filter(id=theme_name)[:1].get()
    return render(request, "theme.html", {"theme": theme.theme.upper(), "link": theme.themeLink, "words": words})


@login_required(login_url="user:login")
def quizzes(request):
    themes = Theme.objects.all()
    return render(request, "quizzes.html", {"themes": themes})


@login_required(login_url="user:login")
def quizTheme(request, theme_name):
    words = Word.objects.filter(word_id=theme_name, brainteaser=None).count()
    allWords = Word.objects.filter(word_id=theme_name).count()
    types = ["audial", "visual"]
    if allWords - words > 3:
        types.append("kinesthetic")
    print(types)
    theme = Theme.objects.filter(id=theme_name)[:1].get()
    return render(request, "quizTheme.html", {"quiz_url": theme_name, "theme": theme.theme.upper(), "types": types})


@login_required(login_url="user:login")
def quiz(request, theme_name, person_type):
    page = person_type + '.html'
    words = Word.objects.filter(word_id=theme_name).order_by('?')
    if len(words) < 1:
        return

    if person_type == "kinesthetic":
        words = words.exclude(brainteaser__isnull=True)

    options = words[:4]
    image_word = options[0]

    random.shuffle(options)

    choosed_answer = request.GET.get("mybtn1") or request.GET.get("mybtn2") or request.GET.get(
        "mybtn3") or request.GET.get("mybtn4")

    if choosed_answer == request.GET.get("word"):
        messages.success(request, "Правильна відповідь!")
    else:
        messages.info(request, 'Відповідь неправильна!')
    print("Correct answer =", image_word, "| callstack : ", inspect.currentframe())
# print((choosed_answer, request.GET.get("word"), request.GET.get("mybtn1"), request.GET.get("mybtn2"),
#        request.GET.get("mybtn3"),
#        request.GET.get("mybtn4")))

    return render(request, page,
                  {'btn1': options[0], 'btn2': options[1], 'btn3': options[2], 'btn4': options[3],
                   'word': image_word, 'person_type': person_type
                   })
