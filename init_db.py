import sqlite3
import pandas as pd
import os

DB_PATH = 'koko_teacher.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create topics table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        topic TEXT,
        source_database TEXT,
        used BOOLEAN DEFAULT 0,
        cycle INTEGER DEFAULT 1
    )
    ''')

    # Create lessons table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER,
        language TEXT,
        script TEXT,
        scheduled_time TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        youtube_url TEXT,
        telegram_message_id TEXT,
        FOREIGN KEY (topic_id) REFERENCES topics (id)
    )
    ''')

    # Import topics from CSV (Database A)
    csv_path = 'koko post youtube and telegram/koko_teacher_10000_topics.csv'
    if os.path.exists(csv_path):
        df_a = pd.read_csv(csv_path)
        for _, row in df_a.iterrows():
            cursor.execute('INSERT INTO topics (category, topic, source_database) VALUES (?, ?, ?)',
                           (row['category'], row['topic'], 'A'))

    # Import topics from TXT (Database B)
    txt_path = 'koko post youtube and telegram/google-10000-english.txt'
    if os.path.exists(txt_path):
        with open(txt_path, 'r') as f:
            words = f.readlines()
            for word in words:
                word = word.strip()
                if word:
                    cursor.execute('INSERT INTO topics (category, topic, source_database) VALUES (?, ?, ?)',
                                   ('Vocabulary', word, 'B'))

    conn.commit()
    conn.close()
    print("Database initialized and topics imported.")

if __name__ == "__main__":
    init_db()
