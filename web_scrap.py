#Store movie name,language,ua from Mumbai location from BookMyShow and store it in MongoDB

import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['bookmyshowdb']
collection = db['movies_mumbai']
collection.delete_many({})

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 20)

driver.get("https://in.bookmyshow.com/")

try:
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]')))
    search_box.send_keys("Mumbai")
    mumbai_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul//li[contains(., 'Mumbai')]")))
    mumbai_option.click()
except:
    driver.quit()
    exit()

wait.until(EC.url_contains("mumbai"))
driver.get("https://in.bookmyshow.com/explore/movies-mumbai")
last_height = driver.execute_script("return document.body.scrollHeight")
scroll_attempts = 0
max_scroll_attempts = 20

while scroll_attempts < max_scroll_attempts:
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(random.uniform(1.5, 2.5))

    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        scroll_attempts += 1
    else:
        last_height = new_height
        scroll_attempts = 0

movies = driver.find_elements(By.CSS_SELECTOR, "a.sc-133848s-11")

for movie in movies:
    try:
        name = movie.find_element(By.CSS_SELECTOR, "div.sc-7o7nez-0.elfplV").text
        details = movie.find_elements(By.CSS_SELECTOR, "div.sc-7o7nez-0.bsZIkT")

        ua_rating = details[0].text if len(details) > 0 else "N/A"
        language = details[1].text if len(details) > 1 else "N/A"

        collection.insert_one({
            "name": name,
            "ua_rating": ua_rating,
            "language": language
        })
    except:
        continue

driver.quit()
print(f"Total Movies Scraped and Saved: {collection.count_documents({})}")