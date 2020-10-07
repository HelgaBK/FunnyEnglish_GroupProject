from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Post 1',
        'content': 'First post content',
        'date_posted' : '07 September, 2020'
    },
    {
        'author': 'Jane',
        'title': 'Post 2',
        'content': 'Second post content',
        'date_posted' : '08 September, 2020'
    }
]

def home(request):
    context = {
        'posts':posts
    }
    return render(request,'FunnyEnglish/home.html',context)

def about(request):
    return render(request,'FunnyEnglish/about.html')