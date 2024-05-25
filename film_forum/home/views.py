from django.shortcuts import render
from django.http import JsonResponse
from member.models import Movies
import time
from test import result
# from movie.models import 
#新加入的function
def testPage(request):

    movies1 = Movies.objects.filter(year__gt=2019)[:10]
    movies2 = Movies.objects.filter(year__gt=2019)[:10]
    movies3 = Movies.objects.filter(year__gt=2019)[:10]
    movieup = Movies.objects.filter(mid=89)

    global result
    # print(result.search('abc'))

    if request.GET.get("term"):
        term = request.GET.get('term')
        movies = result.search(term)

        data = [{'label': movie[0], 'value': movie[0], 'url': str(movie[1]) } for movie in movies]
        return JsonResponse(data, safe=False)

        
    # if request.GET.get("term"):
    #     # Before search
    #     start_time = time.time()

    #     term = request.GET.get('term')

    #     movies = Movies.objects.filter(name__icontains=term)[:20]
        

    #     # After search
    #     end_time = time.time()

    #     search_time = (end_time - start_time)
    #     # print(f"start {start_time} seconds")
    #     # print(f"end {end_time} seconds")
    #     print(f"Orignal search time need {search_time} milliseconds")
        
    #     data = [{'label': movie.name, 'value': movie.name, 'url': str(movie.mid) } for movie in movies]
    #     return JsonResponse(data, safe=False)
    
    return render(request, "index.html", {'movies1': movies1, 'movies2': movies2, 'movies3': movies3, 'movieup': movieup[0]}) 



# def searchbar(request):
#     if request.method == 'GET':
#         search = request.GET.get('search')
#         post = Blog.objects.all().filter(title=search)
#         return render(request, 'searchbar.html', {'post':post})
    

# def load_more_videos(request):
#     current_count = int(request.GET.get('current_count', 0))
#     count_per_load = 4
#     videos = Movies.objects.all()[current_count:current_count + count_per_load]
#     video_data = [{'title': video.title, 'cover_image': video.cover_image.url, 'url': video.url} for video in videos]
#     return JsonResponse({'videos': video_data})

