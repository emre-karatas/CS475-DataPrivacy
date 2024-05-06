import requests
import os

# Instagram API endpoint for user profile information
PROFILE_ENDPOINT = "https://graph.instagram.com/{user_id}?fields=id,username,name,profile_picture_url,biography&access_token={access_token}"

def get_profile_info(user_id, access_token):
    url = PROFILE_ENDPOINT.format(user_id=user_id, access_token=access_token)
    response = requests.get(url)
    
    if response.status_code == 200:
        print("SUCCESSSSSSSSSSSSSSSSSS")
        print(response)
        profile_data = response.json()
        return profile_data
    else:
        print("ERRORRRRRRRRRRRRRRRR:", response.status_code)
        print(response.reason)
        return None

def main():
    insta_access_token = os.getenv("INSTAGRAM_TOKEN")
    face_access_token = os.getenv("FACEBOOK_TOKEN")
    user_id = os.getenv("USER_ID")

    user_id = "7365627961712506241"
    
    profile_info = get_profile_info(user_id, insta_access_token)
    
    if profile_info:
        print("User Information:")
        print("Username:", profile_info['username'])
        print("Name:", profile_info.get('name'))
        """print("Profile Picture URL:", profile_info['profile_picture_url'])
        print("Bio:", profile_info['biography']) """
    else:
        print("Failed to retrieve profile information.")

if __name__ == "__main__":
    main()
