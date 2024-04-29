from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from member.models import *
from .forms import ForumsForm
# # from .models import *
# from forum.models import Forums, ForumsMessage
from member.models import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect  #直接回到某個網址




def movie(request):

    movie_id = request.GET.get('m_id')
    print(movie_id)

    film = Movies.objects.filter(mid=movie_id).values_list("mid", "rid", "name", "year", "rating", "time", "age", "introduction", "img", "director", "star", "tag")
    forum_article = Article.objects.filter(mid=movie_id).order_by("-time").values('uid', 'mid', 'art_id', 'time', 'conent', 'title')

    # for article in forum_article:
    #     article.formatted_time = article.time.strftime("%Y-%m-%d %I:%M %p")

    print(film)


    previous_url = request.META.get('HTTP_REFERER', '/')
    
    request.session['previous_url'] = previous_url


            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        # jsut test
        # else:
        #     return redirect('forum')
    # else:
    #     form = ForumsForm()

    return render(request, "movie.html", {'forum_article': forum_article, 'film': film})