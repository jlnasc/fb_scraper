from abc import ABC, abstractmethod

import psycopg2

class BaseRepository(ABC):
    
    # Create
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def insert(self, entity):
        pass
    
    # Read
    @abstractmethod
    def read(self, id):
        pass
    
    @abstractmethod
    def read_all(self):
        pass
    
    # Update
    @abstractmethod
    def update(self, entity):
        pass

    # Delete
    @abstractmethod
    def delete(self, entity):
        pass
    



