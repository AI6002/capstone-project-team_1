def group_reviews(reviews):
    """
    Group reviews by aspect and sentiment.

    Args:
        reviews (list of tuple): List of reviews where each review is a tuple of aspects and sentiments.

    Returns:
        dict: A dictionary where each aspect is associated with sentiment counts.
    """
    aspect_sentiment_counts = {}

    for aspects, sentiments in reviews:
        for aspect, sentiment in zip(aspects, sentiments):
            if aspect not in aspect_sentiment_counts:
                aspect_sentiment_counts[aspect] = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
            aspect_sentiment_counts[aspect][sentiment] += 1

    return aspect_sentiment_counts


def calculate_aspect_scores(aspect_sentiment_counts):
    """
    Calculate aspect sentiment scores.

    Args:
        aspect_sentiment_counts (dict): Aspect sentiment counts.

    Returns:
        dict: A dictionary where each aspect is associated with a sentiment score.
    """
    aspect_scores = {}

    for aspect, sentiment_counts in aspect_sentiment_counts.items():
        score = sentiment_counts['Positive'] - sentiment_counts['Negative']
        aspect_scores[aspect] = score

    return aspect_scores


def find_best_and_worst_features(aspect_scores):
    """
    Find the best and worst features based on aspect scores.

    Args:
        aspect_scores (dict): Aspect sentiment scores.

    Returns:
        list, list: Lists of best and worst features.
    """
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


def analyze_feature_sentiments(mapped_reviews):
    """
    Analyze feature sentiments based on mapped reviews.

    Args:
        mapped_reviews (list of tuple): List of mapped reviews.

    Returns:
        list, list: Lists of best and worst features.
    """
    aspect_sentiment_counts = group_reviews(mapped_reviews)
    aspect_scores = calculate_aspect_scores(aspect_sentiment_counts)
    best_features, worst_features = find_best_and_worst_features(aspect_scores)
    
     # Check if the lists are not null, not none, and not empty
    best_feature_str = ', '.join(filter(None, best_features)) if best_features else None
    worst_feature_str = ', '.join(filter(None, worst_features)) if worst_features else None

    # Create the new format dictionary
    best_and_worst_features = {
        'bestFeature': best_feature_str,
        'worstFeature': worst_feature_str
    }
    
    # best_and_worst_features = {
    #     'bestFeature': best_features,
    #     'worstFeature': worst_features
    # }

    return best_and_worst_features
