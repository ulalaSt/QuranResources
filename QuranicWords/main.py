import sqlite3
import json

# Database file
db_name = 'wbw_database.db'

# JSON file paths
arabic_json = 'quran_wbw_uthmani.json'
position_json = 'quran_wbw_position.json'
ru_json = 'quran_wbw_ru.json'
kk_json = 'quran_wbw_kk.json'
en_json = 'quran_wbw_en.json'

# Connect to SQLite database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create the main table for Arabic words
cursor.execute('''
    CREATE TABLE IF NOT EXISTS quran_words (
        id INTEGER PRIMARY KEY,
        surah INTEGER,
        ayah INTEGER
    )
''')

# Function to create tables for each translation language
def create_translation_table(language_code):
    table_name = f'quran_words_{language_code}'
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            translation TEXT
        )
    ''')

# Function to insert data into tables
def insert_data(table_name, data):
    for word_id, translation in data.items():
        cursor.execute(f'''
            INSERT INTO {table_name} (id, translation)
            VALUES (?, ?)
        ''', (int(word_id), translation))

# Read the position JSON and insert into quran_words table
with open(position_json, 'r', encoding='utf-8') as f_pos, open(arabic_json, 'r', encoding='utf-8') as f_arb:
    positions = json.load(f_pos)
    arabic_words = json.load(f_arb)
    
    for word_id, info in positions.items():
        surah = info['surah']
        ayah = info['ayah']
        text = arabic_words[word_id]
        cursor.execute('''
            INSERT INTO quran_words (id, surah, ayah)
            VALUES (?, ?, ?)
        ''', (int(word_id), surah, ayah))

# Create tables for each translation and insert data
create_translation_table('kk')
create_translation_table('ru')
create_translation_table('en')

# Insert data into the translation tables
with open(kk_json, 'r', encoding='utf-8') as f_kk, open(ru_json, 'r', encoding='utf-8') as f_ru, open(en_json, 'r', encoding='utf-8') as f_en:
    kk_data = json.load(f_kk)
    ru_data = json.load(f_ru)
    en_data = json.load(f_en)
    
    insert_data('quran_words_kk', kk_data)
    insert_data('quran_words_ru', ru_data)
    insert_data('quran_words_en', en_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created and data inserted successfully.")
