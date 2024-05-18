from Person import Person
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login_facebook(driver, username, password):
    try:
        # Wait for the login form elements to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "pass"))
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
        print(f"Error trying to login to Facebook: {e}")


def scrapePersonFromFacebook(baseUser, driver, base):
    # Navigate to Facebook profile
    profile_url = f"https://www.facebook.com/{baseUser}"
    driver.get(profile_url)

    username = baseUser
    profile_picture_url = ""
    name = None
    bio = None
    followers_count = -1
    following_count = -1
    following = []

    # Extract profile information

    # NAME
    try:
        # Wait until the name element is visible
        name_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1"))
        )

        name = name_element.text
    except Exception as e:
        print(f"Error while getting name: {e}")
    
    # PROFILE PICTURE
    if base == True:
        try:
            # Wait until the profile picture element is visible
            profile_picture_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Profile picture actions"]'))
            )

            # Find the image tag within the SVG element
            image_element = profile_picture_element.find_element(By.TAG_NAME, "image")

            # Extract the value of the xlink:href attribute
            profile_picture_url = image_element.get_attribute("xlink:href")
        except Exception as e:
            print(f"Error while getting profile picture: {e}")

    # BIO
    try:
        # Wait until the bio element is visible
        bio_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@data-pagelet="ProfileTilesFeed_0"]'))
        )

        bio_element = bio_field.find_element(By.CLASS_NAME, "xieb3on").find_element(By.TAG_NAME, "span")

        bio = bio_element.text  # Extract bio text
    except Exception as e:
        print(f"Error while getting bio: {e}")

    # FOLLOWERS
    try:
        driver.get(f"https://www.facebook.com/{baseUser}/following")
        time.sleep(2)

        # Wait until the friend list is visible
        following_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@data-pagelet="ProfileAppSection_0"]'))
        )

        # Get the entire HTML source code of the page
        html_code = driver.page_source

        # Write the HTML code to a file
        following_file_path = f"pages/fb_{username}_following.html"

        with open(following_file_path, "w", encoding="utf-8") as file:
            file.write(html_code)

    except Exception as e:
        print(f"Error while getting followers: {e}")
    
    return Person(name, username, profile_picture_url, bio, followers_count, following_count, "facebook")