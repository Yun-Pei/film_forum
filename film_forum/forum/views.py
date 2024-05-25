from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import *
from member.models import *
from movie.forms import *
from django.db import connection


# from forum.models import Forums, ForumsMessage
# from .forms import MessageForm


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# @csrf_exempt
def forum(request):

    movie_id = request.GET.get('m_id')
    film = Movies.objects.filter(mid=movie_id).values('name', 'mid')
    print(film)

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

    # print(reserve_list)
    previous_url = request.META.get('HTTP_REFERER', '/')
    request.session['previous_url'] = previous_url

    form = ForumsForm()

    movie_id = request.GET.get('m_id')

    # forum_articles = Article.objects.filter(mid=72).order_by("-time").values('uid', 'mid', 'art_id', 'time', 'conent', 'title')

        # 拿會員ID
    if request.user.is_authenticated:
        user_id = request.user.id
        # print(user_id)

    if request.method == 'POST':
        # print("here")
        form = ForumsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            # print(title)

            conent = form.cleaned_data['conent']
            # print(content)

            # # m_id = form.cleaned_data['m_id']
            film_id = Movies.objects.get(pk=movie_id)
            user_id = User.objects.get(pk=user_id)
            # # print(film_id)

            now_time = timezone.now()
            # # print(now_time)

            forum = Article(title=title, conent=conent, time=now_time, uid=user_id, mid=film_id)
            forum.save()

            # film = None

            return HttpResponseRedirect(f'forum?m_id={movie_id}')  # 導入路徑

    return render(request, "forum.html", {'form': form, 'reserve_list':reserve_list, 'film':film})
    
@csrf_exempt
def forum_article(request):
    previous_url = request.META.get('HTTP_REFERER', '/')
    
    request.session['previous_url'] = previous_url

    # 拿會員ID
    if request.user.is_authenticated:
        user_id = request.user.id
        # print(user_id)

    # articles = None
    # ArticleComments = None
    form = MessageForm()

    movie_id = request.GET.get('m_id')
    article_id = request.GET.get('art_id')
    # print(movie_id)
    # print(article_id)

    reserve_list = list()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.id, User.username, User.img, Article.*, Movies.name
            FROM User
            JOIN Article ON User.id = Article.uid_id
            JOIN Movies ON Article.mid_id = Movies.mid
            WHERE Article.art_id = %s
        """, [article_id])
        results = dictfetchall(cursor)
        reserve_list.append(results)


    # articles = Article.objects.filter(art_id=article_id).values('uid', 'mid', 'art_id', 'time', 'conent', 'title')
    # ArticleComments = ArticleComments.objects.filter(art_id=article_id).order_by("-time").values('uid', 'mid', 'art_id', 'time', 'conent')

    reserve_list_comment = list()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.id, User.username, User.img, ArticleComments.*
            FROM User
            JOIN ArticleComments ON User.id = ArticleComments.uid_id
            WHERE ArticleComments.art_id_id = %s
            ORDER BY ArticleComments.time DESC
        """, [article_id])
        results = dictfetchall(cursor)
        reserve_list_comment.append(results)

 
    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():

            conent = form.cleaned_data['conent']
            print(conent)

            film_id = Movies.objects.get(pk=movie_id)
            user_id = User.objects.get(pk=user_id)
            art_id = Article.objects.get(pk=article_id)
            # print(film_id)

            time = timezone.now()
            # print(now_time)

            forum = ArticleComments(art_id=art_id, conent=conent, mid=film_id, time=time, uid=user_id)
            forum.save()

            # return HttpResponse(status=200)
            return HttpResponseRedirect(f'forum_article?m_id={movie_id}&art_id={article_id}')

        
        # edit forum article
        elif request.POST.get("mode") == "forum_article_edit":

            movie_id = request.POST.get('m_id')
            article_id = request.POST.get('art_id')

            time = Article.objects.filter(art_id=article_id).values('time')

            # print(time)
            user_id = User.objects.get(pk=user_id)
            film_id = Movies.objects.get(pk=movie_id)
            # print(movie_id)
            # print(article_id)

            # art_id = Article.objects.get(pk=article_id)


            edit_article = Article(art_id=article_id, mid=film_id, title=request.POST.get('title'), conent=request.POST.get('content'), uid=user_id, time=time)
            edit_article.save()

            return HttpResponse(status=200)

        # delete forum article
        elif request.POST.get("mode") == "forum_article_delete":
            movie_id = request.POST.get('m_id')
            # print("here")
            # print(request.POST.get('m_id'))
            # print("end")
            article_id = request.POST.get('art_id')

            delete_article = Article.objects.get(art_id=article_id)
            delete_article.delete()

            return HttpResponse(status=200) 
        
        elif request.POST.get("mode") == "forum_message_edit":
            article_id = request.POST.get('art_id')
            movie_id = request.POST.get('m_id')
            acom_id = request.POST.get('acom_id')
            print(acom_id)
            content = request.POST.get('content')
            time = ArticleComments.objects.filter(ac_id=acom_id).values('time')

            user_id = User.objects.get(pk=user_id)
            film_id = Movies.objects.get(pk=movie_id)
            art_id = Article.objects.get(pk=article_id)

            art_edit = ArticleComments.objects.get(pk=acom_id)
            print(art_edit)
            art_edit.conent = content
            art_edit.save()
            print(content)

            return HttpResponse('The comment has been successfully modified!')
        
        elif request.POST.get("mode") == "forum_message_delete":
            ac_id = request.POST.get('ac_id')

            delete_article_comment = ArticleComments.objects.get(ac_id=ac_id)
            delete_article_comment.delete()
            return HttpResponse(status=200)

            
# 'form': form, 
    return render(request, "forum_article.html", {'form': form, 'reserve_list': reserve_list, 'reserve_list_comment': reserve_list_comment})
