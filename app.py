from SeleniumInstagram import login_instagram, scrapePersonFromInstagram
from SeleniumFacebook import login_facebook, scrapePersonFromFacebook
from selenium import webdriver
from SimilarityComparisons import jaro_winkler, tfidf_cosine_similarity, image_similarity, combined_similarity, edit_distance, esa_similarity
from config import Config
from Person import Person
from selenium.webdriver.chrome.options import Options
from BeautifulSoupScraper import scrape_profile_page, scrapeFollowers, scrapeFollowings
from typing import List, Dict
from tabulate import tabulate
import time
import pandas as pd

def main():
    # SCRAPE INSTAGRAM PROFILE
    person_insta = scrape_from_instagram()
    print("BASE USER:\n", person_insta)
    print("Followings:")
    for p in person_insta.following:
        print(p)

    time.sleep(5)

    # SCRAPE FACEBOOK PROFILE
    person_fb = scrape_from_facebook()
    print("BASE USER:\n", person_fb)
    print("Followings:")
    for p in person_fb.following:
        print(p)


    result = compare_accounts(person_insta, person_fb)
    print("\n")
    print(result)

def scrape_from_instagram():
    # SCRAPE INSTAGRAM PROFILE
    config = Config()
    baseUser = config.get_insta_username()

    # Initialize WebDriver
    options = Options()
    options.add_argument("--lang=en")
    #options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)

    # Perform login
    driver.get("https://www.instagram.com/accounts/login/")
    login_instagram(driver, baseUser, config.get_insta_password())

    # Scrape the person
    person = scrapePersonFromInstagram(baseUser, driver)
    time.sleep(3)

    # Get the followers
    person = scrape_profile_page(f"pages/{person.username}.html")
    # follower_list = scrapeFollowers(f"pages/{person.username}_followers.html")
    following_list = scrapeFollowers(f"pages/{person.username}_following.html")
    print(following_list)
    #person.add_followers_list(follower_list)
    #person.add_following_list(following_list)

    # Get the followers and following of the followings
    for pers in following_list:
        temp_person = scrapePersonFromInstagram(pers, driver)
        time.sleep(3)
        temp_person = scrape_profile_page(f"pages/{pers}.html")
        print(temp_person)
        # follower_list_temp = scrapeFollowers(f"pages/{pers}_followers.html")
        # following_list_temp = scrapeFollowers(f"pages/{pers}_following.html")
        # temp_person.add_followers_list(follower_list_temp)
        # temp_person.add_following_list(following_list_temp)
        if temp_person is not None:
            person.add_following(temp_person)

    # Close the WebDriver
    driver.quit()

    print("Followings: ")
    for p in person.following:
        print(p)

    return person

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
    person = scrapePersonFromFacebook(baseUser, driver, True)
    time.sleep(2)

    # Get the followings
    img_urls, followings_usernames = scrapeFollowings(f"pages/fb_{person.username}_following.html")

    # Scraping the followings of the base user
    following_list: List[Person] = []
    for following, url in zip(followings_usernames, img_urls):
        # Scrape the followed person or page
        temp_person = scrapePersonFromFacebook(following, driver, False)
        temp_person.set_url(url)
        following_list.append(temp_person)
        time.sleep(2)
    
    # Close the WebDriver
    driver.quit()
    
    person.following = following_list

    return person

# Comparison Functions
def compare_persons(person1: Person, person2: Person, weights: Dict[str, float]):
    name_similarity = tfidf_cosine_similarity(person1.name, person2.name)
    username_similarity = jaro_winkler(person1.username, person2.username)
    bio_similarity = esa_similarity(person1.bio, person2.bio)
    picture_similarity = edit_distance(person1.profile_picture_url, person2.profile_picture_url)

    return {
        'name_similarity': name_similarity,
        'username_similarity': username_similarity,
        'bio_similarity': bio_similarity,
        'picture_similarity': picture_similarity
    }

def compare_followings(following1: List[Person], following2: List[Person], weights: Dict[str, float]):
    if not following1 or not following2:
        return {
            'following_similarity': 0.0,
            'details': []
        }
    
    total_similarity = 0.0
    comparisons = 0
    details = []
    
    for person1 in following1:
        best_similarity = 0.0
        best_match_details = None
        for person2 in following2:
            person_similarities = compare_persons(person1, person2, weights)
            similarity = combined_similarity(
                person_similarities['name_similarity'],
                person_similarities['username_similarity'],
                person_similarities['bio_similarity'],
                person_similarities['picture_similarity'],
                0, weights)  # Following similarity is 0 in this case

            if similarity > best_similarity:
                best_similarity = similarity
                best_match_details = {
                    'match_with': person2.username,
                    'similarities': person_similarities,
                    'combined_similarity': similarity
                }

        total_similarity += best_similarity
        comparisons += 1
        if best_match_details:
            details.append({
                'person': person1.username,
                'best_match': best_match_details
            })

    average_similarity = total_similarity / comparisons if comparisons > 0 else 0.0

    return {
        'following_similarity': average_similarity,
        'details': details
    }

