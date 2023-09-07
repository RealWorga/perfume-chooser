import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
INPUT_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'perfume_data.csv')
OUTPUT_FILE_PATH = os.path.join(PROJECT_ROOT, 'outputs', 'chosen_perfumes_budget.csv')
PDF_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'outputs', 'chosen_perfumes_budget.pdf')

NUM_TOP_PERFUMES = 21

#Temporary location for the perfume datas from the different categories
CATEGORICAL_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'perfume_categorical_datas')

CAT_OUTPUT_PATH = os.path.join(PROJECT_ROOT, "outputs", "perfume_cat_datas")
CAT_OUTPUT_FIXED_PATH = os.path.join(PROJECT_ROOT, "outputs", "perfume_cat_datas_fixed")
