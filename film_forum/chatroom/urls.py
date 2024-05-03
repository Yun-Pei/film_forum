from django.urls import path, include, reverse_lazy
from chatroom import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import *

urlpatterns = [
    path("", chat_views.chatPage, name="chat-page"),

    # authentication section
    path("auth/login/", LoginView.as_view(template_name="loginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path('auth/addChat/', views.addChatPage, name='add-Chat'),
    path('auth/search/', views.MemberSearchView.as_view(), name='search_members'),
    # path('auth/search/', views.addChatPage, name='autocomplete'),
]