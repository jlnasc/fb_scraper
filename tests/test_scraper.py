import pytest
from bs4 import BeautifulSoup
from src.scraping_engine.scraper import Scraper
import os


class TestsLinkExtraction:

    @pytest.mark.parametrize("link,expected_link", [
    ("https://www.facebook.com/photo/?fbid=123456789&set=a.12345678&__cft__[0]=12345678-12345678-12345678&__tn__=EH-R", "https://www.facebook.com/photo/?fbid=123456789"), 
    ("https://www.facebook.com/photo/?fbid=Avsad123", "https://www.facebook.com/photo/?fbid=Avsad123")
    ])
    def test_extract_link(self, link, expected_link):
        # Create a mock post element with the specified link
        post_html = f'<div class="post"><a href="{link}" class="post-link"></a></div>'
        
        mock_post = BeautifulSoup(post_html, 'lxml')
        mock_link_element = mock_post.find('a', class_='post-link')

        scraper = Scraper(None)
        extracted_link = scraper.extract_link_from_element(mock_link_element['href'])

        assert extracted_link == expected_link

class TestDateExtraction:
    
    scraper = Scraper(None)

    valid_date_texts = [
            ("The date is 10/04/2023", "10/04/2023"),
            ("The date is 10-04-2023", "10-04-2023"),
            ("The date is 04/10/2023", "04/10/2023"),
            ("The date is 04-10-2023", "04-10-2023"),
            ("The date is 2023/10/04", "2023/10/04"),
            ("The date is 2023-10-04", "2023-10-04"),
            ("The date is 10-04-23", "10-04-23"),
            ("The date is 10/04/23", "10/04/23"),
        ]
    
    invalid_date_texts = [ 
                ("Invalid date", None),
                ("1/04/a22", None),
                ("100-100-2023", None),
                ("10-0X-2023", None)
                ]
    
    @pytest.mark.parametrize("date_text,expected_date", valid_date_texts)
    def test_extract_date_valid_input(self, date_text, expected_date):
        extracted_date = self.scraper.extract_date_from_text(date_text)

        assert extracted_date == expected_date

    @pytest.mark.parametrize("date_text,expected_date", invalid_date_texts)
    def test_extract_date_invalid_input(self, date_text, expected_date):
        extracted_date = self.scraper.extract_date_from_text(date_text)

        assert extracted_date == expected_date

    
class TestLikeExtraction:
    
    scraper = Scraper(None)

    valid_aria_labels = [
            ("Like: 1 people", 1),
            ("Like: 20 people", 20),
            ("Like: 300 people", 300),
            ("Like: 4000 people", 4000),
            ("Like: 50000 people", 50000)
            ]
    
    invalid_aria_labels = [
            ("Like:", None),
            ("Likes:", None),
            ("Like: people", None),
            ("Likes: 123 people", None),
            ("Like: 123,456 people", None)
            ]
    
    @pytest.mark.parametrize("mock_aria_label,expected_likes", valid_aria_labels)
    def test_extract_likes_valid_input(self, mock_aria_label, expected_likes):
        extracted_likes = self.scraper.extract_likes(mock_aria_label)
        
        assert extracted_likes == expected_likes

    @pytest.mark.parametrize("mock_aria_label,expected_likes", invalid_aria_labels)
    def test_extract_likes_invalid_input(self, mock_aria_label, expected_likes):
        extracted_likes = self.scraper.extract_likes(mock_aria_label)
        
        assert extracted_likes == expected_likes