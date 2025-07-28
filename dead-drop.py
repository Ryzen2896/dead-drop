import requests
import pyperclip
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from urllib.parse import urlparse, parse_qs

UPLOAD_URL = "https://issacos.online/drop.php"

def upload_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(UPLOAD_URL, files=files, allow_redirects=False)

        if response.status_code in (302, 303):
            redirect_url = response.headers.get('Location')
            if redirect_url:
                parsed = urlparse(redirect_url)
                query = parse_qs(parsed.query)
                link = query.get('link', [None])[0]
                if link:
                    print(f"Uploaded! Link: {link}")
                    pyperclip.copy(link)
                    print("Link copied to clipboard!")
                    return True
        print("Upload failed or unexpected response.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Hide the main Tk window
    Tk().withdraw()

    print("Select a file to upload...")
    filepath = askopenfilename()

    if not filepath:
        print("No file selected. Exiting.")
    else:
        upload_file(filepath)