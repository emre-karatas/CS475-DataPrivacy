import os
from dotenv import load_dotenv

# os.environ.clear()
load_dotenv()

class Config:
    def get_insta_username(self):
        return os.getenv("INSTAGRAM_USERNAME")

    def get_insta_password(self):
        return os.getenv("INSTAGRAM_PASSWORD")
    
    def get_fb_username(self):
        return os.getenv("FACEBOOK_USERNAME")
    
    def get_fb_password(self):
        return os.getenv("FACEBOOK_PASSWORD")
