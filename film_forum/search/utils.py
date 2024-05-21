import json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.mid = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, mid):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.mid = mid

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._get_all(node, prefix)

    def _get_all(self, node, prefix):
        results = []
        if node.is_end_of_word:
            results.append({'name': prefix, 'mid': node.mid})
        for char, child_node in node.children.items():
            results.extend(self._get_all(child_node, prefix + char))
        return results

    def serialize(self):
        def serialize_node(node):
            return {
                'children': {char: serialize_node(child_node) for char, child_node in node.children.items()},
                'is_end_of_word': node.is_end_of_word,
                'mid': node.mid
            }
        return json.dumps(serialize_node(self.root))

    @staticmethod
    def deserialize(data):
        def deserialize_node(data):
            node = TrieNode()
            node.children = {char: deserialize_node(child_data) for char, child_data in data['children'].items()}
            node.is_end_of_word = data['is_end_of_word']
            node.mid = data['mid']
            return node

        trie = Trie()
        trie.root = deserialize_node(json.loads(data))
        return trie
