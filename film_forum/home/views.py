from django.shortcuts import render
from django.http import JsonResponse
from member.models import Movies
from member.models import User
from member.models import Browse
from django.utils import timezone
from django.db.models import Count
# from movie.models import 
#新加入的function
def testPage(request):

    movies1 = Movies.objects.filter(year__gt=2019)[:10]
    movies2 = Movies.objects.filter(year__gt=2019)[:10]
    movies3 = Movies.objects.filter(year__gt=2019)[:10]
    movieup = Movies.objects.filter(mid=89)

    # top_movies = Browse.objects.values('mid').annotate(num_views=Count('mid')).order_by('-num_views')[:10]
    # top_movie_ids = [entry['mid'] for entry in top_movies]
    # movies1 = Movies.objects.filter(mid__in=top_movie_ids)
    
    if request.GET.get("term"):
        term = request.GET.get('term')
        movies = Movies.objects.filter(name__icontains=term)[:20]
        
        data = [{'label': movie.name, 'value': movie.name, 'url': str(movie.mid) } for movie in movies]
        return JsonResponse(data, safe=False)
    
    print(request.GET)
    movie_id = request.GET.get('m_id') 
    print('below is mid')
    print(movie_id)
    
    if movie_id:

        if request.user.is_authenticated:
            user_id = request.user.id
            try:
                user = User.objects.get(pk=user_id)
                film = Movies.objects.get(pk=movie_id)
                browse_time = timezone.now()
                browse = Browse(uid=user, mid=film, browseTime=browse_time)
                browse.save()
                print("Browse entry saved successfully!")
            except User.DoesNotExist:
                print("User does not exist")
            except Movies.DoesNotExist:
                print("Movie does not exist")
            except Exception as e:
                print(f"An error occurred while saving browse entry: {e}")
        
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

