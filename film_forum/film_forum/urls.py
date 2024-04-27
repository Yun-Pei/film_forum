"""
URL configuration for film_forum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views as home_views
from member import views as member_views
from forum import views as forum_views
from movie import views as movie_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_views.testPage, name="home"),  #"": 代表runserver後給的路徑，會直接導入到home這個page(羅做的主頁)
    path('forum', forum_views.forum, name="forum"),
    path('movie', movie_views.movie, name="movie"),
    path('forum_article', forum_views.forum_article, name="forum_article"),
    path("chat", include('chatroom.urls')) #給剛剛寫好的function設定一個url
]
