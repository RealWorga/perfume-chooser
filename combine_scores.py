import csv
import os
from config import CAT_OUTPUT_PATH

Z_SCORES = "sorted_final_perfume_z_scores.csv"
BAYESIAN_AVERAGE = "sorted_final_perfume_bayesian_average.csv"
HOTNESS = "sorted_final_perfume_hotness.csv"

WEIGHTS = {
    Z_SCORES: 0.2,
    BAYESIAN_AVERAGE: 0.4,
    HOTNESS: 0.4
}

def load_data_from_csv(filename):
    data = {}
    with open(os.path.join(CAT_OUTPUT_PATH, filename), 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
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

    for perfume, scores in combined_scores.items():
        weighted_sum = sum(WEIGHTS[file] * score for file, score in zip(WEIGHTS, scores))
        combined_scores[perfume] = weighted_sum / sum(WEIGHTS.values())

    return combined_scores

def write_combined_data_to_csv(data, output_filename):
    with open(os.path.join(CAT_OUTPUT_PATH, output_filename), 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["Perfume Name", "Combined Score"])
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        for row in sorted_data:
            writer.writerow(row)

bayesian_data = load_data_from_csv(BAYESIAN_AVERAGE)
hotness_data = load_data_from_csv(HOTNESS)
zscore_data = load_data_from_csv(Z_SCORES)

combined_data = combine_scores([zscore_data, bayesian_data, hotness_data])

write_combined_data_to_csv(combined_data, "combined_scores.csv")

print("Files have been combined!")
