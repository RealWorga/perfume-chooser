import os

# Configuration parameters
project_root = os.path.dirname(os.path.realpath(__file__))
input_file_path = os.path.join(project_root, 'data', 'perfume_data.csv')
output_file_path = os.path.join(project_root, 'outputs', 'chosen_perfumes_budget.csv')
pdf_output_path = os.path.join(project_root, 'outputs', 'chosen_perfumes_budget.pdf')
num_top_perfumes = 21
