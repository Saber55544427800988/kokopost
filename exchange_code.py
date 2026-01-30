import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from config import CLIENT_SECRET_FILE, SCOPES

def main():
    # The code provided by the user
    auth_code = "4/0ASc3gC0XRroduV-3glmMOWaKJYdVgXX9Gi006wQCAbEc5UtLVRxDQC8thn_sQsg13Sep9g"
    
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, 
        scopes=SCOPES,
        redirect_uri='http://localhost'
    )
    
    # Exchange the code for credentials
    flow.fetch_token(code=auth_code)
    credentials = flow.credentials
    
    # Save the credentials to token.pickle
    with open('token.pickle', 'wb') as token:
        pickle.dump(credentials, token)
    
    print("SUCCESS: token.pickle has been generated.")

if __name__ == "__main__":
    main()
