"""
-----------------------------------DEPRECATED------------------------------
Create a PostDatabase class responsible for managing the overall database of Facebook posts.
It will store information about each post, such as the number of likes and the date.
It stores a facebook post objects that contain their IDs, links, date, text & likes
It can use the CSVWriter class to store the data in CSV format.
-----------------------------------DEPRECATED------------------------------
"""
import psycopg2
import csv
import os
import logging
from scraping_engine.file_manager import FileManager
# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='app_db.log', filemode='w', format='%(levelname)s - %(message)s')

class PostDatabase:
    DB_DIR_NAME = "../output/csv_data"
    
    def __init__(self, csv_file) -> None:
        self.directory_name = self.DB_DIR_NAME
        self.file_manager = FileManager(self.directory_name)
        self.csv_file = self.file_manager.get_file_path(self.directory_name, csv_file)
        self.fields = ["ID", "Link", "Date", "Text", "Likes"]   
        self.existing_posts = set()
        self.existing_ids = set()
        self.read_csv = None
        self.cached_max_id = None
    
    def create_csv(self):
        if not self.file_manager.file_exists(self.csv_file):
            self.file_manager.create_directory()
            try:
                with open(self.csv_file, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=self.fields)
                    writer.writeheader()
                logging.info("Created a new CSV file for the database.")
                self.cached_max_id = 0
            except Exception as e:
                logging.error(f"Error creating CSV file: {e}")
                return False
        return True

    def load_existing_posts(self):
        try:
            # Load existing posts into memory for quick lookup
            with open(self.csv_file, mode='r') as file:
                self.open_csv = csv.DictReader(file)
                
                for row in self.open_csv:
                    self.existing_posts.add(row["Link"])
                    self.existing_ids.add(row["ID"])
                    
        except Exception as e:
            logging.error(f"Error loading existing posts: {e}")

    def post_exists(self, post):
        # Check if a post with the given ID exists in memory (quick lookup)
        return post.link in self.existing_posts
    
    def get_next_available_id(self):
        try:
            if self.cached_max_id and self.cached_max_id >= 0:
                self.cached_max_id += 1   
                return self.cached_max_id
            
            if not self.open_csv:
                with open(self.csv_file, mode='r') as file:
                    self.open_csv = csv.DictReader(file)
                    self.existing_ids = set(int(row["ID"]) for row in self.open_csv)
                    
            # Find the next available ID by incrementing from 1
            next_id = 1
            while next_id in self.existing_ids:
                next_id += 1
                
            self.cached_max_id = next_id
            return self.cached_max_id
            
        except Exception as e:
            logging.error(f"Error getting next available ID: {e}")
            return None
        
    def decrease_cached_available_id(self):
        self.cached_max_id -= 1
        
    def add_post(self, post):
        try:
            with open(self.csv_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fields)
                writer.writerow({
                    "ID": post.id,
                    "Link": post.link,
                    "Date": post.date,
                    "Text": post.text,
                    "Likes": post.likes
                })
            self.existing_posts.add(post.link)
            logging.info(f"Added post with ID {post.id} to the database.")
        except Exception as e:
            logging.error(f"Error adding post to the database: {e}")
