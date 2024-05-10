from django.shortcuts import render
from django.http import JsonResponse
from member.models import Movies
from member.models import User
from member.models import Browse
from django.utils import timezone
from django.db.models import Count
from django.db import connection
from itertools import permutations
import pandas as pd
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

def testPage(request):

    movies2 = Movies.objects.filter(year__gt=2019)[:10]
    movies3 = Movies.objects.filter(year__gt=2019)[:10]
    movieup = Movies.objects.filter(mid=89)

    # top_movies = Browse.objects.values('mid').annotate(num_views=Count('mid')).order_by('num_views')[:10]
    movies1 = get_top_ten_movies()

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

    # def create_pairs(Browse):
    #     pairs = permutations(mid.values, 2) # 從所有的物品裡面隨機不放回抽取 2 個物品
    #     pairs = list(pairs) # 可以直接和上面的程式碼整合在一起，但因為這裡的 permutation 實際上是疊代器，因此需要使用 list 來實例化
    #     pairs = pd.DataFrame(pairs, columns=["movie_A", "movie_B"])
    #     return pairs

    # # 將資料進行轉換
    # book_pairs = books_record.groupby('UserId')['Book_title'].apply(create_pairs)

    # # 因為以 Groupby 來聚合資料後，index 就會變成 UserId，因此為了要直接刪除掉故使用 reset_index(drop=True)
    # book_pairs = book_pairs.reset_index(drop=True)

    # # 計算 items_A 對應到 items_B 的個別總數
    # pair_counts = book_pairs.groupby(['book_a', 'book_b']).size()  # size() 和 count() 的差異在於 size 會將 NaN 計算進去。

    # # 將原先計算出來的欄位命名為 Size，並重置 index
    # pair_counts = pair_counts.to_frame(name = 'size').reset_index() 

    # # 根據 size 從大到小進行排序
    # pair_counts_sorted = pair_counts_df.sort_values('size', ascending=False)
    #above is algorithn    

    return render(request, "index.html", {'movies1': movies1, 'movies2': movies2, 'movies3': movies3, 'movieup': movieup[0]}) 





