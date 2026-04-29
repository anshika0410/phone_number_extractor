import streamlit as st
from crawler import WebCrawler
from extractor import PhoneNumberExtractor
import time

st.set_page_config(page_title="Phone Number Extractor", page_icon="📞", layout="centered")

st.title("📞 Phone Number Extractor")
st.markdown("Crawl a website and extract all phone numbers from accessible pages within the same domain.")

# Form for user input
with st.form("extractor_form"):
    url = st.text_input("Enter Website URL", placeholder="https://example.com")
    max_pages = st.number_input("Max pages to crawl", min_value=1, max_value=500, value=50)
    region = st.text_input("Default Region Code (for local numbers)", value="US", help="e.g., US, IN, GB")
    submitted = st.form_submit_button("Start Extraction")

if submitted:
    if not url.startswith("http"):
        st.error("Please enter a valid URL starting with http:// or https://")
    else:
        st.info(f"Starting crawl for {url}...")
        
        # Initialize Crawler and Extractor
        crawler = WebCrawler(start_url=url, max_pages=max_pages)
        extractor = PhoneNumberExtractor(region=region.upper())
        
        all_numbers = set()
        
        # UI Elements for progress
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        crawled_count = 0
        try:
            # Iterate through the pages as the crawler yields them
            for current_url, soup in crawler.crawl():
                crawled_count += 1
                
                # Update progress UI
                progress_text.text(f"Crawling page {crawled_count}: {current_url}")
                # Estimate progress (can't be exact since we discover pages dynamically, but we cap at max_pages)
                progress_val = min(crawled_count / max_pages, 1.0)
                progress_bar.progress(progress_val)
                
                # Extract numbers from the current page
                numbers = extractor.extract_numbers_from_soup(soup)
                all_numbers.update(numbers)
                
            progress_bar.progress(1.0)
            progress_text.text(f"Crawling complete! Visited {crawled_count} pages.")
            
            # Display Results
            if all_numbers:
                st.success(f"Found {len(all_numbers)} unique phone number(s)!")
                
                st.subheader("Extracted Numbers")
                for num in sorted(list(all_numbers)):
                    st.code(num)
            else:
                st.warning("No phone numbers found on the crawled pages.")
                
        except Exception as e:
            st.error(f"An error occurred during crawling: {e}")
