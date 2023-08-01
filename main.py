from src.perfume_chooser import rank_perfumes
from src.pdf_generator import generate_pdf
from config import output_file_path, num_top_perfumes

def save_top_perfumes():
    ranked_df = rank_perfumes()
    if ranked_df is not None:
        top_perfumes = ranked_df.head(num_top_perfumes)
        top_perfumes.to_csv(output_file_path, index=False)
        generate_pdf(top_perfumes)

if __name__ == '__main__':
    save_top_perfumes()
