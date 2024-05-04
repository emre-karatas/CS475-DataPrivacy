import requests
import os

insta_access_token = os.getenv("INSTAGRAM_TOKEN")
face_access_token = os.getenv("FACEBOOK_TOKEN")

# Instagram API endpoint for user profile information
PROFILE_ENDPOINT = "https://graph.instagram.com/{user_id}?fields=id,username,media_count&access_token={access_token}"

def get_profile_info(user_id, access_token):
    url = PROFILE_ENDPOINT.format(user_id=user_id, access_token=access_token)
    response = requests.get(url)
    
    if response.status_code == 200:
        profile_data = response.json()
        return profile_data
    else:
        print("Error:", response.status_code)
        return None

def main():
    # Replace 'USER_ID' and 'ACCESS_TOKEN' with your actual user ID and access token
    user_id = 'USER_ID'
    access_token = 'ACCESS_TOKEN'
    
    profile_info = get_profile_info(user_id, access_token)
    
    if profile_info:
        print("Profile Information:")
        print("Username:", profile_info['username'])
        print("Media Count:", profile_info['media_count'])
    else:
        print("Failed to retrieve profile information.")

if __name__ == "__main__":
    main()
