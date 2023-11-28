import pandas as pd
from collections import Counter


def calculate_accuracy(mapped_data, evaluation_data):

    # Convert the list of tuples to a DataFrame
    mapped_df = pd.DataFrame(mapped_data, columns=['aspect', 'sentiment'])

    # Extract positive and negative aspects from the "aspect" column based on sentiments
    mapped_df['Detected_Positive_Aspects'] = mapped_df.apply(
        lambda row: [aspect for aspect, sentiment in zip(row['aspect'], row['sentiment']) if aspect and
                     sentiment.lower() == 'positive'], axis=1)
    mapped_df['Detected_Negative_Aspects'] = mapped_df.apply(
        lambda row: [aspect for aspect, sentiment in zip(row['aspect'], row['sentiment']) if aspect and
                     sentiment.lower() == 'negative'], axis=1)

    # Merge the evaluation data and mapped data on the index
    merged_data = pd.concat([evaluation_data, mapped_df], axis=1)

    # Export the merged data for further analysis
    # merged_data.to_csv('./MLModel/data/merged_data.csv', index=False)

    correct_positives = 0
    correct_negatives = 0

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for index, row in merged_data.iterrows():
        detected_positives = row['Detected_Positive_Aspects']
        actual_positives = row['Positive_Aspects']

        detected_negatives = row['Detected_Negative_Aspects']
        actual_negatives = row['Negative_Aspects']

        # Compare positive aspects of the evaluation data and the model
        correct_positives += list_similarity(row['Detected_Positive_Aspects'], row['Positive_Aspects'])

        # Compare negative aspects of the evaluation data and the model
        correct_negatives += list_similarity(row['Detected_Negative_Aspects'], row['Negative_Aspects'])

        # True Positives
        true_positives += sum(1 for aspect in set(detected_positives) if aspect in set(actual_positives))
        true_positives += sum(1 for aspect in set(detected_negatives) if aspect in set(actual_negatives))

        # False Positives
        false_positives += sum(1 for aspect in set(detected_positives) if aspect not in set(actual_positives))
        false_positives += sum(1 for aspect in set(detected_negatives) if aspect not in set(actual_negatives))

        # False Negatives
        false_negatives += sum(1 for aspect in set(actual_positives) if aspect not in set(detected_positives))
        false_negatives += sum(1 for aspect in set(actual_negatives) if aspect not in set(detected_negatives))

    total_rows = 2 * merged_data.shape[0]
    accuracy = (correct_positives + correct_negatives) / total_rows if total_rows != 0 else None
    precision = true_positives / (true_positives + false_positives) if (correct_positives + false_positives) != 0 else None
    recall = true_positives / (true_positives + false_negatives) if (correct_positives + false_negatives) != 0 else None
    f1_score = 2 / (1/precision + 1/recall) if precision !=0 and recall != 0 else None

    return accuracy, precision, recall, f1_score


# Function to map reviews using the mapping module
def map_and_evaluate(mapped_data, evaluation_data):

    # Calculate accuracy
    accuracy, precision, recall, f1_score = calculate_accuracy(mapped_data, evaluation_data)

    if accuracy is not None:
        print(f"Accuracy: {accuracy * 100:.2f}%")
    else:
        print("Accuracy: Division by zero, cannot calculate.")

    if precision is not None:
        print(f"Precision: {precision * 100:.2f}%")
    else:
        print("Precision: Division by zero, cannot calculate.")

    if recall is not None:
        print(f"Recall: {recall * 100:.2f}%")
    else:
        print("Recall: Division by zero, cannot calculate.")

    if f1_score is not None:
        print(f"F1 Score: {f1_score * 100:.2f}%")
    else:
        print("F1 Score: Division by zero, cannot calculate.")


def list_similarity(actual, detected):
    counter1 = Counter(actual)
    counter2 = Counter(detected)

    intersection = sum((counter1 & counter2).values())
    total = sum((counter1 | counter2).values())

    similarity = intersection / total if total != 0 else 1  # Handling the case where both lists are empty
    return similarity