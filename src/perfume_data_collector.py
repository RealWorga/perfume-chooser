import math
import os
import csv

from bs4 import BeautifulSoup

from config import CATEGORICAL_DATA_PATH, CAT_OUTPUT_PATH

def calculate_likeability(thumbs_up, thumbs_down):
    n = thumbs_up + thumbs_down
    if n == 0 or thumbs_up == 0:
        return 0

    z = 1.96 #95% confidence
    phat = thumbs_up / n
    likeability = (phat + z*z/(2*n) - z * math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
    return max(0, round(likeability, 5))

def extract_perfume_data(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    
    perfumes = soup.find_all('div', class_='cell small-6 large-4 nomination-box flex-container flex-dir-column align-justify')
    
    perfume_data = []
    
    for perfume in perfumes:
        try:
            name = " ".join(perfume.find('a').text.strip().split())
            # Ignore if there's no name
            if not name:
                continue
            
            img_src = perfume.find('img')['src']
            
            votes = perfume.find_all('div', class_='num-votes')
            thumbs_up = int(votes[0].text)
            thumbs_down = int(votes[1].text)
            likeability = calculate_likeability(thumbs_up, thumbs_down)
            perfume_data.append([name, likeability, thumbs_up, thumbs_down, img_src])
        except Exception as e:
            print(f"Error processing perfume data: {e}")
    
    return perfume_data

def write_to_csv(perfume_data, category):
    os.makedirs(CAT_OUTPUT_PATH, exist_ok=True)
    
    filename = os.path.join(CAT_OUTPUT_PATH, f'perfume_data_{category.replace(" ", "_")}.csv')
    with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["Perfume Name", "Wilson Score", "Thumbs Up", "Thumbs Down", "Img Url"])
        writer.writerows(perfume_data)

def create_categorical_data():
    if not os.path.exists(CATEGORICAL_DATA_PATH):
        print(f"Directory '{CATEGORICAL_DATA_PATH}' does not exist. Please ensure you have the correct path.")
        return

    for filename in os.listdir(CATEGORICAL_DATA_PATH):
        if filename.endswith(".html"):
            constant_name = filename.rsplit('.', 1)[0]
            filepath = os.path.join(CATEGORICAL_DATA_PATH, filename)
            
            with open(filepath, 'r', encoding='utf-8-sig') as file:
                html_data = file.read()
            
            print(constant_name, " - Done.")
            write_to_csv(extract_perfume_data(html_data), constant_name)
