from SeleniumInstagram import login_instagram, scrapePersonFromInstagram
from SeleniumFacebook import login_facebook, scrapePersonFromFacebook
from selenium import webdriver
from config import Config
from selenium.webdriver.chrome.options import Options
from BeautifulSoupScraper import scrape_profile_page, scrapeFollowers, scrapeFollowings
import time

def main():
    # SCRAPE INSTAGRAM PROFILE
    # scrape_from_instagram()

    # SCRAPE FACEBOOK PROFILE
    following_list = scrape_from_facebook()
    for p in following_list:
        print(p)

def scrape_from_instagram():
    # SCRAPE INSTAGRAM PROFILE
    config = Config()
    baseUser = config.get_insta_username()

    # Initialize WebDriver
    options = Options()
    options.add_argument("--lang=en")
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)

    # Perform login
    driver.get("https://www.instagram.com/accounts/login/")
    login_instagram(driver, baseUser, config.get_insta_password())

    # Scrape the person
    person = scrapePersonFromInstagram(baseUser, driver)
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
        temp_person = scrapePersonFromInstagram(pers, driver)
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

    return following_people_list

def scrape_from_facebook():
    # SCRAPE FACEBOOK PROFILE
    config = Config()
    baseUser = config.get_fb_username()

    # Initialize WebDriver
    options = Options()
    options.add_argument("--lang=en")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)

    # Perform login
    driver.get("https://www.facebook.com/")
    login_facebook(driver, config.get_fb_username(), config.get_fb_password())
    time.sleep(3)

    # Scrape the person
    person = scrapePersonFromFacebook(baseUser, driver)
    time.sleep(2)

    # Get the followings
    followings = scrapeFollowings(f"pages/fb_{person.username}_following.html")
    person.add_following_list(followings)

    following_list = []
    for following in followings:
        temp_person = scrapePersonFromFacebook(following, driver)
        time.sleep(2)
        
        following_followings = scrapeFollowings(f"pages/fb_{temp_person.username}_following.html")
        temp_person.add_following_list(following_followings)
        following_list.append(temp_person)

    return following_list

if __name__ == "__main__":
    main()