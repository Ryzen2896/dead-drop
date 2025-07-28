from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pyperclip
import time
import os

UPLOAD_URL = "https://issacos.online/index.php"  # Your upload page

def upload_with_captcha(filepath):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get(UPLOAD_URL)

    try:
        # Wait for file input to be present and visible
        file_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.NAME, "file"))
        )

        # Send the absolute file path
        abs_path = os.path.abspath(filepath)
        file_input.send_keys(abs_path)
        print(f"Selected file: {abs_path}")

        # Wait for the submit button (input or button) to be clickable
        submit_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'], button[type='submit']"))
        )

        print("Please solve the CAPTCHA in the browser window and submit the form.")

        # Now wait for the URL to change indicating successful upload and redirect
        WebDriverWait(driver, 300).until(
            EC.url_contains("index.php?link=")
        )

        # Once URL contains the link param, extract it
        current_url = driver.current_url
        print(f"Upload complete! Redirected to: {current_url}")

        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(current_url)
        query = parse_qs(parsed.query)
        link = query.get('link', [None])[0]

        if link:
            print(f"Download link: {link}")
            pyperclip.copy(link)
            print("Link copied to clipboard!")
        else:
            print("Download link parameter not found in URL.")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Optionally add a delay to let user see the final page before quit
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    Tk().withdraw()
    filepath = askopenfilename()
    if filepath:
        upload_with_captcha(filepath)
    else:
        print("No file selected.")