def compare_accounts(person_insta, person_fb, output_file='account_comparison.xlsx'):
    # Define weights for each similarity measure based on the given table
    weights = {
        'username': 0.30,
        'following': 0.30,
        'name': 0.20,
        'picture': 0.10,
        'bio': 0.10
    }

    account_similarities = compare_persons(person_insta, person_fb, weights)
    
    following_comparison = compare_followings(person_insta.following, person_fb.following, weights)
    
    combined_score = combined_similarity(
        account_similarities['name_similarity'],
        account_similarities['username_similarity'],
        account_similarities['bio_similarity'],
        account_similarities['picture_similarity'],
        following_comparison['following_similarity'],
        weights
    )

    # Prepare data for the main table
    main_table = [
        ["Attribute", "Instagram", "Facebook", "Similarity Score"],
        ["Name", person_insta.name, person_fb.name, account_similarities['name_similarity']],
        ["Username", person_insta.username, person_fb.username, account_similarities['username_similarity']],
        ["Bio", person_insta.bio, person_fb.bio, account_similarities['bio_similarity']],
        ["Profile Picture", person_insta.profile_picture_url, person_fb.profile_picture_url, account_similarities['picture_similarity']],
        ["Following Similarity", "-", "-", following_comparison['following_similarity']],
        ["Total Combined Score", "-", "-", combined_score]
    ]
    
    # Prepare data for the following comparison details table
    details_table = []
    for detail in following_comparison['details']:
        best_match = detail['best_match']
        similarities = best_match['similarities']
        details_table.append([
            detail['person'],
            best_match['match_with'],
            similarities['name_similarity'],
            similarities['username_similarity'],
            similarities['bio_similarity'],
            similarities['picture_similarity'],
            best_match['combined_similarity']
        ])

    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    # Convert the main table to a DataFrame and write to Excel
    df_main = pd.DataFrame(main_table[1:], columns=main_table[0])
    df_main.to_excel(writer, sheet_name='Account Comparison', index=False)

    # Convert the details table to a DataFrame and write to Excel
    details_table_columns = ["Instagram Following", "Best Match", "Name Sim", "Username Sim", "Bio Sim", "Picture Sim", "Combined Sim"]
    df_details = pd.DataFrame(details_table, columns=details_table_columns)
    df_details.to_excel(writer, sheet_name='Following Comparison Details', index=False)

    # Save the Excel file
    writer.close()

    print(f"Comparison results have been written to {output_file}")

    result = {
        'account_similarities': account_similarities,
        'following_comparison': following_comparison,
        'total_combined_score': combined_score
    }
    
    return result

""" person_insta = Person("Burcu Kaplan", "burcukaplan__", "https://scontent.cdninstagram.com/v/t51.2885-19/376243407_264333966526920_2972655541866789887_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent.cdninstagram.com&_nc_cat=100&_nc_ohc=7YaNmMbX50QQ7kNvgGvWRHX&edm=APs17CUBAAAA&ccb=7-5&oh=00_AYAcpTEmCYdQdj1C21LpfqLZZY3p-LxIEOQDbVQ7JDXvvg&oe=664EEBAA&_nc_sid=10d13b", "⋆ Bilkent University | CS ⋆ ✈️", 1063, 1008, "instagram")
person_fb = Person("Burcu Kaplan", "burcutitizkaplan", "https://scontent.fasr2-1.fna.fbcdn.net/v/t39.30808-1/375596737_10227499278220272_9017250208179668883_n.jpg?stp=dst-jpg_p200x200&_nc_cat=106&ccb=1-7&_nc_sid=5f2048&_nc_ohc=nH5_SBlYxFcQ7kNvgFydrOY&_nc_ht=scontent.fasr2-1.fna&oh=00_AYDMPOw8elVkU7qFIvaviw9L093kDpmzDybdfDoJvPzqzw&oe=664ED4A9", "", -1, -1, "facebook")

score = compare_accounts(person_insta, person_fb)
print(score)  """

if __name__ == "__main__":
    main()