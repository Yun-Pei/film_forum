# from member.models import Movies
# from .models import TrieTree
# from .utils import Trie
# from django.shortcuts import render
# import time


# def save_trie_to_db(trie, name):
#     serialized_trie = trie.serialize()
#     TrieTree.objects.update_or_create(
#         movie_name=name,
#         defaults={'data': serialized_trie}
#     )

# def load_trie_from_db(name):
#     try:
#         trie_record = TrieTree.objects.get(movie_name=name)
#         return Trie.deserialize(trie_record.data)
#     except TrieTree.DoesNotExist:
#         return None

# def search_trie(request):
#     trie_name = "movies_trie"
#     trie = load_trie_from_db(trie_name)
#     if not trie:
#         trie = Trie()
#         movies = Movies.objects.filter(mid__lt=100)  #目前暫時用id <= 100
#         for movie in movies:
#             trie.insert(movie.name, movie.mid)
#         save_trie_to_db(trie, trie_name)
    
#     prefix = request.GET.get('term', '').strip()
    
#     # 防止沒有任何輸入依舊會search data
#     if not prefix:
#         return render(request, 'search_tree.html')
    
#     movie_names = trie.search(prefix)
#     data = [{'label': movie['name'], 'value': movie['name'], 'url': str(movie['mid'])} for movie in movie_names]
#     print(data)
#     #     data = [{'label': movie.name, 'value': movie.name, 'url': str(movie.mid) } for movie in movies]
#     #     return JsonResponse(data, safe=False)
#     return render(request, 'search_tree.html', {'movie_names': data})

# # Create your views here.
# # def search_trie(request):
# #     class TrieNode:
# #         def __init__(self):
# #             self.children = {}
# #             self.is_end_of_word = False

# #     class Trie:
# #         def __init__(self):
# #             self.root = TrieNode()

# #         def insert(self, word):
# #             node = self.root
# #             for char in word:
# #                 if char not in node.children:
# #                     node.children[char] = TrieNode()
# #                 node = node.children[char]
# #             node.is_end_of_word = True

# #         def search(self, prefix):
# #             node = self.root
# #             for char in prefix:
# #                 if char not in node.children:
# #                     return []
# #                 node = node.children[char]
# #             return self._get_all(node, prefix)

# #         def _get_all(self, node, prefix):
# #             results = []
# #             if node.is_end_of_word:
# #                 results.append(prefix)
# #             for char, child_node in node.children.items():
# #                 results.extend(self._get_all(child_node, prefix + char))
# #             return results

# #     trie = Trie()

# #     # 從Django模型中讀取所有的電影名稱
# #     movies = Movies.objects.filter(mid__lt = 100)
# #     # movies = Movies.objects.all()
    

# #     for movie in movies:
# #         trie.insert(movie.name)  # 假設你的電影模型有一個名為name的字段

# #     # 現在你可以使用trie.search方法來進行自動完成搜索
    
# #     movie_names = trie.search("A")
# #     print(movie_names)  # 印出所有以""開頭的電影名稱

# #     # start_time = time.time()
# #     # movie_names = trie.search("Ab")
# #     # end_time = time.time()
# #     # search_time = (end_time - start_time) * 1000  # convert to milliseconds
# #     # print(f"Search time: {search_time} milliseconds")
# #     # print(movie_names)



# #     return render(request, 'search_tree.html', {'movie_names': movie_names})