API = "http://localhost:8000/translate"
import requests
import sqlite3

# setup sqlite
conn = sqlite3.connect('translations.db')
cursor = conn.cursor()

# create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    translated TEXT
)
''')

with open('The_Oxford_3000.txt', 'r', encoding='utf-8') as words:
    for word in words:
        word = word.strip()
        data = {"text": word,
                "to": "th"
            }
        response = requests.post(f'{API}', json=data)
        if response.status_code == 200:
            result = response.json()
            translated_word = result["translatedText"]

            cursor.execute('''
            INSERT INTO translations (word, translated)
            VALUES (?, ?)
            ''', (word, translated_word))

            conn.commit()

conn.close()
print("Translation completed and saved in database.")