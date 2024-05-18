from typing import List
from PIL import Image
from io import BytesIO
import requests
import os

class Person:
    def __init__(self, name, username, profile_picture_url: str, bio, followers_count, following_count, user_type):
        self.name = name
        self.username = username
        self.user_type = user_type
        self.profile_picture_url = self.url_converter(profile_picture_url)
        self.bio = bio
        self.followers: List[Person] = []
        self.following: List[Person] = []
        self.followers_count = followers_count
        self.following_count = following_count
        self.profile_picture_path = f"images/{self.user_type}/{self.username}.jpg"

    def __str__(self):
        return f"""Name: {self.name}
User type: {self.user_type}
Username: {self.username}
Profile Picture URL: {self.profile_picture_url}
Bio: {self.bio}
Followers Count: {self.followers_count}
    Followers: {', '.join([follower.username for follower in self.followers])}
Following Count: {self.following_count}
    Following: {', '.join([following.username for following in self.following])}
"""

    def add_follower(self, follower: 'Person'):
        if isinstance(follower, Person):
            self.followers.append(follower)
        else:
            raise ValueError("Follower must be an instance of Person")

    def add_followers_list(self, followers_list: List['Person']):
        if all(isinstance(follower, Person) for follower in followers_list):
            self.followers = followers_list
        else:
            raise ValueError("All followers must be instances of Person")

    def add_following(self, following: 'Person'):
        if isinstance(following, Person):
            self.following.append(following)
        else:
            raise ValueError("Following must be an instance of Person")

    def add_following_list(self, following_list: List['Person']):
        if all(isinstance(following, Person) for following in following_list):
            self.following = following_list
        else:
            raise ValueError("All following must be instances of Person")

    # Convert the URL by removing &amp; and replacing with &
    def url_converter(self, url: str) -> str:
        converted_url = url.replace("&amp;", "&")
        self.download_image(converted_url, f"images/{self.user_type}/" , f"{self.username}.jpg")
        return converted_url

    def set_url(self, url: str):
        self.profile_picture_url = self.url_converter(url)

    def download_image(self, url, save_path, file_name):
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Send a GET request to the URL
            response = requests.get(url)

            # Check if the request was successful
            response.raise_for_status()

            # Open the image using PIL
            img = Image.open(BytesIO(response.content))

            # Save the image to the specified path
            img.save(f"{save_path}/{file_name}")
            print(f"Image successfully downloaded and saved to {save_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
        except IOError as e:
            print(f"Error saving image: {e}")