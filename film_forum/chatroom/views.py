from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from member.models import *
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
#新加入的function
def testPage(request):
    return render(request, "chatroom.html")

def chatPage(request):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chatPage.html", context)

def addChatPage(request):
        
    return render(request, 'addChatPage.html')
    

def search_member(request):
    query = request.POST.get('q')
    members = []
    if query and request.user.is_authenticated:
        user_id = request.user.id
        try:
            # 使用exact查詢條件來完全匹配使用者名稱
            member = User.objects.get(username=query)
            if user_id != member.id:
                members.append(member)
        except User.DoesNotExist:
            pass  # 如果沒有找到相應的使用者，就不添加到結果列表中
    return render(request, 'addChatPage.html', {'members': members})

# class MemberSearchView(ListView):
#     model = User
#     template_name = 'addChatPage.html'
#     context_object_name = 'users'

#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         if query:
#             queryset = User.objects.filter(username__icontains=query)
#             if self.request.user.is_authenticated:
#                 queryset = queryset.exclude(id=self.request.user.id)
#             return queryset
#         return User.objects.none()

# def autocomplete(request):
#     if 'term' in request.GET:
#         qs = User.objects.filter(username__istartwith=request.GET('term'))
#         usernames = list()
#         for user in qs:
#             usernames.append(User.username)
#     return JsonResponse(usernames, safe=False)

# def search_members(request):
#     query = request.GET.get("q")
#     if query:
#         return User.objects.filter(username__icontains=query)
#     return render(request, 'addChatPage.html')