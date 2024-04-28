from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
# from .forms import ForumsForm
from member.models import *
# from forum.models import Forums, ForumsMessage
# from .forms import MessageForm

# Create your views here.
# @csrf_exempt
def forum(request):
    # if request.method == "POST":
    forum_articles = Article.objects.filter().order_by("-time").values('uid', 'mid', 'art_id', 'time', 'conent', 'title')
    
    print(forum_articles)
    return render(request, "forum.html", {'forum_article': forum_articles})
    
# @csrf_exempt
# def forum_article(request):
#     forum_articles = None
#     forum_message = None
#     form = MessageForm()

#     movie_id = request.GET.get('m_id')
#     ur_id = request.GET.get('user_id')
#     forum_id = request.GET.get('f_id')
#     # print(movie_id)


#     forum_articles = Forums.objects.filter(f_id=forum_id).values('f_id', 'm_id', 'time', 'title', 'content', 'user_id')
#     forum_message = ForumsMessage.objects.filter().order_by("-time").values('f_id', 'm_id', 'time', 'message_content')

 
#     if request.method == 'POST':
#         form = MessageForm(request.POST)

#         if form.is_valid():

#             message_content = form.cleaned_data['message_content']
#             print(message_content)

#             forum_instance2 = Forums.objects.get(pk=forum_id, m_id=movie_id)
#             m_id = forum_instance2.m_id
            
#             forum_instance = Forums.objects.get(pk=forum_id)
#             f_id = forum_instance


#             time = timezone.now()
#             # print(now_time)

#             forum = ForumsMessage(f_id=f_id, message_content=message_content, m_id=m_id, time=time)
#             forum.save()


#             return HttpResponseRedirect(f'forum_article?m_id={movie_id}&user_id={ur_id}&f_id={forum_id}')

        
#         # edit forum article
#         elif request.POST.get("mode") == "forum_article_edit":

#             time = Forums.objects.filter(f_id=forum_id).values('time')

#             edit_article = Forums(f_id=forum_id, m_id=movie_id, title=request.POST.get('title'), content=request.POST.get('content'), user_id=ur_id, time=time)
#             edit_article.save()

#             return HttpResponse('The article has been successfully modified!')

#         # delete forum article
#         elif request.POST.get("mode") == "forum_article_delete":
#             delete_article = Forums.objects.get(f_id=forum_id)
#             delete_article.delete()

#             return HttpResponse('The article has been successfully deleted!')
            

#     return render(request, "forum_article.html", {'forum_article': forum_articles, 'form': form, 'forum_message': forum_message})
