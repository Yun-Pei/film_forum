from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
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
    forum_articles = None
    forum_message = None
    form = MessageForm()

    movie_id = None
    ur_id = None
    forum_id = None

    if request.GET.get("mode") == "which_article" or request.method == 'GET' or request.method == 'POST':
        # print("here")
        movie_id = request.GET.get('m_id')
        ur_id = request.GET.get('user_id')
        forum_id = request.GET.get('f_id')

        forum_articles = Forums.objects.filter(f_id=forum_id).values('f_id', 'm_id', 'time', 'title', 'content', 'user_id')
        # print(forum_articles)
        forum_message = ForumsMessage.objects.filter().order_by("-time").values('f_id', 'm_id', 'time', 'message_content')


        if request.method == 'POST':

            if request.POST.get("mode") == "message_post":
                form = MessageForm(request.POST)

                movie_id = request.POST.get('m_id')
                ur_id = request.POST.get('user_id')
                forum_id = request.POST.get('f_id')
                print(movie_id)

                message_content = request.POST.get('the_post')
                print(message_content)

                # m_id = Forums.objects.get(m_id=movie_id)
                #  forum_instance.m_id
                # print(m_id)
                
                forum_instance = Forums.objects.get(pk=forum_id)
                f_id = forum_instance    
                print(f_id)      

                forum_instance2 = Forums.objects.get(pk=forum_id, m_id=movie_id)
                m_id = forum_instance2
                

                # m_id = get_object_or_404(Forums, pk=forum_id)
                print(m_id)

                time = timezone.now()

                forum = ForumsMessage(f_id=f_id, message_content=message_content, m_id=m_id.m_id, time=time)
                forum.save()  

                return redirect('forum_article')

            # print("here")
            # if form.is_valid():
            #     # f_id_list = list(forum_articles.values_list('f_id', flat=True))
            #     # print(f_id_value)

            #     message_content = form.cleaned_data['message_content']
            #     forum_id = form.cleaned_data['f_id']
            #     movie_id = form.cleaned_data['m_id']
            #     print(forum_id)
            #     print(movie_id)

            #     forum_instance = Forums.objects.get(pk=movie_id)
            #     m_id = forum_instance
                
            #     forum_instance = Forums.objects.get(pk=forum_id)

            #     # ValueError: Cannot assign "10": "ForumsMessage.f_id" must be a "Forums" instance.
            #     f_id = forum_instance

            #     # print(film_id)

            #     time = timezone.now()
            #     # print(now_time)

            #     forum = ForumsMessage(f_id=f_id, message_content=message_content, m_id=m_id, time=time)
            #     forum.save()


            #     return redirect('forum_article')  # 導入路徑

            
            # edit forum article
            elif request.POST.get("mode") == "forum_article_edit":
                movie_id = request.POST.get('m_id')
                ur_id = request.POST.get('user_id')
                forum_id = request.POST.get('f_id')

                time = Forums.objects.filter(f_id=forum_id).values('time')

                edit_article = Forums(f_id=forum_id, m_id=movie_id, title=request.POST.get('title'), content=request.POST.get('content'), user_id=ur_id, time=time)
                edit_article.save()

                return HttpResponse('The article has been successfully modified!')

            # delete forum article
            elif request.POST.get("mode") == "forum_article_delete":
                movie_id = request.POST.get('m_id')
                ur_id = request.POST.get('user_id')
                forum_id = request.POST.get('f_id')

                delete_article = Forums.objects.get(f_id=forum_id)
                delete_article.delete()

                return HttpResponse('The article has been successfully deleted!')
            

        return render(request, "forum_article.html", {'forum_article': forum_articles, 'form': form, 'forum_message': forum_message})