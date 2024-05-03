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
    if request.method == "GET":
        return render(request, 'addChatPage.html')
    elif request.method == "POST":
        print(request.POST.get("uid_id"))
        print(request.POST.get("be_uid"))
        return HttpResponse("success")

class MemberSearchView(ListView):
    model = User
    template_name = 'addChatPage.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            queryset = User.objects.filter(username__icontains=query)
            if self.request.user.is_authenticated:
                queryset = queryset.exclude(id=self.request.user.id)
            return queryset
        return User.objects.none()

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