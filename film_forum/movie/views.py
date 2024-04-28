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
    film = Movies.objects.filter(mid=72).values_list("mid", "rid", "name", "year", "rating", "time", "age", "introduction", "img", "director", "star", "tag")
    forum_article = Article.objects.filter().order_by("-time").values('uid', 'mid', 'art_id', 'time', 'conent', 'title')

    # for article in forum_article:
    #     article.formatted_time = article.time.strftime("%Y-%m-%d %I:%M %p")

    print(forum_article)

    form = ForumsForm()

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
            film_id = Movies.objects.get(pk=72)
            user_id = User.objects.get(pk=user_id)
            # # print(film_id)

            now_time = timezone.now()
            # # print(now_time)

            forum = Article(title=title, conent=conent, time=now_time, uid=user_id, mid=film_id)
            forum.save()

            # film = None

            return redirect('movie')  # 導入路徑
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        # jsut test
        # else:
        #     return redirect('forum')
    # else:
    #     form = ForumsForm()

    return render(request, "movie.html", {'form': form, 'forum_article': forum_article, 'film': film})