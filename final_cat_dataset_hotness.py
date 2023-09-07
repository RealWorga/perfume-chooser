from math import log10

import os
import csv
import argparse
from collections import defaultdict

from config import CAT_OUTPUT_PATH, CAT_OUTPUT_FIXED_PATH

def read_csv_data(path):
    data = defaultdict(list)
    urls = {}  # To store image URLs
    
    for filename in os.listdir(path):
        if filename.endswith(".csv") and "final" not in filename:
            with open(os.path.join(path, filename), 'r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                next(reader)  # skip the header

                for row in reader:
                    perfume_name = row[0]
                    wilson_score = float(row[1])
                    thumbs_up = int(row[2])
                    thumbs_down = int(row[3])
                    img_url = row[4]  # Assuming URL is in the fifth column
                    # Append all data, we can aggregate later
                    data[perfume_name].append((wilson_score, thumbs_up, thumbs_down, img_url))
                    urls[perfume_name] = img_url
    
    return data, urls

def reddit_hotness_score(upvotes, downvotes, categories):
    s = upvotes - downvotes
    order = log10(max(abs(s), 1))
    if s > 0:
        sign = 1
    elif s < 0:
        sign = -1
    else:
        sign = 0

    # Here, instead of time since post, we use number of categories to emphasize versatility
    return sign * order + categories / 45000.0

def compute_aggregate_scores(data):
    scores = {}

    for perfume, records in data.items():
        total_upvotes = sum([r[1] for r in records])
        total_downvotes = sum([r[2] for r in records])

        hotness = reddit_hotness_score(total_upvotes, total_downvotes, len(records))
        scores[perfume] = hotness

    return scores

def normalize_scores(scores):
    """
    Normalize scores to range between 0 and 1
    """
    min_score = min(scores.values())
    max_score = max(scores.values())
    range_score = max_score - min_score

    return {perfume: (score - min_score) / range_score for perfume, score in scores.items()}

def generate_final_csv(scores, data, urls, path):
    output_file = os.path.join(path, "final_perfume_hotness.csv")
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["Perfume Name", "Hotness Score", "Number of Categories", "Img Url"])
        
        for perfume, score in scores.items():  # Corrected the loop to use .items()
            writer.writerow([perfume, score, len(data[perfume]), urls[perfume]])

    print(f"Final ranking written to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate final perfume rankings using Reddit's hotness algorithm.")
    parser.add_argument('-fixed', action='store_true', help="Use the fixed path.")
    args = parser.parse_args()
    
    path = CAT_OUTPUT_FIXED_PATH if args.fixed else CAT_OUTPUT_PATH
    
    if not os.path.exists(path):
        print(f"Error: The directory '{path}' does not exist. Please make sure it's the correct path.")
    else:
        data, urls = read_csv_data(path)
        aggregate_scores = compute_aggregate_scores(data)
        normalized_scores = normalize_scores(aggregate_scores)
        generate_final_csv(normalized_scores, data, urls, path)


