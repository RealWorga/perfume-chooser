from PIL import Image as PILImage
import requests
from io import BytesIO
from config import pdf_output_path

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image as RLImage
from reportlab.lib import colors

import tempfile
import os

def fetch_image(url):
    try:
        response = requests.get(url)
        img = PILImage.open(BytesIO(response.content))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            img.save(temp_file.name, 'JPEG')
            return temp_file.name
    except Exception as e:
        print(f"Failed to fetch image at {url} due to {e}")
        return None

def generate_pdf(df):
    from reportlab.lib.styles import getSampleStyleSheet
    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    def scale(val, src, dst):
        return (val - src[0]) / (src[1]-src[0]) * (dst[1]-dst[0]) + dst[0]

    def gradient_color(scaled_value, color1, color2):
        return colors.Color(
            scaled_value * color2.red + (1 - scaled_value) * color1.red,
            scaled_value * color2.green + (1 - scaled_value) * color1.green,
            scaled_value * color2.blue + (1 - scaled_value) * color1.blue
        )

    
    ordered_columns = ["Image URL", "Perfume Name", "Reward", "G/B", "PPml"]
    df = df.rename(columns={'rewards': 'Reward', 'Likeability': 'G/B', 'Price per ml': 'PPml'})
    df['Image URL'] = df['Image URL'].apply(fetch_image)
    df[["Reward", "G/B", "PPml"]] = df[["Reward", "G/B", "PPml"]].round(4)
    df = df[ordered_columns]
    data = [ordered_columns] + df.values.tolist()

    page_width, page_height = A4
    col_width = page_width / 5.0
    col_widths = [
        0.5 * col_width,    # "Image" column (narrower)
        2.5 * col_width,     # "Perfume Name" column (wider)
        0.5 * col_width,     # "Reward" column (narrower)
        0.5 * col_width,     # "Likeability" column (narrower)
        0.5 * col_width,     # "PPml" column (narrower)
    ]

    data[0][0] = "" 

    for i in range(1, len(data)):
        img_path = data[i][0]
        data[i][0] = RLImage(img_path, width=0.75*col_widths[0], height=0.75*col_widths[0])
        # Wrap each perfume name in its own table
        # This helps avoid conflicts between table style and paragraph style
        name_table = Table([[Paragraph(data[i][1], styleN)]], colWidths=[col_widths[1]])
        name_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        data[i][1] = name_table

    doc = SimpleDocTemplate(pdf_output_path, pagesize=A4)
    table = Table(data, colWidths=col_widths)

    min_rewards = df["Reward"].min()
    max_rewards = df["Reward"].max()
    min_likeability = df["G/B"].min()
    max_likeability = df["G/B"].max()
    min_ppml = df["PPml"].min()
    max_ppml = df["PPml"].max()

    color_scale = (colors.green, colors.yellow, colors.red)

    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

        ('ALIGN',(1,0),(-1,0),'LEFT'),
        ('ALIGN',(1,1),(-1,-1),'LEFT'),
        ('ALIGN',(2,0),(-1,0),'RIGHT'),
        ('ALIGN',(2,1),(-1,-1),'RIGHT'),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)  # add gridlines
    ])


    # color grading for Reward, Likeability and PPml
    for i in range(1, len(data)):
        # reverse scale for Reward and Likeability as higher values are better
        scaled_reward = 1 - scale(data[i][2], (min_rewards, max_rewards), (0,1))
        scaled_likeability = 1 - scale(data[i][3], (min_likeability, max_likeability), (0,1))
        # reverse scale for PPml as lower values are worse
        scaled_ppml = 1 - scale(data[i][4], (min_ppml, max_ppml), (0,1))
    
        reward_color = gradient_color(scaled_reward, color_scale[0], color_scale[2])  # from green to red
        likeability_color = gradient_color(scaled_likeability, color_scale[0], color_scale[2])  # from green to red
        ppml_color = gradient_color(scaled_ppml, color_scale[2], color_scale[0])  # from red to green
    
        # Add style for color gradient
        style.add('BACKGROUND', (2,i), (2,i), reward_color)
        style.add('BACKGROUND', (3,i), (3,i), likeability_color)
        style.add('BACKGROUND', (4,i), (4,i), ppml_color)


    # set style to allow text wrapping in cells
    style.add('ALIGN', (1,1), (1,-1), 'LEFT')
    style.add('VALIGN', (1,1), (1,-1), 'TOP')
    style.add('TEXTCOLOR',(1,1),(-1,-1),colors.black)

    table.setStyle(style)

    elems = []
    elems.append(table)
    doc.build(elems)

    for file_name in df['Image URL']:
        try:
            if file_name and os.path.exists(file_name):
                os.remove(file_name)
        except Exception as e:
            print(f"Failed to remove temp image file {file_name} due to {e}")
