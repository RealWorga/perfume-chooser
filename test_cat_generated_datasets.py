import os
import csv

from config import CAT_OUTPUT_PATH, CAT_OUTPUT_FIXED_PATH


def validate_csv_file(filename):
    """
    Validate a given CSV file.
    Returns a list of issues found, empty list if none.
    """
    issues = []
    seen_rows = set()

    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        header = next(reader) 

        if header != ["Perfume Name", "Wilson Score", "Thumbs Up", "Thumbs Down", "Img Url"]:
            issues.append(f"Unexpected header: {header}")

        row_number = 1 
        for row in reader:
            row_number += 1

            if len(row) != 5 or any(not cell.strip() for cell in row):
                issues.append(
                    f"Row {row_number} has an unexpected number of fields or empty cells: {row}")
                continue

            name, score, thumbs_up, thumbs_down, img_url = row

            if not (3 <= len(name) <= 150):
                issues.append(
                    f"Row {row_number} has an unusual name length: {name}")

            if '&amp;' in name:
                issues.append(
                    f"Row {row_number} has encoded characters in the name: {name}")

            try:
                score = float(score)
                thumbs_up = int(thumbs_up)
                thumbs_down = int(thumbs_down)
            except ValueError:
                issues.append(
                    f"Row {row_number} has data in an unexpected format: {row}")
                continue

            if not (0 <= score <= 1):
                issues.append(
                    f"Row {row_number} has an unexpected score value: {score}")

            if thumbs_up < 0 or thumbs_down < 0:
                issues.append(
                    f"Row {row_number} has negative vote counts: {thumbs_up}, {thumbs_down}")

            if not img_url.startswith("https://"):
                issues.append(
                    f"Row {row_number} has an unexpected Img Url format: {img_url}")

            row_tuple = tuple(row)
            if row_tuple in seen_rows:
                issues.append(
                    f"Row {row_number} appears to be a duplicate: {row}")
            else:
                seen_rows.add(row_tuple)

    return issues


def check_csv_files_in_directory(directory):
    """
    Check all CSV files in the given directory.
    Prints issues to console.
    """
    all_files = os.listdir(directory)

    csv_files = [f for f in all_files if f.endswith('.csv')]

    all_issues = []

    for csv_file in csv_files:
        filepath = os.path.join(directory, csv_file)
        issues = validate_csv_file(filepath)

        if issues:
            all_issues.extend([(csv_file, issue) for issue in issues])

    if all_issues:
        for filename, issue in all_issues:
            print(f"In {filename}: {issue}")
    else:
        print("No issues found in any CSV files.")


if __name__ == "__main__":
    check_csv_files_in_directory(CAT_OUTPUT_PATH)
    #check_csv_files_in_directory(CAT_OUTPUT_FIXED_PATH)
