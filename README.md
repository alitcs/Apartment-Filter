# Apartment Filter Script

This Python script automates the process of filtering apartments on [apartments.com](https://www.apartments.com) based on custom search criteria and intelligently determines if a listing is truly a 2-bedroom unit. The script uses Selenium to scrape listings and OpenAI's GPT model to analyze the apartment descriptions.

---

## Project Purpose

Many listings on apartments.com are tagged as "2-bedroom" but include descriptions like "1 bedroom + den" or "1 bedroom + closet." This script helps filter out such listings by:

1. Scraping listings using Selenium based on a user-defined apartments.com URL.
2. Sending each listing’s description to a GPT model.
3. Asking the model if the apartment is **actually** a 2-bedroom.
4. Storing valid apartment URLs in a `URLs.json` file.
5. Tagging newly discovered listings with `"NEW: "`.

---

## Setup Instructions

To run this script, make sure you have:

- Python 3.8 or later
- [Google Chrome browser](https://www.google.com/chrome/)
- ChromeDriver (automatically managed via `webdriver-manager`)
- An OpenAI API key
- Installed the following packages:
  - `selenium`
  - `webdriver-manager`
  - `openai`

You can install them via:

```
pip install selenium webdriver-manager openai
```

---

## Files Included

- `apartments.py`: The main script file.
- `URLs.json`: A JSON file that stores the URLs of valid 2-bedroom apartments (initially just an empty list `[]`).

---

## How to Use

1. Go to [apartments.com](https://www.apartments.com) and apply your preferred filters (e.g. city, price range, bedrooms).
2. Copy the filtered URL and replace the one in the `driver.get(...)` line inside `apartments.py`.
3. Include your own actual OpenAI API key.
4. Run the script:

```
python apartments.py
```

5. The script will:
   - Navigate through all listings
   - Ask GPT if each apartment is truly 2 bedrooms
   - Save matching URLs to `URLs.json`
   - Mark newly found listings with `"NEW: "` above the link

6. You can run the script again later. It will keep previously saved URLs and only mark new ones.

---

## AI Usage

This script uses the `gpt-3.5-turbo` model from OpenAI to evaluate apartment descriptions. It sends a prompt asking whether the description reflects a **true** 2-bedroom apartment. The AI replies either **Yes** or **No**, and the script filters accordingly.

---

## Notes

- This script is customized for **apartments.com** only.
- No license is included — intended for personal use.

