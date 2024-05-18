from typing import List
from PIL import Image
from io import BytesIO
import requests
import os

def download_image(url, save_path, file_name):
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

download_image("https://scontent.fasr2-1.fna.fbcdn.net/v/t39.30808-1/239363438_10161278832391754_3124586202588104528_n.jpg?stp=cp0_dst-jpg_p80x80&_nc_cat=1&ccb=1-7&_nc_sid=5f2048&_nc_ohc=okFNeFZo0hMQ7kNvgF8VwBH&_nc_oc=AdgrTiCGI5DYGvlYATRVOT7oFPCL6hQ0Lpd7n8I4KaQ9sMQfhZopeq9g4TBmBg9eI08&_nc_ht=scontent.fasr2-1.fna&oh=00_AYAvrlBgc1xp_tGbpy038qOf8AT2vAD4DEr8zPXaJAbTpA&oe=664ED24D", "images/facebook/", "DonaldTrump.jpg")