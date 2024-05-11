from django.shortcuts import render
from django.http import JsonResponse
from member.models import Movies
from member.models import User
from member.models import Browse
from member.models import MovieComments
from django.utils import timezone
from django.db.models import Count
from django.db import connection
from itertools import permutations
import pandas as pd
from django.db.models import Avg
# from movie.models import 
#新加入的function

def get_top_ten_movies():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT mid_id, COUNT(mid_id) AS num_views
            FROM Browse
            GROUP BY mid_id
            ORDER BY num_views DESC
            LIMIT 10;
        """)
        top_movies = cursor.fetchall()
    
    top_movie_ids = [entry[0] for entry in top_movies]
    top_movies_objects = Movies.objects.filter(mid__in=top_movie_ids)
    
    return top_movies_objects

def get_top_ten_movies_by_avg_score():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.mid, AVG(mc.score) AS avg_score
            FROM Movies m
            INNER JOIN MovieComments mc ON m.mid = mc.mid_id
            GROUP BY m.mid
            ORDER BY avg_score DESC
            LIMIT 10;
        """)
        top_movies = cursor.fetchall()

    top_movie_ids = [entry[0] for entry in top_movies]
    top_movies_objects = Movies.objects.filter(mid__in=top_movie_ids)
    return top_movies_objects

def create_pairs(movies):
    movie_ids = [movie.mid for movie in movies]  # 提取每部電影的mid屬性
    pairs = permutations(movie_ids, 2)  # 使用電影ID的排列
    pairs = list(pairs)
    pairs = pd.DataFrame(pairs, columns=["movie_A", "movie_B"])
    return pairs

def testPage(request):

    movieup = Movies.objects.filter(mid=89)

    # top_movies = Browse.objects.values('mid').annotate(num_views=Count('mid')).order_by('num_views')[:10]
    movies1 = get_top_ten_movies()

    movies2 = get_top_ten_movies_by_avg_score()
    
    # for entry in top_movies:
    #     movie_id = entry[0]
    #     num_views = entry[1]
    #     movie = Movies.objects.get(mid=movie_id)
    #     print(f"Movie: {movie.mid} - Views: {num_views}")

    # for movie_id in top_movie_ids:
    #     print(movie_id)

    if request.GET.get("term"):
        term = request.GET.get('term')
        movies = Movies.objects.filter(name__icontains=term)[:20]
        
        data = [{'label': movie.name, 'value': movie.name, 'url': str(movie.mid) } for movie in movies]
        return JsonResponse(data, safe=False)
    

    # below is algorithm

    browses = Browse.objects.all()

    user_movies = {}
    for browse in browses:
        user_id = browse.uid.id
        movie_id = browse.mid.mid
        if user_id in user_movies:
            user_movies[user_id].append(movie_id)
        else:
            user_movies[user_id] = [movie_id]

    all_pairs = []
    for user_id, movies in user_movies.items():
        pairs = permutations(movies, 2)
        all_pairs.extend(pairs)

    pair_counts = pd.Series(all_pairs).value_counts()

    top_10_pairs = pair_counts.head(10)

    top_10_movie_objects = []
    for pair, count in top_10_pairs.items():
        movie_A = Movies.objects.get(mid=pair[0])
        movie_B = Movies.objects.get(mid=pair[1])
        top_10_movie_objects.append((movie_A, movie_B, count))

    print(top_10_movie_objects)

    return render(request, "index.html", {'movies1': movies1, 'movies2': movies2, 'moviesalgo': top_10_movie_objects, 'movieup': movieup[0]}) 





