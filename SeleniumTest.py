from SeleniumInstagram import login, scrapePerson
from selenium import webdriver
from config import Config
import time

listOfUsers = ["h.yarkinkurt", "_denizgokcen_"]
profiles = []

config = Config()
username_login = config.get_insta_username()
password_login = config.get_insta_password()
print(username_login)

# Initialize WebDriver
driver = webdriver.Chrome()

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