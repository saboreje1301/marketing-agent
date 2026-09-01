from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/webmasters"
]

BASE_DIR = Path(__file__).resolve().parent

CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"


def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
    )

    credentials = flow.run_local_server(
        port=8080,
        access_type="offline",
        prompt="consent",
    )

    print("\n================================")
    print("ACCESS TOKEN:")
    print(credentials.token)
    print("================================\n")
    
    if credentials.refresh_token:
        print("REFRESH TOKEN (guárdalo en un lugar seguro):")
        print(credentials.refresh_token)
        print("================================\n")


if __name__ == "__main__":
    main()
