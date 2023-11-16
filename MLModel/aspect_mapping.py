import Levenshtein
import nltk
from nltk.stem import LancasterStemmer

nltk.download('lancaster')

# Initialize Lancaster Stemmer
lancaster_stemmer = LancasterStemmer()


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


def find_closest_word(word, synonym_list, threshold_percent=0.1):
    # Apply Lancaster stemming
    stemmed_word = lancaster_stemmer.stem(word)

    closest_word = None
    min_distance = float('inf')
    max_edit_distance = threshold_percent * len(stemmed_word)  # Calculate the maximum allowed edit distance

    for stored_word, _ in synonym_list:  # Iterate through the words in the Trie
        # Apply Lancaster stemming to stored words
        stemmed_stored_word = lancaster_stemmer.stem(stored_word)
        distance = Levenshtein.distance(stemmed_word, stemmed_stored_word)

        if distance <= max_edit_distance:
            if distance < min_distance:
                closest_word = stored_word
                min_distance = distance

    return closest_word


def map_reviews_to_synonyms(reviews, product_type):
    laptop_synonym_words = [
        ("windows", "OS"),
        ("ubuntu", "OS"),
        ("os", "OS"),
        ("linux", "OS"),
        ("operating system", "OS"),
        ("keyboard", "Keyboard"),
        ("trackpad", "Trackpad"),
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
        ("gaming", "Performance"),
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
        ("feature", "Range of Features"),
        ("port", "Connectivity"),
        ("connectivity", "Connectivity"),
        ("design", "Design"),
        ("style", "Design"),
        ("sleek", "Design"),
        ("gorgeous", "Design"),
        ("beautiful", "Design"),
        ("slim", "Design"),
        ("handsome", "Design"),
        ("build", "Build Quality"),
        ("durable", "Build Quality"),
        ("plastic", "Build Quality"),
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
        ("height", "Size"),
        ("space", "Size"),
        ("sound", "Speaker"),
        ("music", "Speaker"),
        ("vocal", "Speaker"),
        ("Amp / DAC", "Speaker"),
        ("Amp", "Speaker"),
        ("DAC", "Speaker"),
        ("microphone", "Microphone"),
        ("mic", "Microphone")
    ]

    phone_synonym_words = [
        ("android", "OS"),
        ("oxygenOS", "OS"),
        ("os", "OS"),
        ("ios", "OS"),
        ("operating system", "OS"),
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
        ("gaming", "Performance"),
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
        ("feature", "Range of Features"),
        ("port", "Connectivity"),
        ("connectivity", "Connectivity"),
        ("5G", "Connectivity"),
        ("design", "Design"),
        ("style", "Design"),
        ("sleek", "Design"),
        ("gorgeous", "Design"),
        ("beautiful", "Design"),
        ("slim", "Design"),
        ("handsome", "Design"),
        ("build", "Build Quality"),
        ("durable", "Build Quality"),
        ("plastic", "Build Quality"),
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
        ("height", "Size"),
        ("space", "Size"),
        ("slippery", "Phone Grip"),
        ("grip", "Phone Grip"),
        ("sound", "Speaker"),
        ("music", "Speaker"),
        ("vocal", "Speaker"),
        ("Amp / DAC", "Speaker"),
        ("microphone", "Microphone"),
        ("mic", "Microphone")
    ]

    smartwatch_synonym_words = [
        ("android", "OS"),
        ("oxygenOS", "OS"),
        ("os", "OS"),
        ("ios", "OS"),
        ("operating system", "OS"),
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
        ("feature", "Range of Features"),
        ("port", "Connectivity"),
        ("connectivity", "Connectivity"),
        ("fitness tracking", "Fitness Tracking"),
        ("health", "Health Monitoring"),
        ("notification", "Notification"),
        ("design", "Design"),
        ("style", "Design"),
        ("sleek", "Design"),
        ("gorgeous", "Design"),
        ("beautiful", "Design"),
        ("slim", "Design"),
        ("handsome", "Design"),
        ("water resistance", "Water Resistance"),
        ("water", "Water Resistance"),
        ("water proof", "Water Resistance"),
        ("build", "Build Quality"),
        ("durable", "Build Quality"),
        ("plastic", "Build Quality"),
        ("well-built", "Build Quality"),
        ("flimsy", "Build Quality"),
        ("break", "Build Quality"),
        ("fragile", "Build Quality"),
        ("sturdy", "Build Quality"),
        ("rug", "Build Quality"),
        ("tough", "Build Quality"),
        ("secure", "Security"),
        # ("camera cover", "security"),
        ("size", "Size"),
        ("one hand phone", "Size"),
        ("small", "Size"),
        ("large", "Size"),
        ("big", "Size"),
        ("height", "Size"),
        ("space", "Size"),
        ("sound", "Speaker"),
        ("music", "Speaker"),
        ("vocal", "Speaker"),
        ("Amp / DAC", "Speaker"),
        ("microphone", "Microphone"),
        ("mic", "Microphone")
    ]

    headphone_synonym_words = [
        ("comfort", "Comfort"),
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
        ("battery", "Battery"),
        ("charge", "Battery"),
        ("port", "Connectivity"),
        ("wireless", "connectivity"),
        ("bluetooth", "connectivity"),
        ("connectivity", "Connectivity"),
        ("noise", "Noise Cancellation"),
        ("noise cancellation", "Noise Cancellation"),
        ("design", "Design"),
        ("style", "Design"),
        ("sleek", "Design"),
        ("gorgeous", "Design"),
        ("beautiful", "Design"),
        ("slim", "Design"),
        ("handsome", "Design"),
        ("water resistance", "Water Resistance"),
        ("water", "Water Resistance"),
        ("water proof", "Water Resistance"),
        ("build", "Build Quality"),
        ("durable", "Build Quality"),
        ("plastic", "Build Quality"),
        ("well-built", "Build Quality"),
        ("flimsy", "Build Quality"),
        ("break", "Build Quality"),
        ("fragile", "Build Quality"),
        ("sturdy", "Build Quality"),
        ("rug", "Build Quality"),
        ("tough", "Build Quality"),
        ("secure", "Security"),
        ("portable", "Portability"),
        ("lightweight", "Portability"),
        ("easy to carry", "Portability"),
        ("bulky", "Portability"),
        ("heavy", "Portability"),
        ("weight", "Portability"),
        ("folding", "Portability"),
        ("button", "Controls"),
        ("touch", "Controls"),
        ("controls", "Controls"),
        # ("camera cover", "security"),
        ("size", "Size"),
        ("one hand phone", "Size"),
        ("small", "Size"),
        ("large", "Size"),
        ("big", "Size"),
        ("height", "Size"),
        ("space", "Size"),
        ("sound", "Sound Quality"),
        ("music", "Sound Quality"),
        ("vocal", "Sound Quality"),
        ("microphone", "Microphone Quality"),
        ("mic", "Microphone Quality")
    ]

    if product_type == "laptop":
        synonym_words = laptop_synonym_words
    elif product_type == "phone":
        synonym_words = phone_synonym_words
    elif product_type == "smartwatch":
        synonym_words = smartwatch_synonym_words
    elif product_type == "headphone":
        synonym_words = headphone_synonym_words
    else:
        raise ValueError("Invalid product type")

    word_trie = Trie()
    for word, mapping in synonym_words:
        word_trie.insert(word, mapping)

    mapped_reviews = []

    for aspect_list, sentiment_list in reviews:
        mapped_aspects = []
        for aspect in aspect_list:
            closest_word = find_closest_word(aspect, synonym_words)
            mapping = [mapping for word, mapping in synonym_words if word == closest_word]
            if mapping:
                mapped_aspects.append(mapping[0])

        mapped_sentiments = sentiment_list
        mapped_reviews.append((mapped_aspects, mapped_sentiments))

    return mapped_reviews
