import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebCrawler:
    def __init__(self, start_url, max_pages=50):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.domain = urlparse(start_url).netloc
        self.session = requests.Session()
        # Use a realistic User-Agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def is_same_domain(self, url):
        return urlparse(url).netloc == self.domain

    def get_links(self, soup, current_url):
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(current_url, href)
            # Remove URL fragments
            full_url = full_url.split('#')[0]
            
            # Ensure it's http/https and on the same domain
            if full_url.startswith('http') and self.is_same_domain(full_url):
                links.add(full_url)
        return links

    def crawl(self):
        queue = [self.start_url]
        pages_crawled = 0

        while queue and pages_crawled < self.max_pages:
            current_url = queue.pop(0)
            
            if current_url in self.visited_urls:
                continue
                
            self.visited_urls.add(current_url)
            logging.info(f"Crawling: {current_url}")
            
            try:
                response = self.session.get(current_url, timeout=10)
                # Skip non-HTML content (like PDFs, images)
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    continue
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Yield the URL and the parsed soup
                yield current_url, soup
                
                new_links = self.get_links(soup, current_url)
                for link in new_links:
                    if link not in self.visited_urls and link not in queue:
                        queue.append(link)
                        
                pages_crawled += 1
                
            except requests.RequestException as e:
                logging.error(f"Failed to fetch {current_url}: {e}")
