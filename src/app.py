from flask import Flask, jsonify, g
from db_factory.db_factory import DatabaseFactory
from scraping_engine.scraper import Scraper
from scraping_engine.post_exporter import TextFileExporter, InfoFileExporter
import os

app = Flask(__name__)

FB_DATA_SOURCE = os.path.join(os.path.dirname(__file__), '..', 'data', '2_11.html')        

@app.before_request
def before_request():
    db_manager, db_repository, db_service = DatabaseFactory.get_db_objects()
    g.db_manager = db_manager
    g.db_repository = db_repository
    g.db_service = db_service
    
@app.get("/")
def home():
    return "Facebook Post Scraper"

@app.route("/api/config", methods=['POST'])
def config_system():
    try:
        g.db_service.create_table()
        
        return jsonify({"message": "System successfully configured"}), 200
    
    except Exception as e:
        return jsonify({"message": f"An error ocurred while attemping to configure the system: {e}"}), 500
    
@app.route("/api/start_data_ingestion", methods=['POST'])
def data_ingestion():
    try:
        # Enqueue the data ingestion task into the background task queue
        data_ingestion_task.delay()
        
        return jsonify({"message": "Data ingestion successfully started "}), 200
    
    except Exception as e:
        return jsonify({"message": f"An error ocurred while attemping to start the analysis: {e}"}), 500
    
@app.route("/api/check_data_ingestion_status", methods=['GET'])
def data_ingestion_status():
    pass
            
def export_facebook_post(post):
  exporter_classes = [TextFileExporter(post), InfoFileExporter(post)]

  for exporter in exporter_classes:
    exporter.set_directory_name()
    exporter.create_directory()
    exporter.set_file_name()
    exporter.write_file()

@app.task
def data_ingestion_task():
    scraper = Scraper(FB_DATA_SOURCE)
    scraper.load_html_source()
    all_posts = scraper.get_facebook_posts()

    for post in all_posts:
        fb_post_filtered = scraper.scrape_facebook_post(post)

        if not fb_post_filtered.is_valid():
            continue

        fb_post_id = g.db_service.add_post(fb_post_filtered)

        if fb_post_id:
            fb_post_filtered.insert_id(fb_post_id)
            export_facebook_post(fb_post_filtered)
            


if __name__ == "__main__":
  app.run(debug=True)