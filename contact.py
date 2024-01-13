from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
import time, random, csv, os
import pyautogui

# VIRTUAL MACHINE

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-geolocation")
chrome_options.add_argument("--remote-allow-origins=*")

chrome_options.add_argument('user-data-dir=/Users/williamzhao/Library/Application Support/Google/Chrome/')
chrome_options.add_argument("--profile-directory=Profile 1")
chrome_options.add_argument("--start-maximized")
service = Service(executable_path='/opt/homebrew/bin/chromedriver')
chrome_options.add_extension(r'buzzstream.crx')


driver = webdriver.Chrome(service=service, options=chrome_options)
# driver.fullscreen_window()

# Project Boating Safety
google_search_operators = [
    "https://www.google.com/search?q=boat-ed.com+inurl:resources",
    "https://www.google.com/search?q=asdasd123"
    "https://www.google.com/search?q=boating+safety+marinas+inurl:.org/resources"
]

action = ActionChains(driver)

def scroll_down():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            try:
                element = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="botstuff"]/div/div[3]/div[4]/a[1]/h3/div'))
                )
                element.click()
            except Exception:
                break
        last_height = new_height

def highlight_contacts():
    
    whitespace_element = driver.find_element(By.TAG_NAME, "body")
    action.key_down(Keys.CONTROL).click(whitespace_element).key_up(Keys.CONTROL).perform()
    for j in range(12):pyautogui.press('down')
    pyautogui.press('return')
    for j in range(3):pyautogui.press('down')
    pyautogui.press('enter')
    

def get_all_urls():
    urls = []
    serp_listings = driver.find_elements(By.CLASS_NAME, "MjjYud")
    for listing in serp_listings:
        try:
            urls.append(listing.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        except:
            continue
    return urls


def check_and_send(url_list):
    for link in url_list:

        # OPEN BuzzMarker

        # Switch to BuzzMarker Iframe

        







driver.get("https://www.google.com/search?q=boat-ed.com+inurl:resources")
scroll_down()
highlight_contacts()
urls = get_all_urls()


time.sleep(9999)
driver.quit()