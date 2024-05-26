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
    rating_data = MovieComments.objects.all().values('uid_id', 'mid_id', 'score')

    df = pd.DataFrame(list(rating_data))

    user_item_matrix = df.pivot_table(index='uid_id', columns='mid_id', values='score', fill_value=0)

    user_item_matrix.index.name = 'userId'
    user_item_matrix.columns.name = 'movieId'
    
    return user_item_matrix

matrix= generate_user_item_matrix();
# print(matrix)

def train_knn_model(user_item_matrix, n_neighbors=10):
    # 定義使用餘弦相似度的 KNN 模型
    cf_knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=n_neighbors, n_jobs=-1)
    
    # 擬合模型
    cf_knn_model.fit(user_item_matrix)
    
    return cf_knn_model

def user_recommender_engine(user_id, matrix, cf_model, n_recs):
    if user_id not in matrix.index:
        raise KeyError(f"User ID {user_id} not found in the matrix.")
    # print(f"User ID {user_id} found in the matrix.")
    distances, indices = cf_model.kneighbors(matrix.loc[user_id].values.reshape(1, -1), n_neighbors=n_recs+1)
    similar_user_ids = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[1:]
    
    similar_user_ids = [matrix.index[i[0]] for i in similar_user_ids]
    print(similar_user_ids)
    movie_scores = {}
    for similar_user_id in similar_user_ids:
        similar_user_ratings = matrix.loc[similar_user_id]
        # print(f"Ratings from similar user {similar_user_id}: {similar_user_ratings}")
        for movie_id, score in similar_user_ratings.items():
            # print(f"Checking movie {movie_id} with score {score} for similar user {similar_user_id}")
            a=matrix.loc[user_id].index
            # print(a)
            if score > 0 :
                if movie_id not in movie_scores:
                    movie_scores[movie_id] = []
                movie_scores[movie_id].append(score)
    # print("Movie scores:", movie_scores)
    recommended_movies = sorted(movie_scores.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True)[:n_recs]
    recommended_movie_ids = [movie_id for movie_id, scores in recommended_movies]
    
    return recommended_movie_ids

# def get_latest_browsed_movie(user_id):
#     latest_browse = Browse.objects.filter(uid_id=user_id).order_by('-browseTime').first()
#     if latest_browse:
#         return latest_browse.mid_id
#     return None

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
        print(f"TrieTree search time need {search_time} milliseconds")

        data = [{'label': movie[0], 'value': movie[0], 'url': str(movie[1]) } for movie in movies]
        return JsonResponse(data, safe=False)

    # below is algorithm
    user_item_matrix = generate_user_item_matrix()
    
    # 訓練 KNN 模型
    knn_model = train_knn_model(user_item_matrix)

    user_id = request.user.id
    
    if user_id:
        if user_id not in user_item_matrix.index:
            user_id = user_item_matrix.index[0]
    else:
        random_user = random.choice(MovieComments.objects.values_list('uid_id', flat=True))
        user_id = random_user

    # print(f"User ID {user_id}")
    # print(f'{latest_movie_id}')
    recommended_movies_list = []
    # print(f"Latest movie ID for user {user_id}: {latest_movie_id}")
    
    recommended_movie_ids = user_recommender_engine(user_id=user_id, matrix=user_item_matrix, cf_model=knn_model, n_recs=10)
    recommended_movies_list = Movies.objects.filter(mid__in=recommended_movie_ids)
    # print("Recommended movies list:", recommended_movies_list)
    return render(request, "index.html", {'movies1': movies1, 'movies2': movies2, 'moviesalgo': recommended_movies_list})



