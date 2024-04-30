from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from member.models import *
from django.views.generic import ListView
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

class MemberSearchView(ListView):
    model = User
    template_name = 'addChatPage.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(username__icontains=query)
        return User.objects.none()
 