from db_repository.fb_post_repository import DatabaseRepository
from db_utilities.db_manager import DatabaseManager
from db_service.db_service import DatabaseService

class DatabaseFactory:
    @staticmethod
    def get_db_objects():
        db_manager = DatabaseManager(host="localhost", dbname="jl", user="jl", password="1234")
        db_manager.configure_connection_pool()

        db_repository = DatabaseRepository(db_manager)

        db_service = DatabaseService(db_repository)