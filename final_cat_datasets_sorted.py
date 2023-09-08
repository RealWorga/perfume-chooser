import csv
import os
from config import CAT_OUTPUT_PATH

def sort_csv_by_second_column(input_file_name, output_file_name):
    input_file_path = os.path.join(CAT_OUTPUT_PATH, input_file_name)
    output_file_path = os.path.join(CAT_OUTPUT_PATH, output_file_name)

    with open(input_file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        sorted_rows = sorted(reader, key=lambda row: float(row[1]), reverse=True)

    with open(output_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in sorted_rows:
            writer.writerow(row)

files_to_sort = ["final_perfume_bayesian_average.csv", "final_perfume_hotness.csv", "final_perfume_z_scores.csv"]
for file in files_to_sort:
    sort_csv_by_second_column(file, f"sorted_{file}")

print("Files have been sorted!")
