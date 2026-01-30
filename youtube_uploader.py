import os
import pickle
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import CLIENT_SECRET_FILE, SCOPES

TOKEN_PICKLE = 'token.pickle'

def get_authenticated_service():
    credentials = None
    
    # Try to load from environment variable first (for GitHub Actions)
    token_b64 = os.getenv("YOUTUBE_TOKEN_B64")
    if token_b64:
        import base64
        credentials = pickle.loads(base64.b64decode(token_b64))
    
    if not credentials and os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            credentials = pickle.load(token)
            
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            # Use local server for auth
            credentials = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(credentials, token)
            
    return build('youtube', 'v3', credentials=credentials)

def upload_video(file_path, title, description, category_id="27", tags=None):
    youtube = get_authenticated_service()
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags or ["languagelearning", "shorts"],
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
        }
    }
    
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
            
    print(f"Video uploaded successfully! ID: {response['id']}")
    return f"https://www.youtube.com/shorts/{response['id']}"

if __name__ == "__main__":
    # This will trigger the auth flow if no token exists
    # Note: In the sandbox, this might require manual intervention for the first time
    print("Initializing YouTube service...")
    try:
        get_authenticated_service()
        print("YouTube service initialized.")
    except Exception as e:
        print(f"Error initializing YouTube service: {e}")
