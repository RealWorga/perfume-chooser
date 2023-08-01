from .data_manager import load_data, normalize_data, compute_rewards

from config import input_file_path

def rank_perfumes():
    df = load_data(input_file_path)
    if df is None:
        return None

    df = normalize_data(df)
    if df is None:
        return None

    df = compute_rewards(df)

    ranked_df = df.sort_values('rewards', ascending=False)
    ranked_df.reset_index(drop=True, inplace=True)

    return ranked_df
