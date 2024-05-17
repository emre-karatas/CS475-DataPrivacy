from Person import Person
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_instagram(driver, username, password):
    try:
        # Wait for the login form elements to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )

        username_field.send_keys(username)
        password_field.send_keys(password)

        # Locate and click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        time.sleep(4)
    except Exception as e:
        print(f"Error trying to login to Instagram: {e}")


def scrapePersonFromInstagram(username, driver):
    print(f"running for: {username}")
    # Navigate to Instagram profile
    profile_url = f"https://www.instagram.com/{username}"
    driver.get(profile_url)

    username = None
    profile_picture_url = None
    name = None
    bio = None
    followers_count = -1
    following_count = -1

    # USERNAME
    try:
        # PROFILE PAGE
        # Wait until the username element is visible
        username_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[contains(@class, \"x1lliihq\")]"))
        )
        # Get the entire HTML source code of the page
        html_code = driver.page_source

        # Extract profile information
        username = username_element.text

        # Write the HTML code to a file
        file_path = f"pages/{username}.html"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_code)

        # FOLLOWERS PAGE
        # Get the entire HTML source code of the followers page
        driver.get(f"{profile_url}/followers")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@role, 'dialog')]"))
        )
        time.sleep(3)
        followers_html_code = driver.page_source

        # Write the HTML code to a file
        followers_file_path = f"pages/{username}_followers.html"
        with open(followers_file_path, "w", encoding="utf-8") as file:
            file.write(followers_html_code)

        # FOLLOWING PAGE
        # Get the entire HTML source code of the following page
        driver.get(f"{profile_url}/following")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@role, 'dialog')]"))
        )
        time.sleep(3)
        following_html_code = driver.page_source

        # Write the HTML code to a file
        following_file_path = f"pages/{username}_following.html"
        with open(following_file_path, "w", encoding="utf-8") as file:
            file.write(following_html_code)

    except Exception as e:
        print(f"Error while scraping '{username}' : {e}")

    """
    # NAME
    try:
        # Wait until the name element is visible
        name_element = WebDriverWait(driver, 10).until(
            #EC.visibility_of_element_located((By.XPATH, '//*[@id="mount_0_0_HP"]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/div[1]/div[1]/span'))
            EC.visibility_of_element_located((By.XPATH, '//div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/div[1]/div[1]/span'))
        )

        # Extract the name text
        name = name_element.text
        print(name)
    except Exception as e:
        print(f"Error while getting name: {e}")

    # BIO
    try:
        # Wait until the bio element is visible
        bio_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class, \"_ap3a\")]"))
        )

        # Extract bio text
        bio = bio_element.text
    except Exception as e:
        print(f"Error while getting bio: {e}")

    # PROFILE PICTURE
    try:
        # Wait until the profile picture element is visible
        profile_picture_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/header/div/div/a/img"))
            #EC.visibility_of_element_located((By.XPATH, "//img[contains(@class, \"xpdipgo\")]"))
            #EC.visibility_of_element_located((By.CSS_SELECTOR, "img[class*='xpdipgo']"))
        )
        print("NAME: ", str(profile_picture_element))

        # Extract profile picture URL
        profile_picture_url = profile_picture_element.get_attribute("src")
    except Exception as e:
        print(f"Error while getting profile picture: {e}")

    try:
        if profile_picture_url == None:
                profile_picture_element = WebDriverWait(driver, 10).until(
                #EC.visibility_of_element_located((By.XPATH, "//img[contains(@alt, \"Profil\")]"))
                EC.visibility_of_element_located((By.XPATH, "//img[contains(@class, \"xpdipgo\")]"))
            )
            
        # Extract profile picture URL
        profile_picture_url = profile_picture_element.get_attribute("src")
    except Exception as e:
        print(f"Error while getting profile picture for non profile picture: {e}")

    # FOLLOWER COUNT
    try:
        # Wait until the follower count is visible
        followers_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/ul/li[2]/a/span"))
        )

        print(followers_button.text)
        followers_count = int(followers_button.text.split(" ")[0])
    except Exception as e:
        print(f"Error while getting followers count: {e}")

    # FOLLOWING COUNT
    try:
        # Wait until the following count is visible
        following_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[2]/section/main/div/ul/li[3]/a/span"))
        )

        print(following_button.text)
        following_count = int(following_button.text.split(" ")[0])
    except Exception as e:
        print(f"Error while getting following count: {e}")

    # FOLLOWERS
    try:
        driver.get(f"{profile_url}/followers")
        time.sleep(3)
        followers = []
        # Wait until the followers list is visible
        parent_element = driver.find (By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div")

    except Exception as e:
        print(f"Error while getting followers: {e}") """
    return Person(name, username, profile_picture_url, bio, followers_count, following_count)