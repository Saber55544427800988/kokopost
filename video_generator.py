import os
import sys
import asyncio
import edge_tts
import numpy as np
from moviepy import TextClip, AudioFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips, concatenate_audioclips
from config import VIDEO_WIDTH, VIDEO_HEIGHT
from PIL import Image, ImageDraw

# Voice mapping - Male voices
VOICES = {
    "en": "en-US-GuyNeural",
    "Spanish": "es-ES-AlvaroNeural",
    "French": "fr-FR-HenriNeural",
    "Chinese": "zh-CN-YunxiNeural"
}

# Language flags
FLAGS = {
    "Spanish": "ES",
    "French": "FR", 
    "Chinese": "CN"
}

# Cross-platform font
def get_font_path():
    if sys.platform == "win32":
        candidates = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    for font in candidates:
        if os.path.exists(font):
            return font
    return None

FONT_PATH = get_font_path()

async def generate_tts_segment(text, voice, output_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def create_gradient_background(width, height, color_top, color_bottom):
    """Create smooth gradient background"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def create_slide1(topic, language, duration):
    """Slide 1: Topic Introduction"""
    # Dark blue gradient
    bg = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, (20, 30, 70), (10, 15, 40))
    bg_path = "temp_bg1.png"
    bg.save(bg_path)
    bg_clip = ImageClip(bg_path).with_duration(duration)
    
    clips = [bg_clip]
    
    # Title "KOKO TEACHER"
    title = TextClip(
        text="KOKO TEACHER",
        font_size=60,
        color='yellow',
        font=FONT_PATH,
        method='label',
        margin=(20, 20)
    ).with_duration(duration).with_position(('center', 250))
    clips.append(title)
    
    # English Topic label
    topic_label = TextClip(
        text="Topic:",
        font_size=48,
        color='#CCCCCC',
        font=FONT_PATH,
        method='label',
        margin=(10, 10)
    ).with_duration(duration).with_position(('center', 550))
    clips.append(topic_label)
    
    # Topic text
    topic_text = TextClip(
        text=topic,
        font_size=50,
        color='white',
        font=FONT_PATH,
        method='caption',
        size=(VIDEO_WIDTH - 200, None),
        text_align='center',
        margin=(20, 20)
    ).with_duration(duration).with_position(('center', 650))
    clips.append(topic_text)
    
    # Target Language label
    lang_label = TextClip(
        text="Learning:",
        font_size=48,
        color='#CCCCCC',
        font=FONT_PATH,
        method='label',
        margin=(10, 10)
    ).with_duration(duration).with_position(('center', 850))
    clips.append(lang_label)
    
    # Language name
    lang_text = TextClip(
        text=language.upper(),
        font_size=65,
        color='#00BFFF',
        font=FONT_PATH,
        method='label',
        margin=(20, 20)
    ).with_duration(duration).with_position(('center', 950))
    clips.append(lang_text)
    
    # Branding
    brand = TextClip(
        text="@KokoTeacher",
        font_size=36,
        color='#888888',
        font=FONT_PATH,
        method='label',
        margin=(10, 10)
    ).with_duration(duration).with_position(('center', VIDEO_HEIGHT - 120))
    clips.append(brand)
    
    return CompositeVideoClip(clips, size=(VIDEO_WIDTH, VIDEO_HEIGHT)), bg_path

def create_slide2(vocab_list, language, duration):
    """Slide 2: Vocabulary (3 words)"""
    # Teal gradient
    bg = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, (15, 50, 70), (10, 30, 45))
    bg_path = "temp_bg2.png"
    bg.save(bg_path)
    bg_clip = ImageClip(bg_path).with_duration(duration)
    
    clips = [bg_clip]
    
    # Title
    title = TextClip(
        text="VOCABULARY",
        font_size=60,
        color='yellow',
        font=FONT_PATH,
        method='label',
        margin=(20, 20)
    ).with_duration(duration).with_position(('center', 250))
    clips.append(title)
    
    # Vocabulary items - centered layout
    y_pos = 500
    
    for i, item in enumerate(vocab_list[:3]):
        word = item.get('word', '')
        meaning = item.get('meaning', '')
        
        # Combined text: "1. Word"
        line_text = f"{i+1}.  {word}"
        line_clip = TextClip(
            text=line_text,
            font_size=46,
            color='white',
            font=FONT_PATH,
            method='caption',
            size=(VIDEO_WIDTH - 250, None),
            text_align='center',
            margin=(20, 20)
        ).with_duration(duration).with_position(('center', y_pos))
        clips.append(line_clip)
        
        # Meaning on next line - Increased offset to y_pos + 90 (was +70)
        meaning_clip = TextClip(
            text=f"= {meaning}",
            font_size=36,
            color='#00BFFF',
            font=FONT_PATH,
            method='caption',
            size=(VIDEO_WIDTH - 250, None),
            text_align='center',
            margin=(20, 20)
        ).with_duration(duration).with_position(('center', y_pos + 90))
        clips.append(meaning_clip)
        
        # Increased spacing between items to 220 (was 200)
        y_pos += 220
    
    # Branding
    brand = TextClip(
        text="@KokoTeacher",
        font_size=36,
        color='#888888',
        font=FONT_PATH,
        method='label',
        margin=(10, 10)
    ).with_duration(duration).with_position(('center', VIDEO_HEIGHT - 120))
    clips.append(brand)
    
    return CompositeVideoClip(clips, size=(VIDEO_WIDTH, VIDEO_HEIGHT)), bg_path

def create_slide3(examples_list, language, duration):
    """Slide 3: Example Phrases"""
    # Purple gradient
    bg = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, (50, 25, 70), (25, 15, 45))
    bg_path = "temp_bg3.png"
    bg.save(bg_path)
    bg_clip = ImageClip(bg_path).with_duration(duration)
    
    clips = [bg_clip]
    
    # Title
    title = TextClip(
        text="EXAMPLES",
        font_size=60,
        color='yellow',
        font=FONT_PATH,
        method='label',
        margin=(20, 20)
    ).with_duration(duration).with_position(('center', 250))
    clips.append(title)
    
    # Example items - centered
    y_pos = 500
    
    for i, item in enumerate(examples_list[:3]):
        phrase = item.get('phrase', '')
        meaning = item.get('meaning', '')
        
        # Phrase line
        line_text = f"{i+1}.  {phrase}"
        phrase_clip = TextClip(
            text=line_text,
            font_size=42,
            color='white',
            font=FONT_PATH,
            method='caption',
            size=(VIDEO_WIDTH - 250, None),
            text_align='center',
            margin=(20, 20)
        ).with_duration(duration).with_position(('center', y_pos))
        clips.append(phrase_clip)
        
        # Meaning - Increased offset to y_pos + 80 (was +60)
        meaning_clip = TextClip(
            text=f"({meaning})",
            font_size=32,
            color='#FF9999',
            font=FONT_PATH,
            method='caption',
            size=(VIDEO_WIDTH - 250, None),
            text_align='center',
            margin=(20, 20)
        ).with_duration(duration).with_position(('center', y_pos + 80))
        clips.append(meaning_clip)
        
        # Increased spacing between items to 200 (was 180)
        y_pos += 200
    
    # Call to action
    cta = TextClip(
        text="Follow for more!",
        font_size=42,
        color='yellow',
        font=FONT_PATH,
        method='label',
        margin=(20, 20)
    ).with_duration(duration).with_position(('center', VIDEO_HEIGHT - 200))
    clips.append(cta)
    
    # Branding
    brand = TextClip(
        text="@KokoTeacher",
        font_size=36,
        color='#888888',
        font=FONT_PATH,
        method='label',
        margin=(10, 10)
    ).with_duration(duration).with_position(('center', VIDEO_HEIGHT - 120))
    clips.append(brand)
    
    return CompositeVideoClip(clips, size=(VIDEO_WIDTH, VIDEO_HEIGHT)), bg_path

def create_video(lesson_data, language, output_path):
    """Create the complete video with new format"""
    
    # 1. Generate all audio segments
    audio_segments = []
    native_voice = VOICES.get(language, VOICES["en"])
    
    for i, part in enumerate(lesson_data['audio_script']):
        seg_path = f"seg_{i}.mp3"
        voice = VOICES["en"] if part['voice'] == "en" else native_voice
        asyncio.run(generate_tts_segment(part['text'], voice, seg_path))
        audio_segments.append(AudioFileClip(seg_path))
    
    # Combine all audio
    full_audio = concatenate_audioclips(audio_segments)
    full_audio.write_audiofile("temp_full.mp3", logger=None)
    final_audio = AudioFileClip("temp_full.mp3")
    
    # 2. Calculate slide durations based on audio
    total_duration = final_audio.duration
    
    # Intro (segment 0)
    s1_dur = audio_segments[0].duration + 1.5
    
    # Vocabulary (segments 1-6)
    s2_dur = sum(seg.duration for seg in audio_segments[1:7]) + 1.0
    
    # Examples (segments 7+)
    s3_dur = total_duration - s1_dur - s2_dur + 1.5
    if s3_dur < 5:
        s3_dur = 5
    
    # 3. Create slides
    topic = lesson_data['slide1'].get('english_topic', lesson_data.get('topic', 'Topic'))
    vocab = lesson_data['slide2'].get('vocab', [])
    examples = lesson_data['slide3'].get('examples', [])
    
    c1, b1 = create_slide1(topic, language, s1_dur)
    c2, b2 = create_slide2(vocab, language, s2_dur)
    c3, b3 = create_slide3(examples, language, s3_dur)
    
    # 4. Combine video and audio
    final_video = concatenate_videoclips([c1, c2, c3]).with_audio(final_audio)
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
    
    # 5. Cleanup all temp files
    temp_files = ["temp_full.mp3", "temp_bg1.png", "temp_bg2.png", "temp_bg3.png"]
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
    for i in range(len(lesson_data['audio_script'])):
        if os.path.exists(f"seg_{i}.mp3"):
            os.remove(f"seg_{i}.mp3")
    
    return output_path
