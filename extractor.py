import phonenumbers
from bs4 import BeautifulSoup

class PhoneNumberExtractor:
    def __init__(self, region='US'):
        """
        Initialize the extractor.
        :param region: The default region code (e.g., 'US', 'IN', 'GB') used for parsing
                       numbers that are not in international format (+...).
        """
        self.region = region

    def extract_text_from_html(self, soup):
        """
        Extract clean text from a BeautifulSoup object, removing scripts and styles.
        """
        # Kill all script and style elements
        for element in soup(["script", "style", "noscript", "meta", "header", "footer"]):
            element.extract()

        # Get text
        text = soup.get_text(separator=' ')
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text

    def extract_numbers_from_text(self, text):
        """
        Finds all phone numbers in the given text and returns them in E.164 format.
        """
        unique_numbers = set()
        
        # Use phonenumbers.PhoneNumberMatcher to find valid numbers in the text
        for match in phonenumbers.PhoneNumberMatcher(text, self.region):
            formatted_number = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E.164)
            unique_numbers.add(formatted_number)
            
        return unique_numbers

    def extract_numbers_from_soup(self, soup):
        """
        Extracts numbers from both visible text and 'tel:' links in the soup.
        """
        numbers = set()
        
        # 1. Extract from 'tel:' links (highly reliable)
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('tel:'):
                raw_number = href.replace('tel:', '').strip()
                try:
                    parsed = phonenumbers.parse(raw_number, self.region)
                    if phonenumbers.is_valid_number(parsed):
                        numbers.add(phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E.164))
                except phonenumbers.NumberParseException:
                    pass
        
        # 2. Extract from visible text
        text = self.extract_text_from_html(soup)
        numbers.update(self.extract_numbers_from_text(text))
        
        return numbers
