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
from django.db import connection
from django.views.decorators.csrf import csrf_exempt



def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def movie(request):

    movie_id = request.GET.get('m_id')
    print(movie_id)

    reserve_list = list()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.id, User.username, Article.*
            FROM User
            JOIN Article ON User.id = Article .uid_id
            WHERE Article.mid_id = %s
            ORDER BY Article.time DESC
        """, [movie_id])
        results = dictfetchall(cursor)
        reserve_list.append(results)

    film = Movies.objects.filter(mid=movie_id).values_list("mid", "rid", "name", "year", "rating", "time", "age", "introduction", "img", "director", "star", "tag")
    

    processed_movie_data = []

    # 遍歷資料
    for movie in film:
        # 將原始star欄位分割成名字列表
        names_list = movie[10].split(',')
        
        # 使用'・'連接名字列表，生成新的名字字符串
        new_names_string = '・'.join(names_list)
        
        # 創建一個新的元組，將修改後的star欄位放入其中
        processed_movie_tuple = (*movie[:10], new_names_string, *movie[11:])
        
        # 將新的元組加入處理後的資料列表中
        processed_movie_data.append(processed_movie_tuple)

    # forum_article = Article.objects.filter(mid=movie_id).order_by("-time").values('uid', 'mid', 'art_id', 'time', 'conent', 'title')

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

    return render(request, "movie.html", {'reserve_list': reserve_list, 'film': processed_movie_data})


@csrf_exempt
def movie_comment(request):
    #拿連結
    previous_url = request.META.get('HTTP_REFERER', '/')
    request.session['previous_url'] = previous_url
    # 拿會員ID
    if request.user.is_authenticated:
        user_id = request.user.id
        # print(user_id)

    movie_id = request.GET.get('m_id')

    reserve_list_comment = list()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.id, User.username, MovieComment.*, Movies.name
            FROM User
            JOIN MovieComment ON User.id = MovieComment.uid_id
            JOIN Movies ON MovieComment.mid_id = Movies.mid
            WHERE Movies.mid = %s
        """, [movie_id])
        results = dictfetchall(cursor)
        reserve_list_comment.append(results)


    # 'form': form, 
    return render(request, "movie.html", {'reserve_list_comment': reserve_list_comment})