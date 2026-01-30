# Koko Teacher - Final Setup Guide

The "Koko Teacher" app is now fully optimized with high-quality video generation and the specific posting requirements you requested.

## 1. Final Workflow
- **YouTube Shorts**: Posts high-quality vertical videos with gradient backgrounds, professional fonts, and accurate TTS.
- **Telegram**: Posts the lesson as **text only** (with a link to the YouTube video) to keep the channel clean.
- **Languages**: Spanish, French, and Chinese (with correct character encoding).

## 2. YouTube Authentication (Mandatory)
Before the first automated post, you must authorize the YouTube API:
1. Run: `python3 youtube_uploader.py`
2. Follow the link provided, log in to your YouTube account, and grant permissions.
3. This will create a `token.pickle` file, which the app uses for future automated uploads.

## 3. Running the App
To start the daily automation:
```bash
cd /home/ubuntu/koko_teacher
python3 main.py
```
The schedule is:
- **09:00 AM**: Spanish
- **07:00 PM**: French
- **12:00 AM**: Chinese

## 4. Manual Trigger
To post a lesson immediately for testing:
```bash
python3 main.py Spanish
python3 main.py French
python3 main.py Chinese
```

## 5. Improvements Made
- **Visuals**: Replaced static black screens with professional gradient backgrounds.
- **Encoding**: Fixed character corruption (e.g., "Buenos días" instead of "Buenos dXas").
- **Pronunciation**: Improved AI prompts to ensure natural pronunciation guides.
- **Platform Specifics**: Video for YouTube, Text for Telegram.
