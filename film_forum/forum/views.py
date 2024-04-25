from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
# from .forms import ForumsForm
from .models import *
from forum.models import Forums, ForumsMessage
from .forms import MessageForm

# Create your views here.
@csrf_exempt
def forum(request):
    # if request.method == "POST":
    forum_articles = Forums.objects.filter().order_by("-time").values('f_id', 'm_id', 'time', 'title', 'content', 'user_id')

    return render(request, "forum.html", {'forum_article': forum_articles})
    
@csrf_exempt
def forum_article(request):
    # if request.method == "POST":
    forum_articles = Forums.objects.filter(f_id=10).order_by("-time").values('f_id', 'm_id', 'time', 'title', 'content', 'user_id')


    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message_content = form.cleaned_data['message_content']
            print(message_content)

            forum_instance = Forums.objects.get(pk=10)
            m_id = forum_instance
            
            forum_instance = Forums.objects.get(pk=10)

            # ValueError: Cannot assign "10": "ForumsMessage.f_id" must be a "Forums" instance.
            f_id = forum_instance

            # print(film_id)

            time = timezone.now()
            # print(now_time)

            forum = ForumsMessage(f_id=f_id, message_content=message_content, m_id=m_id, time=time)
            forum.save()


            return redirect('forum_article')  # 導入路徑
        # jsut test
        else:
            return redirect('forum')

    return render(request, "forum_article.html", {'forum_article': forum_articles, 'form': form})