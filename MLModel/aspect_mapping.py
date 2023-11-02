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


def find_closest_word(word, synonym_list, threshold_percent=0.6):
    closest_word = None
    min_distance = float('inf')
    max_edit_distance = threshold_percent * len(word)  # Calculate the maximum allowed edit distance
    print(max_edit_distance)
    print(word)

    for stored_word, _ in synonym_list:  # Iterate through the words in the Trie
        print(stored_word)
        distance = Levenshtein.distance(word, stored_word)
        print(distance)
        if distance <= max_edit_distance:
            if distance < min_distance:
                closest_word = stored_word
                min_distance = distance

    return closest_word


def map_reviews_to_synonyms(reviews):
    synonym_words = [
        ("android", "OS"),
        ("oxygenOS", "OS"),
        ("os", "OS"),
        ("ios", "OS"),
        ("keyboard", "Keyboard"),
        ("price", "Price"),
        ("expensive", "Price"),
        ("cheap", "Price"),
        ("afford", "Price"),
        ("budget", "Price"),
        ("cost", "Price"),
        ("money", "Price"),
        ("dollar", "Price"),
        ("pay", "Price"),
        ("$", "Price"),
        ("camera", "Camera"),
        ("photo", "Camera"),
        ("picture", "Camera"),
        ("photograph", "Camera"),
        ("zoom", "Camera"),
        ("performance", "Performance"),
        ("powerful", "Performance"),
        ("smooth", "Performance"),
        ("slow", "Performance"),
        ("lag", "Performance"),
        ("bug", "Performance"),
        ("processor", "Performance"),
        ("memory", "Performance"),
        ("consumption", "Performance"),
        ("storage", "Performance"),
        ("battery", "Battery"),
        ("charge", "Battery"),
        ("display", "Display"),
        ("pixel", "Display"),
        ("screen", "Display"),
        ("dull", "Display"),
        ("blur", "Display"),
        ("resolution", "Display"),
        ("versatile", "Range of Features"),
        ("port", "Range of Features"),
        ("feature", "Range of Features"),
        ("design", "Design"),
        ("style", "Design"),
        ("sleek", "Design"),
        ("gorgeous", "Design"),
        ("beautiful", "Design"),
        ("slim", "Design"),
        ("handsome", "Design"),
        ("build", "Build Quality"),
        ("durable", "Build Quality"),
        ("well-built", "Build Quality"),
        ("flimsy", "Build Quality"),
        ("break", "Build Quality"),
        ("fragile", "Build Quality"),
        ("sturdy", "Build Quality"),
        ("rug", "Build Quality"),
        ("tough", "Build Quality"),
        ("secure", "Security"),
        # ("camera cover", "security"),
        ("fingerprint", "Security"),
        ("facial", "Security"),
        ("face-id", "Security"),
        ("touch-id", "Security"),
        ("authenticate", "Security"),
        ("portable", "Portability"),
        ("lightweight", "Portability"),
        ("easy to carry", "Portability"),
        ("bulky", "Portability"),
        ("heavy", "Portability"),
        ("weight", "Portability"),
        ("size", "Size"),
        ("one hand phone", "Size"),
        ("small", "Size"),
        ("large", "Size"),
        ("big", "Size"),
        ("space", "Size"),
        ("slippery", "Phone Grip"),
        ("grip", "Phone Grip")
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
