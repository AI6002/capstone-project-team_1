import Levenshtein


class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.mapping = set()  # Use a set to store multiple words with the same mapping


class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Function to insert words into the Trie
    def insert(self, words, mapping):
        for word in words:
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.mapping.add(mapping)

    def search(self, word):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return None  # Word not found in the Trie
        return node.mapping

def find_closest_word(word, synonym_list):
    closest_word = None
    min_distance = float('inf')
    for stored_word, _ in synonym_list:  # Iterate through the words in the Trie
        distance = Levenshtein.distance(word, stored_word)
        if distance < min_distance:
            closest_word = stored_word
            min_distance = distance
    return closest_word


def map_reviews_to_synonyms(reviews):
    synonym_words = [
        ("android", "OS"),
        ("os", "OS"),
        ("ios", "OS"),
        ("keyboard", "keyboard"),
        ("price", "price"),
        ("expensive", "price"),
        ("cheap", "price"),
        ("afford", "price"),
        ("budget", "price"),
        ("cost", "price"),
        ("money", "price"),
        ("dollar", "price"),
        ("pay", "price"),
        ("$", "price"),
        ("camera", "camera"),
        ("photo", "camera"),
        ("picture", "camera"),
        ("photograph", "camera"),
        ("zoom", "camera"),
        ("performance", "performance"),
        ("powerful", "performance"),
        ("smooth", "performance"),
        ("slow", "performance"),
        ("lag", "performance"),
        ("bug", "performance"),
        ("processor", "performance"),
        ("memory", "performance"),
        ("storage", "performance"),
        ("battery", "battery"),
        ("charge", "battery"),
        ("display", "display"),
        ("pixel", "display"),
        ("screen", "display"),
        ("dull", "display"),
        ("blur", "display"),
        ("resolution", "display"),
        ("versatile", "range of features"),
        ("port", "range of features"),
        ("feature", "range of features"),
        ("design", "design"),
        ("style", "design"),
        ("sleek", "design"),
        ("gorgeous", "design"),
        ("beautiful", "design"),
        ("slim", "design"),
        ("handsome", "design"),
        ("build quality", "build quality"),
        ("durable", "build quality"),
        ("well-built", "build quality"),
        ("flimsy", "build quality"),
        ("break", "build quality"),
        ("fragile", "build quality"),
        ("sturdy", "build quality"),
        ("rug", "build quality"),
        ("tough", "build quality"),
        ("secure", "security"),
        ("camera cover", "security"),
        ("fingerprint", "security"),
        ("facial", "security"),
        ("face-id", "security"),
        ("touch-id", "security"),
        ("authenticate", "security"),
        ("portable", "portability"),
        ("lightweight", "portability"),
        ("easy to carry", "portability"),
        ("bulky", "portability"),
        ("heavy", "portability"),
        ("weight", "portability"),
        ("size", "size"),
        ("one hand phone", "size"),
        ("small", "size"),
        ("large", "size"),
        ("big", "size"),
        ("space", "size"),
        ("slippery", "phone grip"),
        ("grip", "phone grip")
    ]

    word_trie = Trie()
    for word, mapping in synonym_words:
        word_trie.insert(word, mapping)

    mapped_reviews = []

    for aspect_list, sentiment_list in reviews:
        mapped_aspects = []
        for aspect in aspect_list:
            closest_word = find_closest_word(aspect, synonym_words)
            mapping = [mapping for word, mapping in synonym_words if word == closest_word]
            mapped_aspects.append(mapping[0] if mapping else aspect)

        mapped_sentiments = sentiment_list
        mapped_reviews.append((mapped_aspects, mapped_sentiments))

    return mapped_reviews
