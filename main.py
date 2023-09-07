from src.perfume_chooser import rank_perfumes
from src.pdf_generator import generate_pdf
from config import OUTPUT_FILE_PATH, NUM_TOP_PERFUMES

def save_top_perfumes():
    ranked_df = rank_perfumes()
    if ranked_df is not None:
        top_perfumes = ranked_df.head(NUM_TOP_PERFUMES)
        top_perfumes.to_csv(OUTPUT_FILE_PATH, index=False)
        generate_pdf(top_perfumes)

if __name__ == '__main__':
    save_top_perfumes()
