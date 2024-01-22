from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from datetime import datetime
from pynput.mouse import Button, Controller
import time, pyautogui, random

counter = 0

def scroll_down():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="botstuff"]/div/div[3]/div[4]/a[1]/h3/div'))
                )
                element.click()
            except Exception:
                break
        last_height = new_height
    
def get_filter_urls(min_da, max_da):
    urls = []
    serp_listings = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "MjjYud"))
    )
    for listing in serp_listings:
        try:
            da_element = listing.find_element(By.XPATH, ".//div[contains(@class, 'ah_serpbar__item-inner')]/span[contains(@class, 'ah_serpbar__item-label') and text()='dr']/following-sibling::span[contains(@class, 'ah_serpbar__item-data')]")
            da_number = float(da_element.text)
            
            if min_da <= da_number <= max_da:
                listing_link = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if listing_link.endswith((".pdf", ".gov", ".edu")):
                    continue
                print(f"Domain Authority: {da_number} Link: {listing_link}")
                urls.append(listing_link)
        except Exception as e:
            print(e)
            continue
    return urls

def check_if_more_than_two_months(date_str, current_date=datetime.now()):
    try:
        # Handle case where date_str is in time format like '2:10 pm'
        if ':' in date_str:
            # Assuming the time is for the current date
            date_obj = datetime.combine(current_date.date(), datetime.strptime(date_str, '%I:%M %p').time())
        elif len(date_str) <= 6:
            # Original logic for 'Jan 01' format
            date_obj = datetime.strptime(date_str + ' ' + str(current_date.year), '%b %d %Y')
            if date_obj > current_date:
                date_obj = datetime.strptime(date_str + ' ' + str(current_date.year - 1), '%b %d %Y')
        else:
            # Original logic for 'mm/dd/yy' format
            date_obj = datetime.strptime(date_str, '%m/%d/%y')
            if date_obj.month > current_date.month or (date_obj.month == current_date.month and date_obj.day > current_date.day):
                date_obj = date_obj.replace(year=date_obj.year - 1)
        
        return (current_date - date_obj).days >= 60
    except ValueError:
        return False
    

# IF NEED TO ADD PROJECT, ADD TO STREAM
# CHECK IF RESEARCH PAGE URL EXISTS

def check_and_send(url_list):
    
    for i, link in enumerate(url_list):

        print(f"{i+1}/{len(url_list)} Checking Conditions For {link}")

        has_not_been_logged_flag=False
        
        driver.get(link)
        pyautogui.hotkey("command", "0", interval=0.5)
        
        # Buzzstream_open = True

        # CASE IF BUZZ STREAM HAS NOT LOGGED THIS CURRENT SITE
        # FIRST VALIDATE EMAILS IF ALL EMAILS ARE VALID
        # SECOND CLICK ON SAVE TO BUZZSTREAM BUTTON
        # SINCE IT HAS LOGGED IN BUZZ STREAM SET LOGGED FLAG = FALSE
        # (IF NOT FLAG) IGNORE DATE

        try:
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "buzzstream-extension-form"))
            )
            driver.switch_to.frame(iframe)
                
            try:
                save_buzzstream_button_exist = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//save-button[@ng-click='persistChanges()']/button"))
                    
                )
                has_not_been_logged_flag = True
            except Exception:
                pass

            if (has_not_been_logged_flag):
                try: 
                    email_list = WebDriverWait(driver, 3).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//contact-info-field[@placeholder='Email']//input[@type='text']"))
                    )
                    if (email_list): 
                        save_buzzstream_button_exist.click()

                except Exception:
                    print("No Email List or No Valid Emails Found! ")
                    pyautogui.hotkey("command", "0", interval=0.3)
                    continue
                
            time.sleep(1)


            # CASE CHECK TIME STAMP DATE
            # IF IT HAS NOT BEEN MORE THAN TWO MONTHS AND NOT BEEN MARKED AS LOGGED: MOVE TO NEXT SITE

            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[@ng-class=\"{ active: isCurrentPath('/history') }\"]")) 
                ).click()
            except Exception:
                print("Cannot click history")

            try:

                try:
                    time_date_stamp = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH,"//span[@class='chronicle-timestamp']"))
                    ).text
                except Exception:
                    print("could not find time date stamp")
                    pass
                
                if (not check_if_more_than_two_months(time_date_stamp) and not has_not_been_logged_flag):
                    print(f"Last Date: {time_date_stamp} not been more than 2 Months or not. Skipping... ")
                    pyautogui.hotkey("command", "0", interval=0.3)
                    continue
            except Exception:
                pyautogui.hotkey("command", "0", interval=0.3)
                continue

            print(f"Last Date: {time_date_stamp} Moving Forward ")

            # CHECK IF IN SEQUENCE
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[@ng-class=\"{ active: isCurrentPath('/qualify') }\"]"))
                ).click()
            except Exception:
                pyautogui.hotkey("command", "0", interval=0.3)
                continue
        
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'card-right')]//button[contains(@class, 'btn-primary') and text()='Add']"))
                ).click()
            except Exception as e:
                pass

            try:
                research_page_url_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "Research Page Url"))
                )
                research_page_url = research_page_url_element.get_attribute('value')

                if (not research_page_url):
                    pyautogui.hotkey("command", "0", interval=0.3)
                    continue
            except Exception as e:
                pyautogui.hotkey("command", "0", interval=0.3)
                continue

            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn') and contains(@class, 'btn-link') and contains(., 'compose')]"))).click()
            except Exception:
                pyautogui.hotkey("command", "0", interval=0.3)
                continue
            
            time.sleep(2)
            mouse.position = (850, 880)
            mouse.click(Button.left, 1)
            time.sleep(2)

            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[@ng-class=\"{ active: isCurrentPath('/') }\"]"))
                ).click()
            except Exception:
                continue

            driver.switch_to.default_content()
            pyautogui.hotkey("command", "0", interval=0.3)
            print(f"Successfully Sequenced For {link}")
            count += 1
        
        except Exception as e:
            
            print(f"An error occurred: {e}")
           
            continue
            

