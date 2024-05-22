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
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process
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

def create_user_item_matrix():
    # 獲取所有瀏覽數據
    browses = Browse.objects.all().select_related('uid', 'mid')

    # 創建用戶-電影評分字典
    user_movie_dict = {}
    for browse in browses:
        user_id = browse.uid.id
        movie_id = browse.mid.mid
        if user_id not in user_movie_dict:
            user_movie_dict[user_id] = {}
        user_movie_dict[user_id][movie_id] = 1  # 假設瀏覽過的電影評分為1

    # 創建用戶-電影評分矩陣
    user_item_matrix = pd.DataFrame(user_movie_dict).fillna(0).T

    return user_item_matrix

def train_knn_model(user_item_matrix):
    # 定義基於餘弦相似度的 KNN 模型
    cf_knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)

    # 訓練 KNN 模型
    cf_knn_model.fit(user_item_matrix)

    return cf_knn_model

def movie_recommender_engine(movie_name, matrix, cf_model, n_recs):
    # Fit model on matrix
    cf_model.fit(matrix)
    
    # Calculate neighbour distances
    distances, indices = cf_model.kneighbors(matrix[movie_name], n_neighbors=n_recs)
    movie_rec_ids = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
    
    # List to store recommendations
    cf_recs = []
    for i in movie_rec_ids:
        cf_recs.append({'Title': movie_name['title'][i[0]], 'Distance': i[1]})
    
    # Select top number of recommendations needed
    df = pd.DataFrame(cf_recs, index=range(1, n_recs))
    
    return df

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

    # # Retrieve the most recent movie that each user has browsed
    # recent_browses = Browse.objects.order_by('uid', '-browseTime')
    
    # # Extract movie IDs from the recent browses
    # recent_movie_ids = [browse.mid_id for browse in recent_browses]
    
    # # Define user_item_matrix using the recent browses
    # user_item_matrix = pd.DataFrame(0, index=[1], columns=recent_movie_ids)
    # print(user_item_matrix)
    # # Define a KNN model on cosine similarity
    # cf_knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)
    
    # # Call movie_recommender_engine function to get recommendations
    # recommendations = movie_recommender_engine(movie_name=recent_movie_ids[0], matrix=user_item_matrix, cf_model=cf_knn_model, n_recs=10)
    user_item_matrix = create_user_item_matrix()
    cf_knn_model = train_knn_model(user_item_matrix)

    recent_browses = Browse.objects.order_by('uid', '-browseTime').distinct('uid')
    recent_movie_id = recent_browses[0].mid.mid
    recommendations = movie_recommender_engine(recent_movie_id, user_item_matrix, cf_knn_model, n_recs=10)

    recommended_movies = Movies.objects.filter(mid__in=[rec['movie_id'] for rec in recommendations])

    return render(request, "index.html", {'movies1': movies1, 'movies2': movies2, 'moviesalgo': recommended_movies, 'movieup': movieup[0]}) 





