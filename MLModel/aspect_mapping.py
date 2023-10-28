import Levenshtein

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
    ("range of features", "range of features"),
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
    # Add more synonym pairs as needed
]

# Define the TrieNode class to store words in the mapping attribute
class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.mapping = set()  # Use a set to store multiple words with the same mapping

# Function to insert words into the Trie
def insert_words(trie, words, mapping):
    for word in words:
        node = trie.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.mapping.add(mapping)

# Insert your synonym words into the Trie
word_trie = Trie()
for word, mapping in synonym_words:
    insert_words(word_trie, [word], mapping)  # Use a list to store the words

reviews = [
    (['camera', 'performance', 'battery life'], ['Positive', 'Positive', 'Negative']),
    (['photos', 'Android experience', 'battery'], ['Positive', 'Positive', 'Negative']),
    (['price', 'performance', 'OxygenOS', 'camera quality', 'features'], ['Positive', 'Positive', 'Positive', 'Negative', 'Negative']),
    (['camera system', 'Google services'], ['Positive', 'Negative']),
    (['design', 'processing power'], ['Positive', 'Negative']),
    (['performance', 'portability'], ['Positive', 'Positive']),
    (['display', 'media consumption', 'productivity', 'price'], ['Positive', 'Positive', 'Positive', 'Neutral']),
    (['use', 'performance', 'applications'], ['Positive', 'Negative', 'Neutral']),
    (['display', 'keyboard', 'stylus'], ['Positive', 'Negative', 'Negative']),
    (['processing power'], ['Negative'])
]

# Initialize an empty list to store the mapped data
mapped_reviews = []

# Function to find the closest word in the Trie using Levenshtein distance
def find_closest_word(word, word_trie):
    closest_word = None
    min_distance = float('inf')
    for stored_word in word_trie.root.mapping:  # Iterate through the words in the Trie
        distance = Levenshtein.distance(word, stored_word)
        if distance < min_distance:
            closest_word = stored_word
            min_distance = distance
    return closest_word

# Iterate through the reviews and map aspects and sentiments
for aspect_list, sentiment_list in reviews:
    mapped_aspects = []
    for aspect in aspect_list:
        mapping = word_trie.search(aspect)  # Check if the word exists in the Trie
        if mapping is None:
            closest_word = find_closest_word(aspect, word_trie)
            if closest_word:
                mapping = word_trie.search(closest_word)
        mapped_aspects.append(mapping.pop() if mapping else aspect