if (__name__ == '__main__'):
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

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("document.body.style.zoom='70%'")
    action = ActionChains(driver)
    mouse = Controller()


    # mental-health-links, mental-health-resources, mental-health-links
    # gov, no edu, huge websites
    # Outbound links > 20
    # 

    search_queries =[
    'inurl:resources progressive overload cardio -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:links cardio training -site:.gov -site:.edu inurl:resources OR inurl:links',
    'intitle:fitness progressive overload site:.org -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:blog VO2 max training -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:health endurance training site:.edu -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:fitness cardio workouts -site:.gov -site:.edu inurl:resources OR inurl:links',
    'intitle:training increase endurance site:.gov -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:articles cardiovascular fitness -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:tips progressive cardio -site:.gov -site:.edu inurl:resources OR inurl:links',
    'intitle:health building endurance site:.net -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:guides improving VO2 max -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:advice cardio exercises -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:info progressive overload in fitness -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:faq cardio training tips -site:.gov -site:.edu inurl:resources OR inurl:links',
    'intitle:workouts enhancing endurance site:.com -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:community fitness training -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:forum cardio fitness -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:discussion endurance sports -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:news VO2 max improvement -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:updates progressive training -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:support cardiovascular health -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:help fitness methods -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:content overload principle in cardio -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:directory endurance exercises -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:hub cardio workout plans -site:.gov -site:.edu inurl:resources OR inurl:links',
    'intitle:fitness progressive overload strategies site:.org -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:techniques improving cardio fitness -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:ideas VO2 max workouts -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:insights endurance training methods -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:experts cardio training principles -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:knowledge progressive overload benefits -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:learn maximizing endurance -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:research cardio training science -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:science fitness overload -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:studies cardiovascular improvements -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:reports endurance workout tips -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:statistics VO2 max data -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:data progressive cardio training -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:analysis fitness endurance -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:overview cardio overload techniques -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:summary endurance building -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:concepts cardio fitness training -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:principles maximizing VO2 max -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:approaches endurance training plans -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:strategies cardio workout efficiency -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:methods progressive overload in cardio -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:techniques enhancing cardiovascular fitness -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:practices cardio training tips -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:case-studies endurance sports training -site:.gov -site:.edu inurl:resources OR inurl:links',
    'inurl:examples VO2 max increasing workouts -site:.gov -site:.edu inurl:resources OR inurl:links'
]
    

    for search_operator in search_queries:
        if (counter == 170): break
        try:
            time.sleep(random.randrange(1, 5))
            driver.get(f"https://www.google.com/search?q={search_operator}")
            scroll_down()
            urls = get_filter_urls(1, 21)
            check_and_send(urls)
        except Exception:
            continue

    #https://www.providencetherapybc.com/resources
    #https://braininjuryconnectionsnw.org/resources/health-care-and-alternative-medical-practices/counselors-and-mental-health/
    # check_and_send(["https://www.goshen1.org/resources/parents/mental_health_resources.php"])
    

    time.sleep(9999)
    driver.quit()