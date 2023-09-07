import csv
import os

from config import CAT_OUTPUT_PATH, CAT_OUTPUT_FIXED_PATH

def fix_empty_names_in_csv(filename):
    input_filepath = os.path.join(CAT_OUTPUT_PATH, filename)
    output_filepath = os.path.join(CAT_OUTPUT_FIXED_PATH, filename)
    
    os.makedirs(CAT_OUTPUT_FIXED_PATH, exist_ok=True)

    valid_rows = []
    with open(input_filepath, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        headers = next(reader)
        valid_rows.append(headers)
        
        for row in reader:
            perfume_name = row[0].strip()
            if perfume_name:
                valid_rows.append(row)

    with open(output_filepath, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(valid_rows)

def main():
    for filename in os.listdir(CAT_OUTPUT_PATH):
        if filename.endswith(".csv"):
            fix_empty_names_in_csv(filename)
            print(f"Fixed {filename} and saved to {CAT_OUTPUT_FIXED_PATH}")

if __name__ == '__main__':
    main()
