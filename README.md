# Phone Number Extractor Web Crawler

A Python-based web crawler that visits all accessible pages within a given domain and extracts unique phone numbers, formatting them consistently using the E.164 standard. It features a clean, interactive user interface built with Streamlit.

## Features
- **Same-Domain Crawling:** Ensures the crawler doesn't wander off to external websites.
- **Robust Phone Number Extraction:** Uses Google's `phonenumbers` library to find and parse both international and local phone numbers accurately.
- **`tel:` Link Support:** Captures phone numbers explicitly marked in HTML links (`href="tel:..."`).
- **Streamlit UI:** Provides a user-friendly interface to input the URL, set maximum pages to crawl, specify a default region code, and view live progress.
- **Normalization:** Outputs all found numbers in the unique E.164 format (e.g., `+14155552671`).

## Setup Instructions

### Prerequisites
- Python 3.8+

### Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd phone_number_extractor
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

2. **Interact with the UI:**
   - Open your browser to the local URL provided by Streamlit (usually `http://localhost:8501`).
   - Enter the target **Website URL** (e.g., `https://example.com`).
   - (Optional) Adjust the **Max pages to crawl**.
   - (Optional) Enter a **Default Region Code** (like `US`, `GB`, `IN`) to help the extractor parse local numbers that lack a country code.
   - Click **Start Extraction**.
  
<img width="1713" height="816" alt="image" src="https://github.com/user-attachments/assets/27ac79c0-661f-4add-a034-83c217793f35" />
<img width="1613" height="737" alt="image" src="https://github.com/user-attachments/assets/5c19acc8-d5e6-40ff-813f-9403ea4f007e" />


## How it Works
1. **`crawler.py`**: Initializes a `requests.Session` and manages a queue of URLs. It fetches a page, yields the parsed `BeautifulSoup` object, finds new links, and ensures they belong to the same domain.
2. **`extractor.py`**: Receives the `BeautifulSoup` object, searches for `tel:` links, and strips HTML to scan the raw text for phone numbers using `phonenumbers.PhoneNumberMatcher`.
3. **`app.py`**: Coordinates the crawler and extractor, rendering the progress and final unique set of numbers in a web interface.
