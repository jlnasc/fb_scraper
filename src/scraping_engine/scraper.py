import re
import os
import configparser
from bs4 import BeautifulSoup
from scraping_engine.facebook_post import FacebookPost
from scraping_engine.post_exporter import FacebookPostExporter, InfoFileExporter

"""
Create a Scraper class responsible for handling the web scraping logic. 
It will fetch and parse the HTML content of the website to extract Facebook posts and their associated information. 
It will create instances of the FacebookPost class for each found post.
"""
class Scraper:
    
    def __init__(self, html_source_path):
        self.html_source_path = html_source_path
        self.html_file = None
        self.posts = None
        
        self.config = configparser.ConfigParser()

        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scraper_config.ini')
        self.config.read(config_path, encoding='utf-8')

        self.FACEBOOK_POST_CLASS_ID    = self.config['ScraperConfiguration']['FACEBOOK_POST_CLASS_ID']
        self.POST_TEXT_FATHER_CLASS_ID = self.config['ScraperConfiguration']['POST_TEXT_FATHER_CLASS_ID']
        self.POST_ACCOUNT_CLASS_ID     = self.config['ScraperConfiguration']['POST_ACCOUNT_CLASS_ID']
        self.POST_TEXT_CLASS_ID        = self.config['ScraperConfiguration']['POST_TEXT_CLASS_ID']
        self.POST_LINK_CLASS_ID        = self.config['ScraperConfiguration']['POST_LINK_CLASS_ID']
        self.POST_LIKES_CLASS_ID       = self.config['ScraperConfiguration']['POST_LIKES_CLASS_ID']
        
    def load_html_file(self):
        try:
            with open(self.html_source_path, encoding="utf8") as html_file:
                print("Loading the data ...")
                self.html_file = BeautifulSoup(html_file, "lxml")
        except Exception as error:
            print(f"An error occurred while loading the file: {error}")
            
    def get_facebook_posts(self):
        self.posts = self.html_file.find_all("div", class_=self.FACEBOOK_POST_CLASS_ID)
        return self.posts
        
    def scrape_facebook_post(self, post):
        # Process the post's link, text, date, likes
        link = self.process_post_link(post)
        account = self.process_post_account(post)
        text = self.process_post_text(post)
        date = self.process_post_date(text)
        likes = self.process_post_likes(post)
        # Create a new FacebookPost instance using the processed data
        return FacebookPost(link, account, text, date, likes)
    
    def find_text_div_elements(self, post):
        #return post.find_all("div", class_=self.POST_TEXT_FATHER_CLASS_ID)
        return post.find_all("span", class_=self.POST_TEXT_CLASS_ID)
    
    def process_post_account(self, post):
        strong_element = post.find("strong")
        if strong_element:
            return strong_element.get_text().strip()
        return None
    
    def process_post_link(self, post):
        link_element = post.find("a", class_=self.POST_LINK_CLASS_ID, attrs={"href": True})
        if link_element:
            unprocessed_link = link_element.get("href")
            return self.extract_link_from_element(unprocessed_link)
        return None

    def extract_link_from_element(self, unprocessed_link):
        link = unprocessed_link
        if '&set=' in unprocessed_link:
            link = unprocessed_link.split('&set=')[0]
        return link
            
    def process_post_text(self, post):
        text_div_elements = self.find_text_div_elements(post)
        for text_element in text_div_elements:
            if text_element:
                poem_text = text_element.get_text().strip()  # Remove explicit whitespace characters
                if poem_text and len(poem_text) > 40: #and '.com' not in poem_text 
                    return poem_text
        return None
    
    def process_post_date(self, poem_text):
        if poem_text and '.com' not in poem_text:
            return self.extract_date_from_text(poem_text)
        return None

    def extract_date_from_text(self, text):
        date_pattern = r"[0-9]{1,4}[\_|\-|\/|\|][0-9]{1,2}[\_|\-|\/|\|][0-9]{1,4}"  # Regular expression to match date patterns in the format MM/DD/YYYY or MM-DD-YYYY DD/MM/YYYY or DD-MM-YYYY YYYY/MM/DD or YYYY-MM-DD MM-DD-YY or MM/DD/YY YYYY-MM-DD
        dates = re.findall(date_pattern, text)
        if dates:
            return dates[0]
        return None
    
    def process_post_likes(self, post):
        likes_element = post.find('div', class_=self.POST_LIKES_CLASS_ID, attrs={"aria-label": True})
        if likes_element:
            return self.extract_likes(likes_element.get("aria-label"))
        return None

    def extract_likes(self, aria_label):
        likes_pattern = re.compile(r"Like: (\d+) people")
        matches = likes_pattern.search(aria_label)
        if matches:
            number_of_likes = int(matches.group(1))
            return number_of_likes   
        return None