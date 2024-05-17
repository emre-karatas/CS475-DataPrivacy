from bs4 import BeautifulSoup
from Person import Person

def scrape_profile_page(file_path: str):
    username = None
    profile_picture_url = None
    name = None
    bio = None
    followers_count = -1
    following_count = -1

    # Scrape the profile page
    try:
        # Read the HTML code from the file
        with open(file_path, "r", encoding="utf-8") as file:
            html_code = file.read()

        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(html_code, "html.parser")

        # Find the <img> tag with "profile picture" in its alt attribute
        img_tag = soup.find('img', alt=lambda alt: alt and 'profile picture' in alt)

        # USERNAME
        # Extract the username
        username_element = soup.find('h2', class_='x1lliihq')

        # Extract the text of the h2 element
        username = username_element.text.strip()

        # BIO
        # Extract the bio
        bio_element = soup.find('h1', class_='_ap3a')

        # Extract the text of the h1 element
        bio = bio_element.text.strip()

        # NAME, FOLLOWERS AND FOLLOWING COUNT
        # Find the meta element with the specified property
        meta_element = soup.find('meta', property='og:description')

        # Extract the content attribute
        content = meta_element['content']

        # Extract follower count and following count
        # Split the text on commas
        parts = content.split(", ")

        for part in parts:
            # Remove extra spaces
            part = part.strip()
            
            # Check if part contains "Followers"
            if "Followers" in part:
                # Extract the number before "Followers"
                followers_count = int(part.split()[0].replace(",",""))  # Split on spaces and get the first element (number)
            
            # Check if part contains "Following"  
            if "Following" in part:
                # Extract the number before "Following"
                following_count = int(part.split()[0].replace(",",""))  # Split on spaces and get the first element (number)

            if "See" in part:
                # Extract the name
                name_part = part.split()[0]

                # Find the indices of "from" and "("
                from_index = part.find("from")
                open_parenthesis_index = part.find("(")

                # Extract the substring between "from" and "("
                name = part[from_index + len("from"):open_parenthesis_index].strip()

        # IMAGE
        # Extract the src attribute value
        if img_tag:
            src_value = img_tag['src']
            profile_picture_url = src_value.replace("&amp;", "&")
        else:
            print("No <img> tag with 'profile picture' in its alt attribute found.")
        
        return Person(name, username, profile_picture_url, bio, followers_count, following_count)
    except Exception as e:
        print(f"Error while scraping the profile page: {e}")
        return None
    
def scrapeFollowers(file_path):
    # Init an array of followers
    followers = []
    try:
        # Scrape the followers html page
        with open(file_path, "r", encoding="utf-8") as file:
                html_code = file.read()

        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(html_code, "html.parser")

        # Find the div element that contains the followers
        followers_section = soup.find('div', class_='_aano').find('div')

        # Find all div elements with the specified class
        div_elements = followers_section.find_all('div', class_='_aarf')

        # Extract info to build person
        for div in div_elements:
            username = div.a.get('href').split("/")[1]
            followers.append(username)

        return followers
    except Exception as e:
        print(f"Error scraping followers: {e}")
        return followers
    
def scrapeFollowings(file_path):
    # Init an array of followings
    followings = []
    try:
        # Scrape the followings html page
        with open(file_path, "r", encoding="utf-8") as file:
            html_code = file.read()
        
        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(html_code, "html.parser")

        # Find the div element that contains the followings
        followings_section = soup.find_all('div', class_='x1iyjqo2 x1pi30zi')

        for following in followings_section:
            # Extract the username
            username = following.a.get('href').split("/")[-1]
            followings.append(username)

        return followings
    except Exception as e:
        print(f"Error scraping followings: {e}")
        return followings