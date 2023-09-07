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
                    img_url = row[4]  # Assuming URL is in the fifth column

                    data[perfume_name].append(wilson_score)
                    urls[perfume_name] = img_url

    return data, urls

def z_score_normalization(data):
    z_scores = {}
    
    all_avg_scores = [sum(scores)/len(scores) for scores in data.values()]
    global_mean = sum(all_avg_scores) / len(all_avg_scores)
    global_std = (sum([(s - global_mean) ** 2 for s in all_avg_scores]) / len(all_avg_scores)) ** 0.5

    for perfume, scores in data.items():
        avg_score = sum(scores) / len(scores)
        z_score = (avg_score - global_mean) / global_std

        z_scores[perfume] = z_score

    # Normalize z-scores to [0, 1]
    min_z, max_z = min(z_scores.values()), max(z_scores.values())
    for perfume, z_score in z_scores.items():
        z_scores[perfume] = (z_score - min_z) / (max_z - min_z)
    
    return z_scores

def generate_final_csv(z_scores, data, urls, path):
    output_file = os.path.join(path, "final_perfume_z_scores.csv")
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["Perfume Name", "Final Z-Score", "Number of Categories", "Img Url"])
        
        for perfume, z_score in z_scores.items():
            writer.writerow([perfume, z_score, len(data[perfume]), urls[perfume]])

    print(f"Final scores written to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate final perfume scores from categorical datasets.")
    parser.add_argument('-fixed', action='store_true', help="Use the fixed path.")
    args = parser.parse_args()
    
    path = CAT_OUTPUT_FIXED_PATH if args.fixed else CAT_OUTPUT_PATH

    if not os.path.exists(path):
        print(f"Error: The directory '{path}' does not exist. Please make sure it's the correct path.")
    else:
        data, urls = read_csv_data(path)
        z_scores = z_score_normalization(data)
        generate_final_csv(z_scores, data, urls, path)
