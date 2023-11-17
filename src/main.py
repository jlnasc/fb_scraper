#TODO :  fix folder issues
from scraping_engine.scraper import Scraper
from scraping_engine.post_exporter import TextFileExporter, InfoFileExporter
from db_repository.fb_post_repository import DatabaseRepository
from db_utilities.db_manager import DatabaseManager
from db_service.db_service import DatabaseService
import progressbar
import os

#  Constants
FB_DATA_SOURCE = os.path.join(os.path.dirname(__file__), '..', 'data', '2_11.html')        

def export_facebook_post(post):
    """
    Export a Facebook post into a text file (content of the post & its info).

    Args:
        post (FacebookPost): The FacebookPost object to export.

    Returns:
        str: The file path of the exported file.
    """
    exporter_classes = [TextFileExporter(post), InfoFileExporter(post)]

    for exporter in exporter_classes:
        exporter.set_directory_name()
        exporter.create_directory()
        exporter.set_file_name()
        exporter.write_file()
        

def main():
    print("Facebook Post Scraper")
    
    db_manager = DatabaseManager(host="localhost", dbname="jl", user="jl", password="1234")
    db_repository = DatabaseRepository(db_manager)
    db_service = DatabaseService(db_repository)
    
    db_manager.configure_connection_pool()
    db_service.create_table()
    
    scraper = Scraper(FB_DATA_SOURCE)
    scraper.load_html_source()
    all_posts = scraper.get_facebook_posts()
    
    bar = progressbar.ProgressBar(max_value=len(all_posts), redirect_stdout=True)
    post_count = 0

    for post in all_posts:

        fb_post_filtered = scraper.scrape_facebook_post(post)
        
        post_count += 1
        bar.update(post_count)
        
        if not fb_post_filtered.is_valid():
            continue
        
        fb_post_id = db_service.add_post(fb_post_filtered)

        if fb_post_id:
            fb_post_filtered.insert_id(fb_post_id)
            export_facebook_post(fb_post_filtered)
                
if __name__ == "__main__":
    main()