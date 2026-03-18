import json
import sqlite3

# Load the data from the JSON files
with open('pals_data.json', 'r') as file:
    pals_data = json.load(file)

with open('pals_skill_details.json', 'r') as file:
    skills_data = json.load(file)

# Merge the data from the two JSON files
merged_data = []
for pal in pals_data:
    pal_name = pal['name']
    skills = next((item['skills'] for item in skills_data if item['name'] == pal_name), [])
    pal['skills'] = skills
    merged_data.append(pal)

# Connect to SQLite database
conn = sqlite3.connect('pals_database.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS pals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    img_src TEXT,
    hp TEXT,
    defense TEXT,
    attack TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS elements (
    type TEXT PRIMARY KEY,
    img_src TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS skills (
    name TEXT PRIMARY KEY,
    element TEXT,
    power TEXT,
    cooldown TEXT,
    range TEXT,
    element_link TEXT,
    FOREIGN KEY (element_link) REFERENCES elements(type)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pal_skills (
    pal_id INTEGER,
    skill_name TEXT,
    FOREIGN KEY (pal_id) REFERENCES pals(id),
    FOREIGN KEY (skill_name) REFERENCES skills(name),
    PRIMARY KEY (pal_id, skill_name)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pal_elements (
    pal_id INTEGER,
    element_type TEXT,
    FOREIGN KEY (pal_id) REFERENCES pals(id),
    FOREIGN KEY (element_type) REFERENCES elements(type),
    PRIMARY KEY (pal_id, element_type)
)
''')

# Insert data into the database
for pal in merged_data:
    cursor.execute('''
    INSERT INTO pals (name, img_src, hp, defense, attack) 
    VALUES (?, ?, ?, ?, ?)
    ''', (pal['name'], pal['img_src'], pal['hp'], pal['defense'], pal['attack']))
    
    pal_id = cursor.lastrowid
    
    for element in pal['elements']:
        cursor.execute('''
        INSERT OR IGNORE INTO elements (type, img_src)
        VALUES (?, ?)
        ''', (element['type'], element['img_src']))
        
        cursor.execute('''
        INSERT INTO pal_elements (pal_id, element_type)
        VALUES (?, ?)
        ''', (pal_id, element['type']))
    
    for skill in pal['skills']:
        element_link = f"https://palworld.gg/{skill['element']}"
        cursor.execute('''
        INSERT OR IGNORE INTO skills (name, element, power, cooldown, range, element_link)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (skill['name'], skill['element'], skill['power'], skill['cooldown'], skill['range'], element_link))
        
        cursor.execute('''
        INSERT INTO pal_skills (pal_id, skill_name)
        VALUES (?, ?)
        ''', (pal_id, skill['name']))

# Commit the changes and close the connection
conn.commit()
conn.close()

print('Database created and data inserted successfully.')


























