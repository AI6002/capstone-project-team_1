# Function to group reviews by aspect and sentiment
def group_reviews(reviews):
    aspect_sentiments = {}

    for aspects, sentiments in reviews:
        for aspect, sentiment in zip(aspects, sentiments):
            if aspect not in aspect_sentiments:
                aspect_sentiments[aspect] = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
            aspect_sentiments[aspect][sentiment] += 1

    return aspect_sentiments


# Function to calculate aspect sentiment scores
def calculate_aspect_scores(aspect_sentiments):
    aspect_scores = {}

    for aspect, sentiment_counts in aspect_sentiments.items():
        score = sentiment_counts['Positive'] - sentiment_counts['Negative']
        aspect_scores[aspect] = score

    return aspect_scores


# Function to find best and worst features
def find_best_and_worst_features(aspect_scores):
    best_features = []
    worst_features = []

    max_score = max(aspect_scores.values())
    min_score = min(aspect_scores.values())

    for aspect, score in aspect_scores.items():
        if score == max_score:
            best_features.append(aspect)
        if score == min_score:
            worst_features.append(aspect)

    return best_features, worst_features


# Sample data
reviews = [
    (['camera', 'performance', 'battery'], ['Positive', 'Positive', 'Negative']),
    (['camera', 'OS', 'battery'], ['Positive', 'Positive', 'Negative']),
    (['price', 'performance', 'price', 'build quality', 'range of features'],
     ['Positive', 'Positive', 'Positive', 'Negative', 'Negative']),
    (['security', 'price'], ['Positive', 'Negative']),
    (['design', 'performance'], ['Positive', 'Negative']),
    (['performance', 'portability'], ['Positive', 'Positive']),
    (['display', 'display', 'performance', 'price'], ['Positive', 'Positive', 'Positive', 'Neutral']),
    (['OS', 'performance', 'camera'], ['Positive', 'Negative', 'Neutral']),
    (['display', 'keyboard', 'design'], ['Positive', 'Negative', 'Negative']),
    (['performance'], ['Negative'])
]

# Main execution
aspect_sentiments = group_reviews(reviews)
aspect_scores = calculate_aspect_scores(aspect_sentiments)
best_features, worst_features = find_best_and_worst_features(aspect_scores)

print("Best Features:")
print(best_features)

print("\nWorst Features:")
print(worst_features)
