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


from urllib.request import urlopen as uReq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import time
# import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import csv
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


# Create your views here.

# @csrf_exempt
# def login(request):
#     if request.method == "GET":
#         return render(request, "login.html")


# crawl data into database
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

            form.save()
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
    
    # if request.method == "POST":
    #     # movie = Movies(name='The Shawshank Redemption', year='1994', time='2h 22m', age='R-12', introduction='Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.'
    #     #                 , img='https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_QL75_UX140_CR0,1,140,207_.jpg',
    #     #                 director='Frank Darabont', star='Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler, Clancy Brown, Gil Bellows, Mark Rolston, James Whitmore, Jeffrey DeMunn, Larry Brandenburg, Neil Giuntoli, Brian Libby, David Proval, Joseph Ragno, Jude Ciccolella, Paul McCrane, Renee Blaine, Scott Mann',
    #     #                 tag='Drama', rating='5'
    #     #                 )
        
    #     # movie.save()

    #     # return HttpResponse('OK!')
    #     with open('C:/Users/Ariel/db_project/film_forum/film_forum/member/top250_all.csv', 'r', encoding='latin-1') as file:
    #     # 使用CSV讀取器讀取CSV文件
    #         csv_reader = csv.reader(file)
    #         # 跳過首行，因為它可能是標題行
    #         next(csv_reader)
    #         # 遍歷CSV文件中的每一行
    #         for row in csv_reader:
    #             # 根據CSV文件的結構，假設每一行的順序分別是：name, year, time, age, introduction, link, img, director, star, type
    #             # 創建Movies對象並保存到數據庫中
    #             movie = Movies.objects.create(
    #                 name=row[0],
    #                 year=row[1],
    #                 time=row[2],
    #                 age=row[3],
    #                 introduction=row[4],
    #                 # link=row[5],
    #                 img=row[6],
    #                 director=row[7],
    #                 star=row[8],
    #                 tag=row[9],
    #                 rating='5',
                    
    #             )
    #             # 保存Movies對象
    #             movie.save()

    #     return HttpResponse('Movies imported successfully from CSV!')
# @csrf_exempt
# def crawl(request):
#     if request.method == "POST":

#         with open('C:/Users/Ariel/OneDrive/桌面/imdb/.csv', 'r', encoding='utf-8') as file:

#             csv_reader = csv.reader(file)

#             for row in csv_reader:

#                 movie = Movies(name=row[0], year=row[1], time=row[2], age=row[3], introduction=row[4], img=row[5],director=row[6], star=row[7],tag=row[8], rating='0')

#                 movie.save()
                        

#         return HttpResponse('Movies imported successfully from CSV!')
    
#     # return render("crwal.html")
#     return render(request, "crawl.html")