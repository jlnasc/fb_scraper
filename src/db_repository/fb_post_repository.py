import psycopg2
import logging
from ._base import BaseRepository
from scraping_engine.facebook_post import FacebookPost


logging.basicConfig(level=logging.DEBUG, filename='app_db.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')


class DatabaseRepository(BaseRepository):
    """
    DatabaseRepository class for interacting with the database.
    """

    def __init__(self, db_manager):
        """
        Constructs a new DatabaseRepository object.

        Args:
            db_manager: The database manager to use for database operations.
        """
        self.db_manager = db_manager

    def create(self):
        """
        Creates the `facebook_posts` table if it doesn't exist.

        Returns:
            True if the table was created successfully, False otherwise.
        """

        try:
            connection = self.db_manager.get_connection()
            cursor = connection.cursor()

            # Define the table schema
            query = """CREATE TABLE IF NOT EXISTS facebook_posts (
                    id SERIAL PRIMARY KEY,
                    account VARCHAR(255),
                    dt VARCHAR(30),
                    likes INT,
                    link VARCHAR(255) UNIQUE,
                    content TEXT
                );
            """

            logging.debug("Executing query: {}".format(query))
            cursor.execute(query)

            connection.commit()
            cursor.close()
            logging.info("Table 'facebook_posts' created successfully.")

            return True

        except Exception as e:
            logging.error("Error creating the table: {}".format(e))
            return False

        finally:
            self.db_manager.return_connection(connection)

    def insert(self, post: FacebookPost) -> int:
            """
            Inserts a new post into the database.

            Args:
                post: The FacebookPost object to insert.

            Returns:
                The ID of the inserted post, or None if there is an error.
            """

            logging.info("Inserting post: {}".format(post.link))

            try:
                connection = self.db_manager.get_connection()
                cursor = connection.cursor()

                # Create a prepared statement to prevent SQL injection
                query = """INSERT INTO facebook_posts (account, dt, likes, link, content)
                           VALUES (%s, %s, %s, %s, %s) RETURNING id;"""

                logging.debug("Executing prepared statement: {}".format(query))
                cursor.execute(query, (post.account, post.date, post.likes, post.link, post.text))

                # Fetch the ID of the inserted post
                inserted_id = cursor.fetchone()[0]
                logging.info("Post inserted successfully with ID: {}".format(inserted_id))

                connection.commit()
                cursor.close()

                return inserted_id

            except psycopg2.IntegrityError as e:
                logging.error(f"Integrity Error inserting post {post.link}: {e}")
                return None

            except Exception as e:
                logging.error(f"Error in insert: {e}")
                return None

            finally:
                self.db_manager.return_connection(connection)            

    def read(self, post_id: int) -> FacebookPost:
        """
        Reads a post from the database by ID.

        Args:
            post_id: The ID of the post to read.

        Returns:
            The FacebookPost object, or None if the post does not exist.
        """

        try:
            connection = self.db_manager.get_connection()
            cursor = connection.cursor()

            query = """SELECT * from facebook_posts WHERE id = %s;"""
            parameters = (post_id,)
            
            logging.debug("Executing query: {}".format(query))
            cursor.execute(query, parameters)

            read_val = cursor.fetchone()[0]

            if not read_val:
                logging.error(f"Post {post_id} not found")
                return None

            connection.commit()
            cursor.close()

            return FacebookPost(**read_val)

        except Exception as e:
            logging.error(f"Error reading post {post_id}: {e}")
            return None
        
    def read_all(self):
        """
        Reads all the posts

        Returns:
            The posts, or None if the posts don't exist.
        """
        
        try:
            connection = self.db_manager.get_connection()
            cursor = connection.cursor()
            
            query = """SELECT * from facebook_posts;"""
            cursor.execute(query)
            
            entire_table = cursor.fetchall()
            
            connection.commit()
            cursor.close()
            
            return entire_table
         
        except Exception as e:
            logging.error(f"Error reading table: {e}")    
            return None
        
        finally:
            self.db_manager.return_connection(connection)
        
    def update(self, entity):
        pass

    def delete(self, post):
        """
        Deletes a post from the database by ID.

        Args:
            post_id: The ID of the post to read.

        Returns:
            True, or False if the post does not exist.
        """
        try:
            connection = self.db_manager.get_connection()
            cursor = connection.cursor()
            
            query = """DELETE FROM facebook_posts WHERE id = %s;"""
            parameters = (post.id, )
            cursor.execute(query, parameters)
            
            connection.commit()
            cursor.close()   
            
            return True
        
        except Exception as e:
            logging.error(f"Error deleting post.id - {post.id}: {e}")    
            return False
        
        finally:
            self.db_manager.return_connection(connection)
