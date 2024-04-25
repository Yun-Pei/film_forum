from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
# from .forms import ForumsForm
from .models import *

# Create your views here.
@csrf_exempt
def forum(request):
    # if request.method == "POST":
    forum_articles = Forums.objects.filter().order_by("-time").values('f_id', 'm_id', 'time', 'title', 'content', 'user_id')

    return render(request, "forum.html", {'forum_article': forum_articles})
    
@csrf_exempt
def forum_article(request):
    # if request.method == "POST":
    forum_articles = Forums.objects.filter().order_by("-time").values('f_id', 'm_id', 'time', 'title', 'content', 'user_id')

    return render(request, "forum_article.html", {'forum_article': forum_articles})