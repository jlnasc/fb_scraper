import os
import logging
from abc import ABC, abstractmethod
from scraping_engine.file_manager import FileManager

"""
Create a PostExporter class responsible for writing the post text to text files.
It will take a FacebookPost object as input and write its text to a text file within the corresponding post folder.
"""

# Configure logging
log_dir = '../logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app_exporter.log')
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w', format='%(levelname)s - %(message)s')

class FacebookPostExporter(ABC):
    """
    Base class for exporting Facebook post content to files.
    """
    BASE_POEMS_DIR = '../output/poems'
     
    def __init__(self, fb_post) -> None:
        """
        Initialize the exporter with a FacebookPost object.
        """
        
        self.fb_post = fb_post
        self.directory_name = None
        self.file_name = None
        self.file_manager = None
    
    def set_directory_name(self):
        """
        Set the directory name based on the FacebookPost ID
        """
        individual_directory_name = str(self.fb_post.id)
        self.directory_name = os.path.join(self.BASE_POEMS_DIR, individual_directory_name)
        
    def create_directory(self):
        """
        Create the desired directory
        """
        self.file_manager = FileManager(self.directory_name)
        self.file_manager.create_directory()
        
    @abstractmethod
    def set_file_name(self):
        """
        Set the info/text file name.
        """
        
        pass
    
    @abstractmethod
    def write_file(self):
        """
        Export the info/text into the txt file.
        """
        
        pass
    
    @property
    def file_path(self) -> str:
        """
        Get the info/text file path
        """
        current_directory = os.getcwd()
        return self.file_manager.get_file_path_relative(current_directory, self.directory_name, self.file_name)

    def handle_file_write_error(self, error):
        """
        Handle writing errors.
        """
        logging.error(f"An error occurred while writing the file: {error}", exc_info=True)
        
   
            
class TextFileExporter(FacebookPostExporter):
    """
    Exporter class for writing Facebook post's text into text files.
    """
    MAX_TITLE_LENGTH = 50
    
    def set_file_name(self):
        """
        Set the file name based on the first line of the post's text.
        """
        try:
            clean_poem_name = ''.join(letter for letter in self.fb_post.text.split('\n', 1)[0] if letter.isalnum())[:self.MAX_TITLE_LENGTH]
        except Exception:
            clean_poem_name = self.fb_post.id
        self.file_name = f"{clean_poem_name}.txt"
        # print(f"File Name: {self.file_name}")
        
    def write_file(self):
        """
        Export the post's text into the txt file.
        """
        try:
            print(self.file_path)
            if not self.file_manager.file_exists(self.file_path):
                with open(self.file_path, "w") as file:
                    file.write(self.fb_post.text)
        except Exception as e:
            self.handle_file_write_error(e)
            

class InfoFileExporter(FacebookPostExporter):
    
    def set_file_name(self):
        """
        Set the file name based on the post's id.
        """
        
        self.file_name = "{}_info.txt".format(self.fb_post.id)
        # print(f"REAL_ID: {self.fb_post.id}")
    def write_file(self):
        """
        Export the post's info into the txt file.
        """
        
        try:
            with open(self.file_path, "w") as file:
                file.write("###############################################\n")
                file.write(f"ID: {self.fb_post.id}\n")
                file.write(f"Account: {self.fb_post.account}\n")
                file.write(f"Date: {self.fb_post.date}\n")
                file.write(f"Likes: {self.fb_post.likes}\n")
                file.write(f"Link: {self.fb_post.link}\n")
                #file.write(f"Text:\n{self.fb_post.text}\n")
                file.write("###############################################\n")
        except Exception as e:
            self.handle_file_write_error(e)
    