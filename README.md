# 🎓 Koko Teacher - Automated Language Learning Video Generator

**Koko Teacher** is an automated system that generates professional vertical video lessons for English speakers learning Spanish, French, or Chinese. Videos are optimized for YouTube Shorts, Instagram Reels, and TikTok.

---

## 🎥 Video Format

All videos follow a standardized **3-slide vertical format**:

### Video Specifications
- **Resolution**: 1080x1920 (vertical/portrait)
- **Duration**: 30-45 seconds
- **Background**: Dark gradients (professional, eye-friendly)
- **Font**: Large, bold, sans-serif
- **Audio**: Male English TTS + Native language TTS

### Slide Structure
1. **Slide 1**: Topic Introduction (5-10s)
   - English topic
   - Target language name
   
2. **Slide 2**: Vocabulary (15-20s)
   - 3 key words with English meanings
   
3. **Slide 3**: Examples (15-20s)
   - 3 practical phrases with translations

📖 **See [VIDEO_FORMAT_SPEC.md](VIDEO_FORMAT_SPEC.md) for complete format documentation**

---

## 🚀 Features

✅ **Automated Content Generation** - AI-powered lesson creation using Gemini/Groq  
✅ **Multi-Language Support** - Spanish, French, Chinese  
✅ **Professional TTS** - Male voices for English and native languages  
✅ **YouTube Integration** - Automatic upload with metadata  
✅ **Telegram Notifications** - Post lessons to Telegram channel  
✅ **Scheduled Publishing** - Automated daily lessons  
✅ **Database Tracking** - Topic rotation and lesson history  

---

## 📁 Project Structure

```
koko_teacher_ABSOLUTE_FINAL/
├── main.py                      # Main orchestration script
├── lesson_generator.py          # AI lesson content generation
├── video_generator.py           # Main video creation (3-slide format)
├── generate_special_video.py   # Special/custom video generation
├── youtube_uploader.py          # YouTube API integration
├── telegram_poster.py           # Telegram bot integration
├── config.py                    # Configuration and API keys
├── init_db.py                   # Database initialization
├── koko_teacher.db              # SQLite database
├── VIDEO_FORMAT_SPEC.md         # Complete video format documentation
├── SETUP_GUIDE.md               # Original setup instructions
└── README.md                    # This file
```

---

## 🛠️ Installation

### 1. Install Dependencies

```bash
pip install moviepy edge-tts google-generativeai Pillow openai
```

### 2. Configure API Keys

Edit `config.py` and add your API keys:

```python
GROQ_API_KEY = "your_groq_api_key"
GEMINI_API_KEY = "your_gemini_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "@your_channel"
```

### 3. Initialize Database

```bash
python3 init_db.py
```

This creates the SQLite database with topics for Spanish, French, and Chinese.

### 4. Setup YouTube Authentication (Optional)

```bash
# Get authorization URL
python3 get_auth_url.py

# Exchange code for token
python3 exchange_code.py
```

---

## 📖 Usage

### Automated Daily Lessons

Run the main script to start automated lesson generation:

```bash
python3 main.py
```

**Schedule** (configured in `config.py`):
- **Spanish**: 09:00
- **French**: 19:00
- **Chinese**: 00:00

### Generate Single Lesson

Generate a lesson for a specific language:

```bash
python3 main.py Spanish
python3 main.py French
python3 main.py Chinese
```

### Generate Special Video

Create a custom lesson video:

```bash
python3 generate_special_video.py
```

This generates a special lesson based on the prompt in the script (currently: "Ordering Coffee" in Spanish).

---

## 🎬 Video Generation Process

1. **Content Generation**
   - AI generates lesson content (topic, vocabulary, examples, audio script)
   - Uses Gemini API (primary) with Groq fallback
   
2. **Audio Creation**
   - Generates TTS for each audio segment
   - Alternates between English and native language
   - Uses male voices: `en-US-GuyNeural`, `es-ES-AlvaroNeural`, etc.
   
3. **Video Assembly**
   - Creates 3 slides with gradient backgrounds
   - Adds text overlays (large, bold, readable)
   - Synchronizes audio with slide transitions
   
4. **Publishing**
   - Uploads to YouTube with metadata
   - Posts to Telegram with lesson summary
   - Saves to database for tracking

---

## 🎨 Customization

### Change Video Settings

Edit `config.py`:

```python
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FONT_SIZE = 60
MAX_LINES_PER_SLIDE = 4
```

