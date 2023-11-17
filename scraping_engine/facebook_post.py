"""
Create a FacebookPost class representing a single Facebook post and its related information. 
The class should have attributes like post_text, picture_link, likes, date, etc.
"""

class FacebookPost:
    FB_ACCOUNT_NAME = 'Poemas de Anabela Bernardes: "Os meus silêncios"'

    def __init__(self, link, account, text, date, likes):
        self.id = None
        self.link = link
        self.account = account
        self.text = text
        self.date = date
        self.likes = likes
    
    def insert_id(self, id):
        self.id = id
        
    def is_valid(self):
        """
        A post is valid if its text contains more than 1 line, and
        The fb account linked to it is the desired one.
        
        Args:
            post (FacebookPost): The FacebookPost object to export.

        Returns:
            bool: Post is valid
        """
        return self.text and self.link and '\n' in self.text and self.account == self.FB_ACCOUNT_NAME

    def __str__(self):
        return f"ID: {self.id}\n" \
               f"Account: {self.account}\n" \
               f"Link: {self.link}\n" \
               f"Text:\n{self.text}\n" \
               f"Date: {self.date}\n" \
               f"Likes: {self.likes}\n" \
               f"###############################################"