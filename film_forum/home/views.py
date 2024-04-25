from django.shortcuts import render
from django.http import JsonResponse
from .models import Video
#新加入的function
def testPage(request):
    return render(request, "index.html")

def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Blog.objects.all().filter(title=search)
        return render(request, 'searchbar.html', {'post':post})
    

def load_more_videos(request):
    current_count = int(request.GET.get('current_count', 0))
    count_per_load = 4
    videos = Video.objects.all()[current_count:current_count + count_per_load]
    video_data = [{'title': video.title, 'cover_image': video.cover_image.url, 'url': video.url} for video in videos]
    return JsonResponse({'videos': video_data})

def home(request):
    
    videos1 = Video.objects.filter(category='category')[:4]
    videos2 = Video.objects.filter(category='category')[:4]
    videos3 = Video.objects.filter(category='category')[:4]
    
    return render(request, 'home.html', {'videos1': videos1, 'videos2': videos2, 'videos3': videos3})