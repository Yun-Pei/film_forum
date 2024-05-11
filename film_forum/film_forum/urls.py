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
# from django.contrib.auth.views import 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_views.testPage, name="home"),  #"": 代表runserver後給的路徑，會直接導入到home這個page(羅做的主頁)
    # 給一個name之後在不同分頁的bar中若有要連回主頁的功能可以直接url 回home的主頁
    path('forum', forum_views.forum, name="forum"),
    path('movie', movie_views.movie, name="movie"),
    path('register', member_views.register, name="register"),
    path('forum_article', forum_views.forum_article, name="forum_article"),
    path('login', member_views.login, name="login"),
    path('log_out', member_views.log_out, name="log_out"),
    # path('crawl', member_views.crawl, name="crawl"),
    # path("", views.index, name="home")
    # path('searchbar/', home_views.searchbar, name='searchbar'),
    # path('load-more-videos/', home_views.load_more_videos, name='load_more_videos'),
]
