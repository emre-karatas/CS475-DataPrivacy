from SeleniumInstagram import login, scrapePerson
from selenium import webdriver
from config import Config
from selenium.webdriver.chrome.options import Options
import time

listOfUsers = ["esattokk", "burcukaplan__"]
profiles = []

config = Config()
username_login = config.get_insta_username()
password_login = config.get_insta_password()

# Initialize WebDriver
options = Options()
options.add_argument("--lang=en")
driver = webdriver.Chrome(options=options)

# Perform login
driver.get("https://www.instagram.com/accounts/login/")

login(driver, username_login, password_login)

for person in listOfUsers:
    profiles.append(scrapePerson(person, driver))
    time.sleep(3)

for profile in profiles:
    print(profile)
# Close the WebDriver
driver.quit()