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
                    data[perfume_name].append((wilson_score, thumbs_up, thumbs_down))
                    urls[perfume_name] = img_url
    
    return data, urls

def bayesian_average(data):
    """
    Returns a dictionary of perfumes and their Bayesian average scores.
    """
    bayesian_scores = {}

    total_scores = sum([ws for scores in data.values() for ws, _, _ in scores])
    total_votes = sum([tu + td for scores in data.values() for _, tu, td in scores])

    total_data_points = sum([len(scores) for scores in data.values()])

    # Constants C & M
    M = total_scores / total_data_points
    C = total_votes / total_data_points

    for perfume, scores in data.items():
        total_votes_for_perfume = sum([tu + td for _, tu, td in scores])
        sum_weighted_scores = sum([ws * (tu + td) for ws, tu, td in scores])

        bayesian_score = (C * M + sum_weighted_scores) / (C + total_votes_for_perfume)
        bayesian_scores[perfume] = bayesian_score
    
    return bayesian_scores



def normalize_scores(scores):
    """
    Normalize scores to range between 0 and 1
    """
    min_score = min(scores.values())
    max_score = max(scores.values())
    range_score = max_score - min_score

    return {perfume: (score - min_score) / range_score for perfume, score in scores.items()}

def generate_final_csv(normalized_scores, data, urls, path):
    output_file = os.path.join(path, "final_perfume_bayesian_average.csv")
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["Perfume Name", "Bayesian Score", "Number of Categories", "Img Url"])
        
        for perfume, score in normalized_scores.items():
            writer.writerow([perfume, score, len(data[perfume]), urls[perfume]])

    print(f"Final scores written to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate final perfume scores from categorical datasets.")
    parser.add_argument('-fixed', action='store_true', help="Use the fixed path.")
    args = parser.parse_args()
    
    path = CAT_OUTPUT_FIXED_PATH if args.fixed else CAT_OUTPUT_PATH

    # Ensure the directory exists
    if not os.path.exists(path):
        print(f"The specified directory '{path}' does not exist. Please check your input.")
    else:
        data, urls = read_csv_data(path)
        bayesian_scores = bayesian_average(data)
        normalized_scores = normalize_scores(bayesian_scores)
        generate_final_csv(normalized_scores, data, urls, path)
