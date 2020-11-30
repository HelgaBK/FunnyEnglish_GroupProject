"""learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from word import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('question/', views.question, name="question"),
    # path('quiz/', views.quiz, name="quiz"),
    path('quizzes/', views.quizzes, name="quizzes"),
    path('quizzes/<int:theme_name>', views.quizTheme, name="quizTheme"),
    path('quizzes/<int:theme_name>/<person_type>', views.quiz, name="quiz"),
    path('testing/', views.testing, name="testing"),
    path('statistics/', views.statistics, name="statistics"),
    path('user/', include("user.urls")),
    path('themes/', views.themes, name="themes"),
    re_path(r'^theme/(?P<theme_name>.+)$', views.theme, name="theme"),
    #path('quizzes/<int:theme_name>/<person_type>/result', views.quiz_result, name='quizResult')
    path('result/', views.quiz_result, name='quizResult')
]
