# import os
# import sys

# sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
# os.environ['DJANGO_SETTINGS_MODULE'] = 'film_forum.settings'

# import django
# django.setup()

# # And then import models

# from member.models import Movies


# def search_trie():
#     class TrieNode:
#         def __init__(self):
#             self.children = {}
#             self.is_end_of_word = False

#     class Trie:
#         def __init__(self):
#             self.root = TrieNode()

#         def insert(self, word):
#             node = self.root
#             for char in word:
#                 if char not in node.children:
#                     node.children[char] = TrieNode()
#                 node = node.children[char]
#             node.is_end_of_word = True

#         def search(self, prefix):
#             node = self.root
#             for char in prefix:
#                 if char not in node.children:
#                     return []
#                 node = node.children[char]
#             return self._get_all(node, prefix)

#         def _get_all(self, node, prefix):
#             results = []
#             if node.is_end_of_word:
#                 results.append(prefix)
#             for char, child_node in node.children.items():
#                 results.extend(self._get_all(child_node, prefix + char))
#             return results

#     trie = Trie()

#     # 從Django模型中讀取所有的電影名稱
#     movies = Movies.objects.filter(mid < 100)

#     for movie in movies:
#         trie.insert(movie.name)  # 假設你的電影模型有一個名為name的字段

#     # 現在你可以使用trie.search方法來進行自動完成搜索
#     print(trie.search("Mo"))  # 將打印出所有以"Mo"開頭的電影名稱
