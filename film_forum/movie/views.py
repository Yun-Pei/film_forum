from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .forms import ForumsForm
from .models import *
from forum.models import Forums, ForumsMessage
from member.models import Movies
# Create your views here.


@csrf_exempt
def movie(request):
    film = Movies.objects.filter(id=72).values_list("id", "name", "year", "time", "age", "introduction", "img", "director", "star", "type")
    forum_article = Forums.objects.filter().order_by("-time").values('f_id', 'm_id', 'time', 'title', 'content', 'user_id')

    # for article in forum_article:
    #     article.formatted_time = article.time.strftime("%Y-%m-%d %I:%M %p")

    print(forum_article)

    if request.method == "GET":
        # get movie information
        # print(film[0][0])

        # create a Forum
        form = ForumsForm()

    if request.method == 'POST':
        # print("here")
        form = ForumsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            # print(title)

            content = form.cleaned_data['content']
            # print(content)

            # m_id = form.cleaned_data['m_id']
            film_id = Movies.objects.filter(id=72).values_list("id", flat=True).first()
            # print(film_id)

            now_time = timezone.now()
            # print(now_time)

            forum = Forums(title=title, content=content, m_id=film_id, time=now_time)
            forum.save()

            film = None

            return redirect('movie')  # 導入路徑
        # jsut test
        else:
            return redirect('forum')
    # else:
    #     form = ForumsForm()

    return render(request, "movie.html", {'form': form, 'film': film, 'forum_article': forum_article})