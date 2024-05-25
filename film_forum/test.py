import trie
from member.models import Movies

film = Movies.objects.all().values_list("name", "mid")

film = list(film)

result = trie.TrieTree()
for m in film:
    try:
        result.insert(m[0], m[1])
    except:
        print(m)
        break

# print(result.search("A"))
# print("here")