import json
import os
import requests
import sqlite3
from PIL import Image
from io import BytesIO

# Load the JSON data
with open('pals_data.json', 'r') as file:
    pals_data = json.load(file)

# Create a directory to store the images
os.makedirs('images', exist_ok=True)

# Connect to SQLite database (or create it)
conn = sqlite3.connect('pals.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS pals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    img_src TEXT,
    local_img_path TEXT,
    base_hp INTEGER,
    base_defense INTEGER,
    base_att INTEGER
)
''')

# Function to download an image and return the local path
def download_image(url, name):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    local_path = os.path.join('images', f'{name}.png')
    img.save(local_path)
    return local_path

# Insert data into the database
for pal in pals_data:
    name = pal['name']
    img_src = pal['img_src']
    local_img_path = download_image(img_src, name)
    base_hp = int(pal['hp'])
    base_defense = int(pal['defense'])
    base_att = int(pal['attack'])
    
    cursor.execute('''
    INSERT INTO pals (name, img_src, local_img_path, base_hp, base_defense, base_att)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, img_src, local_img_path, base_hp, base_defense, base_att))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data and images have been successfully stored.")


