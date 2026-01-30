from google_auth_oauthlib.flow import InstalledAppFlow
from config import CLIENT_SECRET_FILE, SCOPES

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, 
        scopes=SCOPES,
        redirect_uri='http://localhost'
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    print(f"AUTH_URL_START: {auth_url} :AUTH_URL_END")

if __name__ == "__main__":
    main()
