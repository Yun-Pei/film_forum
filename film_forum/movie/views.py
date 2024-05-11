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
from django.http import HttpResponse


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
        
        # 使用'・'連接名字列表
        new_names_string = '・'.join(names_list)
        
        processed_movie_tuple = (*movie[:10], new_names_string, *movie[11:])
        
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

    # user_has_commented = False
    # if user_id:
    #     user_has_commented = MovieComments.objects.filter(uid_id=user_id, mid_id=movie_id).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            user_id = request.user.id
            # print(user_id)
        rating = request.POST.get('rating')
        # print(rating)
        content = request.POST.get('addCommentContBox')
        # print(content)

        uid_id = User.objects.get(pk=user_id)
        mid_id = Movies.objects.get(pk=movie_id)
        existing_comment = MovieComments.objects.filter(uid_id=user_id, mid_id=movie_id).exists()
        if existing_comment:
            return HttpResponseRedirect(f'movie?m_id={movie_id}') #這個要處理一下
        time = timezone.now()

        print(uid_id)

        review = MovieComments(score=rating, content=content, mid=mid_id, time=time, uid=uid_id)
        review.save()

        return HttpResponseRedirect(f'movie?m_id={movie_id}')
    
    reserve_list_comment = list()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.id, User.username, MovieComments.*
            FROM User
            JOIN MovieComments ON User.id = MovieComments .uid_id
            WHERE MovieComments.mid_id =%s
            ORDER BY MovieComments.time DESC
        """, [movie_id])
        commentResults = dictfetchall(cursor)
        reserve_list_comment.append(commentResults)

    # print(request.GET)
    # print('below is mid')
    # print(movie_id)
    
    movie_id = request.GET.get('m_id') 

    if movie_id:
        if request.user.is_authenticated:
            user_id = request.user.id
            if user_id:
                user = User.objects.get(pk=user_id)
                film = Movies.objects.get(pk=movie_id)
                browse_time = timezone.now()
                browse = Browse(uid=user, mid=film, browseTime=browse_time)
                browse.save()
                print("Browse entry saved successfully!")

    return render(request, "movie.html", {'reserve_list': reserve_list, 'film': processed_movie_data, 'reserve_list_comment': reserve_list_comment})