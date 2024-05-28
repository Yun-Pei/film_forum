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
@csrf_exempt
def movie(request):

    movie_id = request.GET.get('m_id')
    # print(f'First{movie_id}')

    reserve_list = list()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.id, User.username, User.img, Article.*
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
        names_list_10 = movie[10].split(',')
        names_list_11 = movie[11].split(',')
        
        # 使用'・'連接名字列表
        new_names_string_10 = '・'.join(names_list_10)
        new_names_string_11 = '/ '.join(names_list_11)
        
        # 建立處理後的電影元組
        processed_movie_tuple = (*movie[:10], new_names_string_10, new_names_string_11, *movie[12:])
        
        # 將處理後的電影元組加入處理後的電影數據列表
        processed_movie_data.append(processed_movie_tuple)



    previous_url = request.META.get('HTTP_REFERER', '/')
    
    request.session['previous_url'] = previous_url


    user_has_commented = False

    if request.method == 'GET':
        if request.user.is_authenticated:
            user_id = request.user.id
            movie_id = request.GET.get('m_id')
            user_has_favorite = LikeMovies.objects.filter(uid_id=user_id, mid_id=movie_id).exists()
            user_has_commented = MovieComments.objects.filter(uid_id=user_id, mid_id=movie_id).exists()

            # Browse
            Bro_user = User.objects.get(pk=user_id)
            # print(f'{user}')
            print(f'Second{movie_id}')
            film = Movies.objects.get(pk=movie_id)
            browse_time = timezone.now()
            browse = Browse(uid=Bro_user, mid=film, browseTime=browse_time)
            browse.save()
            # print("Browse entry saved successfully!")
        else:
            user_has_favorite = False
    # if request.user.is_authenticated:
    #     print('user_has_commented')
    #     user_id = request.user.id
    
    reserve_list_comment = list()
    avg_score = 0

    if request.method == 'POST':
        if request.user.is_authenticated:
            user_id = request.user.id
            # movie_id = request.POST.get('m_id')
            if request.POST.get('mode') == 'addfollow':
                # 检查是否已经存在该收藏记录
                movie_id = request.POST.get('m_id')
                if not LikeMovies.objects.filter(uid_id=user_id, mid_id=movie_id).exists():
                    time = timezone.now()
                    like = LikeMovies(uid_id=user_id, mid_id=movie_id, time=time)
                    like.save()
                return HttpResponseRedirect(f'movie?m_id={movie_id}')
            elif request.POST.get('mode') == 'unfollow':
                # print('1111111')
                movie_id = request.POST.get('m_id')
                # print(movie_id)
                # if request.user.is_authenticated:
                #     user_id = request.user.id
                unfollow = LikeMovies.objects.get(mid_id = movie_id, uid_id = user_id)
                unfollow.delete()
                return HttpResponseRedirect(f'movie?m_id={movie_id}')
            
            elif request.POST.get('mode') == "movie_comment_delete":
                movie_id = request.POST.get('m_id')
                Comment_id = request.POST.get('Comment_id')
                # print(movie_id, Comment_id)
                delete_comment = MovieComments.objects.get(Comment_id=Comment_id)
                delete_comment.delete()
                return HttpResponseRedirect(f'movie?m_id={movie_id}')
            
            elif request.POST.get('mode') == "movie_comment_edit":
                Comment_id = request.POST.get('Comment_id')
                movie_id = request.POST.get('m_id')
                content = request.POST.get('content')
                time = MovieComments.objects.filter(Comment_id=Comment_id).values('time')
                # print(Comment_id, movie_id, content, time)

                # user_id = User.objects.get(pk=user_id)
                # movie_id = Movies.objects.get(pk=movie_id)
                # Comment_id = MovieComments.objects.get(pk=Comment_id)

                comment_edit = MovieComments.objects.get(Comment_id=Comment_id)
                # .objects.filter(pk=Comment_id)
                # print(comment_edit)
                comment_edit.content = content
                comment_edit.save()

                return HttpResponse('The review has been successfully modified!')
            
            else:
                rating = request.POST.get('rating')
                # print(rating)
                content = request.POST.get('addCommentContBox')
                # print(content)
                # print(user_id)
                # print(movie_id)

                uid_id = User.objects.get(pk=user_id)
                mid_id = Movies.objects.get(pk=movie_id)
                # print('success')
                existing_comment = MovieComments.objects.filter(uid_id=user_id, mid_id=movie_id).exists()
                if existing_comment:
                    return HttpResponseRedirect(f'movie?m_id={movie_id}') #這個要處理一下
                time = timezone.now()

                review = MovieComments(score=rating, content=content, mid=mid_id, time=time, uid=uid_id)
                review.save()

                return HttpResponseRedirect(f'movie?m_id={movie_id}')
            

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.id, User.username, User.img, MovieComments.*
            FROM User
            JOIN MovieComments ON User.id = MovieComments .uid_id
            WHERE MovieComments.mid_id =%s
            ORDER BY MovieComments.time DESC
        """, [movie_id])
        commentResults = dictfetchall(cursor)
        reserve_list_comment.append(commentResults)

    
    if commentResults:
        total_score = sum(comment['score'] for comment in commentResults)
        avg_score = total_score / len(commentResults)
        avg_score = round(avg_score, 1)
    else:
        avg_score = 0

    # print(f'avg_score: {avg_score}')

    # return render(request, "movie.html", {'reserve_list': reserve_list, 'film': processed_movie_data, 'reserve_list_comment': reserve_list_comment})
    return render(request, "movie.html", {'reserve_list': reserve_list, 'film': processed_movie_data, 'reserve_list_comment': reserve_list_comment, 'user_has_favorite': user_has_favorite, 'user_has_commented': user_has_commented, 'avg_score': avg_score})

    # return render(request, "movie.html", {'reserve_list': reserve_list, 'film': processed_movie_data, 'reserve_list_comment': reserve_list_comment, 'user_has_commented': user_has_commented})
    # print(request.GET)
    # print('below is mid')
    # print(movie_id)
    
    # movie_id = request.GET.get('m_id') 

    # if movie_id:
    #     if request.user.is_authenticated:
    #         user_id = request.user.id
    #         if user_id:
    #             user = User.objects.get(pk=user_id)
    #             # print(f'{user}')
    #             film = Movies.objects.get(pk=movie_id)
    #             browse_time = timezone.now()
    #             browse = Browse(uid=user, mid=film, browseTime=browse_time)
    #             browse.save()
    #             # print("Browse entry saved successfully!")

    # return render(request, "movie.html", {'reserve_list': reserve_list, 'film': processed_movie_data, 'reserve_list_comment': reserve_list_comment})