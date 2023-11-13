
class DatabaseService:
    def __init__(self, post_repository):
        self.post_repository = post_repository

    def create_table(self):
        return self.post_repository.create()
    
    def add_post(self, post):
        return self.post_repository.insert(post)

    def read_post(self, post):
        return self.post_repository.read(post)    

    def read_all(self):
        return self.post_repository.read_all()    
    
    def delete_post(self, post):
        return self.post_repository.delete(post)