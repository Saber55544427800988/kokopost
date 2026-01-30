import os
import sys
import json
import time
from datetime import datetime
from lesson_generator import get_next_topic, generate_lesson_content, mark_topic_used, save_lesson
from video_generator import create_video
from youtube_uploader import upload_video
from telegram_poster import post_to_telegram
from config import SCHEDULE

def run_lesson_cycle(language):
    print(f"[{datetime.now()}] >>> KOKO TEACHER: {language.upper()} <<<")
    
    topic = get_next_topic()
    if not topic: return
    topic_id, topic_text, source, cycle = topic
    
    try:
        lesson_data = generate_lesson_content(topic_text, language)
        print(f"Lesson Data Generated successfully.")
        # Mark topic as used immediately after successful content generation
        # This prevents the same topic from repeating if video/upload fails
        mark_topic_used(topic_id)
        print(f"Topic #{topic_id} marked as used.")
    except Exception as e:
        print(f"AI Error: {e}"); return

    video_filename = f"koko_{language}_{topic_id}.mp4"
    try:
        create_video(lesson_data, language, video_filename)
        print(f"Video Created: {video_filename}")
    except Exception as e:
        print(f"Video Error: {e}"); return

    # YouTube Upload (Video)
    youtube_url = "YouTube pending auth"
    topic = lesson_data['slide1'].get('english_topic', topic_text)
    
    if os.path.exists('token.pickle'):
        try:
            title = f"Learn {language}: {topic} | Koko Teacher #shorts"
            desc = f"Learn {language} vocabulary and phrases!\n\nTopic: {topic}\n\n#languagelearning #{language.lower()} #shorts #education"
            youtube_url = upload_video(video_filename, title, desc)
        except Exception as e: 
            print(f"YouTube Error: {e}")
            youtube_url = "YouTube upload error"
    else:
        print("YouTube Token missing.")
    
    # Delete video file after upload - only keep YouTube link
    if os.path.exists(video_filename):
        os.remove(video_filename)
        print(f"Cleaned up: {video_filename}")

    # Telegram post with new format
    vocab_text = ""
    for item in lesson_data['slide2'].get('vocab', []):
        vocab_text += f"• {item['word']} = {item['meaning']}\n"
    
    examples_text = ""
    for item in lesson_data['slide3'].get('examples', []):
        examples_text += f"• {item['phrase']} ({item['meaning']})\n"
    
    telegram_text = (
        f"*{language} Lesson: {topic}*\n\n"
        f"*Vocabulary:*\n{vocab_text}\n"
        f"*Examples:*\n{examples_text}\n"
        f"[Watch Video]({youtube_url})"
    )
    post_to_telegram(telegram_text)
    
    save_lesson(topic_id, language, lesson_data, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"[{datetime.now()}] Cycle Complete.\n")

if __name__ == "__main__":
    if len(sys.argv) > 1: run_lesson_cycle(sys.argv[1])
    else:
        print("Koko Teacher Active.")
        while True:
            now = datetime.now().strftime("%H:%M")
            for lang, t in SCHEDULE.items():
                if now == t:
                    run_lesson_cycle(lang)
                    time.sleep(60)
            time.sleep(30)
