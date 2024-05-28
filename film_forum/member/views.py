import csv
from django.shortcuts import render, redirect
from .models import *
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from .models import *
from .forms import *
from django.contrib import auth
from django.http import HttpResponseRedirect  #直接回到某個網址
from django.db import connection


# @csrf_exempt
def login(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)


            if user is not None and user.is_active:
                # referer_url = request.META.get('HTTP_REFERER', '/')
                # previous_url = request.session.get('previous_url', '/')
                # referer_url = request.META.get('HTTP_REFERER', '/')
                previous_url = request.session.get('previous_url', '/')

                
                auth.login(request, user)
                return HttpResponseRedirect(previous_url)
            else:
                error_message = "Invalid username or password. Please try again."
                return render(request, 'login.html', {'form': form, 'msg': msg, 'error_message': error_message})            

        else:
            msg = 'error validating form'
    

    return render(request, "login.html", {'form': form, 'msg': msg})
    
def register(request):
    msg = None
    
    # form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['title']

            # forum = User(title=title, conent=conent, time=now_time, uid=user_id, mid=film_id)
            user = form.save(commit=False) #阻止form save
            user.img = request.POST.get('picture', '1') #get img number, if not get push '1'

            print(request.POST.get('picture'))

            user.save()
            msg = 'user created'

            previous_url = request.session.get('previous_url', '/')

            return redirect("login")
        else:
            msg = 'form is not valid'

    else:
        form = RegisterForm()
    
    context = {
        'form': form,
        'msg': msg,
    }

    return render(request, "register.html", context)

def log_out(request):
    auth.logout(request)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def watchlist(request):

    if request.user.is_authenticated:
        user_id = request.user.id
        if request.method == 'POST':
            if request.POST.get('mode') == 'unfollow':
                # print('1111111')
                movie_id = request.POST.get('m_id')
                # print(movie_id)
                # if request.user.is_authenticated:
                #     user_id = request.user.id
                unfollow = LikeMovies.objects.get(mid_id = movie_id, uid_id = user_id)
                unfollow.delete()
                return HttpResponseRedirect('/watchlist')
            
    favo_movie = list()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Movies.*
            FROM Movies
            JOIN LikeMovies ON LikeMovies.mid_id = Movies.mid
            WHERE LikeMovies.uid_id = %s
            ORDER BY LikeMovies.time ASC
        """, [user_id])
        watchlistResults = dictfetchall(cursor)
        favo_movie.append(watchlistResults)

    InfoList = list()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.username, COUNT(*) AS count
            FROM User
            JOIN LikeMovies ON User.id = LikeMovies.uid_id
            WHERE User.id = %s
            GROUP BY User.id
        """, [user_id])
    InfoList = dictfetchall(cursor)
    # print(InfoList)
    return render(request, 'watchlist.html', {'favo_movie': favo_movie, 'InfoList': InfoList})