### Modify Lesson Schedule

Edit `config.py`:

```python
SCHEDULE = {
    "Spanish": "09:00",
    "French": "19:00",
    "Chinese": "00:00"
}
```

### Customize Slide Design

Edit `video_generator.py` or `generate_special_video.py`:

- **Backgrounds**: Modify `create_gradient_background()` color values
- **Fonts**: Change font sizes in `create_slide1()`, `create_slide2()`, `create_slide3()`
- **Layout**: Adjust text positions (y_pos values)

### Change TTS Voices

Edit the `VOICES` dictionary in `video_generator.py`:

```python
VOICES = {
    "en": "en-US-GuyNeural",
    "Spanish": "es-ES-AlvaroNeural",
    "French": "fr-FR-HenriNeural",
    "Chinese": "zh-CN-YunxiNeural"
}
```

Browse available voices: https://speech.microsoft.com/portal/voicegallery

---

## 📊 Database Structure

### Topics Table
- `id`: Unique identifier
- `topic`: Topic name (e.g., "Ordering Food")
- `source_database`: A or B (for rotation)
- `used`: 0 or 1 (tracking usage)
- `cycle`: Number of times rotated

### Lessons Table
- `id`: Unique identifier
- `topic_id`: Foreign key to topics
- `language`: Spanish, French, or Chinese
- `script`: JSON lesson data
- `scheduled_time`: When the lesson was generated

---

## 🔧 Troubleshooting

### Font Not Found Error

The app automatically detects fonts. If you encounter font errors:

**Linux**:
```bash
sudo apt-get install fonts-liberation fonts-dejavu
```

**Windows**: Fonts should be pre-installed

### Audio Generation Fails

Ensure `edge-tts` is installed and you have internet connection:
```bash
pip install --upgrade edge-tts
```

### Video Too Long

Adjust audio script length in `lesson_generator.py` or reduce slide durations in `video_generator.py`.

### YouTube Upload Fails

1. Check `token.pickle` exists
2. Verify `client_secret.json` is valid
3. Re-authenticate: `python3 get_auth_url.py`

---

## 📝 Format Compliance Checklist

Before publishing videos, verify:

- [ ] Resolution: 1080x1920 (vertical)
- [ ] Duration: 30-45 seconds
- [ ] 3 slides with correct layout
- [ ] English as primary language on slides
- [ ] Target language words with English meanings
- [ ] Male TTS voices only
- [ ] Dark gradient backgrounds
- [ ] Large, readable fonts (min 32px)
- [ ] @KokoTeacher branding on all slides
- [ ] No emojis in video content

---

## 🤝 Contributing

To maintain format consistency:

1. Read [VIDEO_FORMAT_SPEC.md](VIDEO_FORMAT_SPEC.md) thoroughly
2. Update **both** `video_generator.py` and `generate_special_video.py`
3. Test with all 3 languages
4. Verify mobile viewing experience
5. Update documentation

---

## 📄 License

This project is for educational purposes. Ensure you have proper rights for any content you publish.

---

## 📞 Support

For issues or questions:
- Check [VIDEO_FORMAT_SPEC.md](VIDEO_FORMAT_SPEC.md) for format details
- Review [SETUP_GUIDE.md](SETUP_GUIDE.md) for setup instructions
- Test with `test_format.py` to validate lesson structure

---

## 🎯 Roadmap

- [ ] Add more languages (German, Italian, Japanese)
- [ ] Instagram Reels integration
- [ ] TikTok auto-posting
- [ ] Web dashboard for monitoring
- [ ] Custom branding options
- [ ] A/B testing for different formats

---

**Version**: 2.0 (Standardized 3-Slide Format)  
**Last Updated**: January 30, 2026  
**Status**: ✅ Production Ready

---

## 🎓 Example Lesson

**Topic**: Ordering Food (Spanish)

**Slide 1**:
```
🎓 KOKO TEACHER
Topic: Ordering Food
Learning: SPANISH
```

**Slide 2**:
```
VOCABULARY
1. Menú = Menu
2. Cuenta = Bill
3. Camarero = Waiter
```

**Slide 3**:
```
EXAMPLES
1. Quisiera el menú (I would like the menu)
2. La cuenta, por favor (The bill, please)
3. ¿Qué recomienda? (What do you recommend?)
Follow for more!
```

**Duration**: ~35 seconds  
**Audio**: Alternating English narration and Spanish pronunciation

---

**Made with ❤️ by Koko Teacher Team**
