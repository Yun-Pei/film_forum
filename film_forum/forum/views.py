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

# Create your views here.
# @csrf_exempt
def forum(request):

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT User.id, User.username, Article.*
            FROM User
            JOIN Article ON User.id = Article .uid_id
        """)
        results = cursor.fetchall()
        # results = [col[0] for col in cursor.description]
        # ['id', 'username', 'art_id', 'time', 'title', 'conent', 'uid_id', 'mid_id']

    # print(results)

        # results = []

        # for row in rows:
        #     user = User.objects.get(pk=row[0])  # 第一列是 User 的 id
        #     article = Article.objects.get(pk=row[3])  # 第四列是 Article 的 id
        #     results.append((user, article))

    previous_url = request.META.get('HTTP_REFERER', '/')
    request.session['previous_url'] = previous_url

    form = ForumsForm()

    movie_id = request.GET.get('m_id')

    forum_articles = Article.objects.filter(mid=72).order_by("-time").values('uid', 'mid', 'art_id', 'time', 'conent', 'title')

        # 拿會員ID
    if request.user.is_authenticated:
        user_id = request.user.id
        print(user_id)

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

    # print(forum_articles)
    return render(request, "forum.html", {'form': form, 'forum_article': forum_articles, 'results':results})
    
@csrf_exempt
def forum_article(request):

    # 拿會員ID
    if request.user.is_authenticated:
        user_id = request.user.id
        # print(user_id)

    articles = None
    articlecomment = None
    form = MessageForm()

    movie_id = request.GET.get('m_id')
    article_id = request.GET.get('art_id')
    # print(movie_id)
    # print(article_id)

    articles = Article.objects.filter(art_id=article_id).values('uid', 'mid', 'art_id', 'time', 'conent', 'title')
    articlecomment = ArticleComment.objects.filter(art_id=article_id).order_by("-time").values('uid', 'mid', 'art_id', 'time', 'conent')

 
    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():

            conent = form.cleaned_data['conent']
            # print(conent)

            film_id = Movies.objects.get(pk=movie_id)
            user_id = User.objects.get(pk=user_id)
            art_id = Article.objects.get(pk=article_id)
            # # print(film_id)

            time = timezone.now()
            # print(now_time)

            forum = ArticleComment(art_id=art_id, conent=conent, mid=film_id, time=time, uid=user_id)
            forum.save()


            return HttpResponseRedirect(f'forum_article?m_id={movie_id}&art_id={article_id}')

        
        # edit forum article
        elif request.POST.get("mode") == "forum_article_edit":

            movie_id = request.POST.get('m_id')
            article_id = request.POST.get('art_id')

            time = Article.objects.filter(art_id=article_id).values('time')

            # print(time)
            user_id = User.objects.get(pk=user_id)
            film_id = Movies.objects.get(pk=movie_id)

            # art_id = Article.objects.get(pk=article_id)


            edit_article = Article(art_id=article_id, mid=film_id, title=request.POST.get('title'), conent=request.POST.get('content'), uid=user_id, time=time)
            edit_article.save()

            return HttpResponse('The article has been successfully modified!')

        # delete forum article
        elif request.POST.get("mode") == "forum_article_delete":
            article_id = request.POST.get('art_id')

            delete_article = Article.objects.get(art_id=article_id)
            delete_article.delete()

            return redirect("forum")
            
# 'form': form, 
    return render(request, "forum_article.html", {'articles': articles,'form': form,  'articlecomment': articlecomment})
