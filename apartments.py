import time
import os
import json
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


service = Service(ChromeDriverManager().install())  

driver = webdriver.Chrome(service=service)

URL_FILE = "URLs.json"

def load_urls():
    global URL_FILE
    if os.path.exists(URL_FILE):
        with open(URL_FILE, "r") as f:
            return json.load(f)
    return []

def save_urls():
    global urls
    with open(URL_FILE, "w") as f:
        json.dump(urls,f,indent=2)

def add_url_if_new(new_url):
    global urls
    if new_url not in urls:
        urls.append("NEW: ")
        urls.append(new_url)
        save_urls()

def clean_urls():
    global urls
    urls = [url for url in urls if url != "NEW: "]

driver.get("https://www.apartments.com/off-campus-housing/on/toronto/university-of-toronto-main-campus/min-2-bedrooms-under-2700/?mid=20250901")

def my_click(Xpath):
    time.sleep(3)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, Xpath))
    )
    button = driver.find_element(By.XPATH, Xpath)
    button.click()

def click_apt(index):
    my_click(f'//*[@id="placardContainer"]/ul/li[{index}]')
    if is_good_apt():
        current_url = driver.current_url
        add_url_if_new(current_url)
    driver.back()
    time.sleep(3)
    if (driver.find_elements(By.XPATH,f'//*[@id="paging"]/ol/li[{index+1}]')):
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",driver.find_element(By.XPATH,f'//*[@id="paging"]/ol/li[{index+1}]' ))
    return driver.find_elements(By.XPATH, f'//*[@id="placardContainer"]/ul/li[{index + 1}]')


def next_page(index):
    my_click(f'//*[@id="paging"]//li[.//a[text()="{index}"]]')
    return(driver.find_elements(By.XPATH, f'//*[@id="paging"]/ol/li[{index}]'))

def check_page():
    count = 1
    while click_apt(count):
        count += 1


def check_all_apts():
    count = 2
    while next_page(count):
        if count >= 10:
            check_page()
        count += 1

def is_good_apt():
    global client
    description = "" 
    try:
        description = driver.find_element(By.XPATH, '//*[@id="descriptionSection"]/p[1]').text
    except:
        print("no description found")

    if description:
        try:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are a strict assistant. Only answer with one word: 'Yes' or 'No'. Do not explain. Do not say both. Just reply with either Yes or No."},
            {"role": "user", "content": f"Based on this apartment's description does it have 2 bedrooms, or is it not explicitly 2 bedrooms, does it have something else like for example, one bedroom plus one den, or one bedroom plus one closet etc? Description: {description}"}
            ],
            temperature=0
            )
            time.sleep(1)
            reply = response.choices[0].message.content.strip().lower()
            return "yes" in reply
        except Exception as e:
           print("openai error ", e)
           return False

urls = load_urls()
clean_urls()
my_click('//*[@id="onetrust-close-btn-container"]/button')
check_page()
check_all_apts()
check_page()
save_urls()
input("press Enter to end the script... ")