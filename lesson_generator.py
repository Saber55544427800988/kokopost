import sqlite3
import json
import google.generativeai as genai
from openai import OpenAI
from config import GROQ_API_KEY, GEMINI_API_KEY, DB_PATH

# Initialize Groq
groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')

def get_next_topic():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, topic, source_database, cycle FROM topics WHERE used = 0 AND source_database = 'A' ORDER BY id LIMIT 1")
    topic = cursor.fetchone()
    if not topic:
        cursor.execute("SELECT id, topic, source_database, cycle FROM topics WHERE used = 0 AND source_database = 'B' ORDER BY id LIMIT 1")
        topic = cursor.fetchone()
    if not topic:
        cursor.execute("UPDATE topics SET used = 0, cycle = cycle + 1 WHERE source_database = 'A'")
        conn.commit()
        cursor.execute("SELECT id, topic, source_database, cycle FROM topics WHERE used = 0 AND source_database = 'A' ORDER BY id LIMIT 1")
        topic = cursor.fetchone()
    conn.close()
    return topic

def generate_lesson_content(topic_text, language):
    prompt = f"""
    You are a professional language teacher for "Koko Teacher".
    Create a 30-45 second vertical video lesson for English speakers learning {language}.
    Topic: {topic_text}
    
    RULES:
    1. Main language on slides is ENGLISH
    2. Target language words shown WITH English meaning
    3. Keep slides SHORT, mobile-friendly, readable
    4. 2-3 lines per slide MAXIMUM
    5. Output MUST be valid JSON
    6. NO emojis in the JSON output
    
    SLIDE FORMAT:
    
    Slide 1 (Topic Introduction):
    - Show the English topic
    - Show target language name
    
    Slide 2 (Vocabulary - 3 words):
    - Word 1: {language} word - English meaning
    - Word 2: {language} word - English meaning  
    - Word 3: {language} word - English meaning
    
    Slide 3 (Example Phrases - 3 short examples):
    - Example 1: Short phrase in {language}
    - Example 2: Short phrase in {language}
    - Example 3: Short phrase in {language}

    JSON structure:
    {{
        "topic": "{topic_text}",
        "language": "{language}",
        "slide1": {{
            "english_topic": "[Topic in English - e.g. Ordering Food]",
            "target_language": "{language}"
        }},
        "slide2": {{
            "vocab": [
                {{"word": "[{language} word]", "meaning": "[English meaning]"}},
                {{"word": "[{language} word]", "meaning": "[English meaning]"}},
                {{"word": "[{language} word]", "meaning": "[English meaning]"}}
            ]
        }},
        "slide3": {{
            "examples": [
                {{"phrase": "[Short {language} phrase]", "meaning": "[English meaning]"}},
                {{"phrase": "[Short {language} phrase]", "meaning": "[English meaning]"}},
                {{"phrase": "[Short {language} phrase]", "meaning": "[English meaning]"}}
            ]
        }},
        "audio_script": [
            {{"voice": "en", "text": "Today we're learning about [Topic]. Let's learn some {language}!"}},
            {{"voice": "en", "text": "First word: [word 1 in English]. In {language}:"}},
            {{"voice": "native", "text": "[word 1 in {language}]"}},
            {{"voice": "en", "text": "Second word: [word 2 in English]. In {language}:"}},
            {{"voice": "native", "text": "[word 2 in {language}]"}},
            {{"voice": "en", "text": "Third word: [word 3 in English]. In {language}:"}},
            {{"voice": "native", "text": "[word 3 in {language}]"}},
            {{"voice": "en", "text": "Now some examples. Number one:"}},
            {{"voice": "native", "text": "[example 1]"}},
            {{"voice": "en", "text": "Number two:"}},
            {{"voice": "native", "text": "[example 2]"}},
            {{"voice": "en", "text": "And number three:"}},
            {{"voice": "native", "text": "[example 3]"}},
            {{"voice": "en", "text": "Great job! Keep practicing with Koko Teacher!"}}
        ]
    }}
    """
    
    # Try Gemini First
    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini failed: {e}. Falling back to Groq...")
        
    # Fallback to Groq
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Groq fallback failed: {e}")
        raise e

def mark_topic_used(topic_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE topics SET used = 1 WHERE id = ?", (topic_id,))
    conn.commit()
    conn.close()

def save_lesson(topic_id, language, lesson_data, scheduled_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO lessons (topic_id, language, script, scheduled_time) VALUES (?, ?, ?, ?)",
        (topic_id, language, json.dumps(lesson_data, ensure_ascii=False), scheduled_time)
    )
    conn.commit()
    conn.close()
