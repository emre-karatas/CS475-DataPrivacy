from SeleniumInstagram import login, scrapePerson
from selenium import webdriver
from config import Config
from selenium.webdriver.chrome.options import Options
from BeautifulSoupScraper import scrape_profile_page, scrapeFollowers
import time

config = Config()
baseUser = config.get_insta_username()

# Initialize WebDriver
options = Options()
options.add_argument("--lang=en")
driver = webdriver.Chrome(options=options)

# Perform login
driver.get("https://www.instagram.com/accounts/login/")
login(driver, baseUser, config.get_insta_password())

# Scrape the person
person = scrapePerson(baseUser, driver)
time.sleep(2)

# Get the followers
person = scrape_profile_page(f"pages/{person.username}.html")
follower_list = scrapeFollowers(f"pages/{person.username}_followers.html")
following_list = scrapeFollowers(f"pages/{person.username}_following.html")
person.add_followers_list(follower_list)
person.add_following_list(following_list)

# Init a list of followings
following_people_list = []

# Get the followers and following of the followings
for pers in following_list:
    temp_person = scrapePerson(pers, driver)
    time.sleep(2)
    temp_person = scrape_profile_page(f"pages/{pers}.html")
    follower_list_temp = scrapeFollowers(f"pages/{pers}_followers.html")
    following_list_temp = scrapeFollowers(f"pages/{pers}_following.html")
    temp_person.add_followers_list(follower_list_temp)
    temp_person.add_following_list(following_list_temp)
    following_people_list.append(temp_person)

# Close the WebDriver
driver.quit()

print("Followings: ")
for p in following_people_list:
    print(p)

# Write the followings to a text file
with open("followings.txt", "w") as file:
    file.write("Followings:\n")
    for p in following_people_list:
        file.write(str(p) + "\n")