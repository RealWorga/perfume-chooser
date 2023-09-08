import csv
import os
from config import CAT_OUTPUT_PATH

# Define the weights for each file type
WEIGHTS = {
    "sorted_final_perfume_z_scores.csv": 0.2,
    "sorted_final_perfume_bayesian_average.csv": 0.4,
    "sorted_final_perfume_hotness.csv": 0.4
}

def load_data_from_csv(filename):
    data = {}
    with open(os.path.join(CAT_OUTPUT_PATH, filename), 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            perfume_name = row[0]
            score = float(row[1])
            data[perfume_name] = score
    return data

def combine_scores(data_lists):
    combined_scores = {}
    for data in data_lists:
        for perfume, score in data.items():
            if perfume in combined_scores:
                combined_scores[perfume].append(score)
            else:
                combined_scores[perfume] = [score]

    # Calculate weighted average
    for perfume, scores in combined_scores.items():
        weighted_sum = sum(WEIGHTS[file] * score for file, score in zip(WEIGHTS, scores))
        combined_scores[perfume] = weighted_sum / sum(WEIGHTS.values())

    return combined_scores

def write_combined_data_to_csv(data, output_filename):
    with open(os.path.join(CAT_OUTPUT_PATH, output_filename), 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Perfume Name", "Combined Score"])
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        for row in sorted_data:
            writer.writerow(row)

# Load data from CSVs
bayesian_data = load_data_from_csv("sorted_final_perfume_bayesian_average.csv")
hotness_data = load_data_from_csv("sorted_final_perfume_hotness.csv")
zscore_data = load_data_from_csv("sorted_final_perfume_z_scores.csv")

# Combine data
combined_data = combine_scores([zscore_data, bayesian_data, hotness_data])

# Write combined data to CSV
write_combined_data_to_csv(combined_data, "combined_scores.csv")

print("Files have been combined!")
