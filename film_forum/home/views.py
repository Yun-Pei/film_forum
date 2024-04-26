from django.shortcuts import render
from django.http import JsonResponse
from member.models import Movies
# from movie.models import 
#新加入的function
def testPage(request):
    movies1 = Movies.objects.filter(year__gt=2019)[:10]
    movies2 = Movies.objects.filter(year__gt=2020)[:4]
    movies3 = Movies.objects.filter(year__gt=2020)[:4]
    movieup = Movies.objects.filter(id=89)
    print(len(movies1))
    len(movies1)
    return render(request, "index.html", {'movies1': movies1, 'movies2': movies2, 'movies3': movies3, 'movieup': movieup[0]}) 

def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Blog.objects.all().filter(title=search)
        return render(request, 'searchbar.html', {'post':post})
    

def load_more_videos(request):
    current_count = int(request.GET.get('current_count', 0))
    count_per_load = 4
    videos = Movies.objects.all()[current_count:current_count + count_per_load]
    video_data = [{'title': video.title, 'cover_image': video.cover_image.url, 'url': video.url} for video in videos]
    return JsonResponse({'videos': video_data})

