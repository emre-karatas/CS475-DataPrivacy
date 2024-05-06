from selenium import webdriver
from Person import Person
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https.instagram.com")
def scrapePerson(username):
    print(f"running for: {username}")
    # Navigate to Instagram profile
    profile_url = f"https://www.instagram.com/{username}/"
    driver.get(profile_url)

    username = None
    profile_picture_url = None
    name = None
    bio = None

    try:
        # Wait until the profile name element is visible
        username_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[contains(@class, \"x1lliihq\")]"))
        )

        # Extract profile information
        username = username_element.text
    except Exception as e:
        print(f"Error while getting name: {e}")

    try:
        # Wait until the profile name element is visible
        next_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, \"x1lliihq x1plvlek\")]"))
        )

        # Extract profile information
        name = next_element.text
    except Exception as e:
        print(f"Error while getting name: {e}")

    try:
        # Wait until the bio element is visible
        bio_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class, \"_ap3a\")]"))
        )

        # Extract bio text
        bio = bio_element.text
    except Exception as e:
        print(f"Error while getting bio: {e}")

    try:
        # Wait until the profile picture element is visible
        profile_picture_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//img[contains(@alt, \"Profil\")]"))
            #EC.visibility_of_element_located((By.XPATH, "//img[contains(@class, \"xpdipgo\")]"))
        )

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

    """ print(f"Username: {username}")
    print(f"Name: {name}")
    print(f"Profile Picture URL: {profile_picture_url}")
    print(f"Bio: {bio}") """

    return Person(name, username, profile_picture_url, bio)

listOfUsers = ["h.yarkinkurt", "_denizgokcen_", "burcukaplan__", "emre.karaatas", "esattokk", "saglamtugrull"]
profiles = []

for person in listOfUsers:
    profiles.append(scrapePerson(person))
    time.sleep(3)

for profile in profiles:
    print(profile)
# Close the WebDriver
driver.quit()