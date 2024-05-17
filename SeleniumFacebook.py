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


def scrapePersonFromFacebook(baseUser, driver):
    # Navigate to Facebook profile
    profile_url = f"https://www.facebook.com/{baseUser}"
    driver.get(profile_url)

    username = baseUser
    profile_picture_url = None
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
    try:
        # Wait until the profile picture element is visible
        profile_picture_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Profile picture actions"]'))
        )

        # Find the image tag within the SVG element
        image_element = profile_picture_element.find_element(By.TAG_NAME, "image")

        # Extract the value of the xlink:href attribute
        profile_picture_url = image_element.get_attribute("xlink:href")
    except Exception as e:
        print(f"Error while getting profile picture: {e}")

    """ # FOLLOWERS AND FOLLOWING COUNT
    try:
        # Find the element containing the friend count
        friend_count_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf')]"))
        )

        # Extract the text content of the element
        friend_count_text = friend_count_element.text

        # Split the text to extract the numerical value of the friend count
        # friend_count = friend_count_text.split()[0]

        # print("Friend count:", friend_count)
    except Exception as e:
        print(f"Error while getting friend count: {e}")
    """
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

        """ # Extract the list of friends
        following_elements = following_field.find_element(By.CLASS_NAME, "x78zum5.x1q0g3np.x1a02dak.x1qughib")
        
        following_table = following_elements.find_elements(By.TAG_NAME, "div")

        following_temp = []
        for element in following_table:
            # Wait for the <a> element to be clickable
            link_element = WebDriverWait(element, 10).until(
                EC.element_to_be_clickable((By.TAG_NAME, "a"))
            )
            link = link_element.get_attribute("href")
            print("link= ", link)
            following_username = link.split('/')[1]
            following_temp.append(following_username)

        following = following_temp
        print(following) """

    except Exception as e:
        print(f"Error while getting followers: {e}")
    
    return Person(name, username, profile_picture_url, bio, followers_count, following_count)