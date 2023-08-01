import pandas as pd
from sklearn.preprocessing import minmax_scale

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File not found at: {file_path}")

def normalize_data(df):
    try:
        df['norm_likeabilities'] = minmax_scale(df['Likeability'])
        df['norm_price_per_ml'] = 1 - minmax_scale(df['Price per ml'])
        return df
    except KeyError:
        print("Incorrect data format. 'Likeability' and 'Price per ml' columns are required.")

def compute_rewards(df):
    df['rewards'] = 0.5 * df['norm_likeabilities'] + 0.5 * df['norm_price_per_ml']
    return df
