from django.shortcuts import render
from django.http import JsonResponse
from member.models import Movies
import time
from test import result
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
import random
from django.db import connection
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

def generate_user_item_matrix():
    browse_data = Browse.objects.all().values('uid_id', 'mid_id', 'browseTime')

    df = pd.DataFrame(list(browse_data))

    df['rating'] = 1

    user_item_matrix = df.pivot_table(index='uid_id', columns='mid_id', values='rating', fill_value=0)

    user_item_matrix.index.name = 'userId'
    user_item_matrix.columns.name = 'movieId'
    
    return user_item_matrix

def train_knn_model(user_item_matrix, n_neighbors=10):
    # 定義使用餘弦相似度的 KNN 模型
    cf_knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=n_neighbors, n_jobs=-1)
    
    # 擬合模型
    cf_knn_model.fit(user_item_matrix)
    
    return cf_knn_model

# 呼叫這個函數來生成 user_item_matrix
matrix = generate_user_item_matrix()
# print(matrix)
# print('aaa')


def movie_recommender_engine(movie_id, matrix, cf_model, n_recs):
    
    if movie_id not in matrix.columns:
        raise KeyError(f"Movie ID {movie_id} not found in the matrix.")
    
    #改成從電影找推薦，因為我要從用戶最近的瀏覽找出要輸入的電影，如果是直接用用戶找也可以，同樣方法不同寫法，但就不用轉置
    matrix_T = matrix.T
    
    cf_model.fit(matrix_T)
    
    distances, indices = cf_model.kneighbors(matrix_T.loc[movie_id].values.reshape(1, -1), n_neighbors=n_recs+1)
    movie_rec_ids = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[1:]
    
    cf_recs = []
    for i in movie_rec_ids:
        cf_recs.append({'MovieID': matrix_T.index[i[0]], 'Distance': i[1]})
    
    df = pd.DataFrame(cf_recs, index=range(1, n_recs + 1))
    
    return df

def get_latest_browsed_movie(user_id):
    latest_browse = Browse.objects.filter(uid_id=user_id).order_by('-browseTime').first()
    if latest_browse:
        return latest_browse.mid_id
    return None

def testPage(request):
    movies1 = get_top_ten_movies()

    global result
    movies2 = get_top_ten_movies_by_avg_score()

    if request.GET.get("term"):
        term = request.GET.get('term')
        start_time = time.time()
        # with connection.cursor() as cursor:
        #     sql = f"select name, mid from Movies where name like \'{term}%\';"

        #     cursor.execute(sql)
        #     movies = cursor.fetchall()
        movies = result.search(term)

        
        end_time = time.time()

        search_time = (end_time - start_time)
        # print(start_time, end_time)
        print(f"Orignal search time need {search_time} milliseconds")

        data = [{'label': movie[0], 'value': movie[0], 'url': str(movie[1]) } for movie in movies]
        return JsonResponse(data, safe=False)

    # below is algorithm
    user_item_matrix = generate_user_item_matrix()
    
    # 訓練 KNN 模型
    knn_model = train_knn_model(user_item_matrix)

    user_id = request.user.id
    if user_id:
        latest_movie_id = get_latest_browsed_movie(user_id)
    else:
        random_movie = random.choice(Browse.objects.values_list('mid_id', flat=True))
        latest_movie_id = random_movie

    recommended_movies_list = []
    # print(f"Latest movie ID for user {user_id}: {latest_movie_id}")
    
    recommended_movies = movie_recommender_engine(movie_id=latest_movie_id, matrix=user_item_matrix, cf_model=knn_model, n_recs=10)
    recommended_movies_list = Movies.objects.filter(mid__in=recommended_movies['MovieID'])

    return render(request, "index.html", {'movies1': movies1, 'movies2': movies2, 'moviesalgo': recommended_movies_list})



