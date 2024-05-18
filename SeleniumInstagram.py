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

    profile_picture_url = ""
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

        # Write the HTML code to a file
        file_path = f"pages/{username}.html"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_code)

        """ # FOLLOWERS PAGE
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
            file.write(followers_html_code) """

        # FOLLOWING PAGE
        # Get the entire HTML source code of the following page
        try:
            time.sleep(3)
            driver.get(f"{profile_url}/following")
            href_following = f'/{username}/following/'
            print(href_following)
            following_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//a[@href='{href_following}']"))
            )
            
            print("button: ", following_button.text)

            following_button.click()

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
            print(f"Error while getting following page: {e}")

    except Exception as e:
        print(f"Error while scraping '{username}' : {e}")

    finally:
        return Person(name, username, profile_picture_url, bio, followers_count, following_count, "instagram")