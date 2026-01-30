import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def post_to_telegram(text, video_path=None):
    """
    As per user request: Post lesson as TEXT to Telegram.
    Video is reserved for YouTube.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': TELEGRAM_CHAT_ID, 
        'text': text, 
        'parse_mode': 'Markdown',
        'disable_web_page_preview': False
    }
    try:
        response = requests.post(url, data=data)
        res_json = response.json()
        if not res_json.get('ok'):
            print(f"Telegram Text Error: {res_json}")
        return res_json
    except Exception as e:
        print(f"Telegram Connection Error: {e}")
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    # Test post
    test_text = "🤖 *Koko Teacher Test*\nThis is a test message (text-only)."
    print(post_to_telegram(test_text))
