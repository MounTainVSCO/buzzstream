import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from pynput.mouse import Button, Controller
from selenium.common.exceptions import NoAlertPresentException
import time, pyautogui, random, math
import requests
from selenium_recaptcha_solver import RecaptchaSolver


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
    print(serp_listings)
    
    if (len(serp_listings) > 20):
        serp_listings[:20]
    for listing in serp_listings:
        try:
            da_element = listing.find_element(By.XPATH, ".//div[contains(@class, 'ah_serpbar__item-inner')]/span[contains(@class, 'ah_serpbar__item-label') and text()='dr']/following-sibling::span[contains(@class, 'ah_serpbar__item-data')]")
            da_number = float(da_element.text)
            
            if min_da <= da_number <= max_da:
            
                listing_links = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if ("gov" not in listing_links and "pdf" not in listing_links and "wordpress" not in listing_links and "wix" not in listing_links and "squarespace" not in listing_links and "weebly" not in listing_links):
                    print(f"Domain Authority: {da_number} links: {listing_links}")
                    urls.append(listing_links)
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

def check_and_send(url_list):
    
    for i, links in enumerate(url_list):
        time.sleep(2)


        print(f"{i+1}/{len(url_list)} Checking Conditions For {links}")

        has_not_been_logged_flag=False
        
        driver.get(links)
        mouse.position = (-1500, 1020)
        mouse.click(Button.left, 1)
        pyautogui.keyDown('ctrl')
        time.sleep(0.1)
        pyautogui.press('0')
        pyautogui.keyUp('ctrl')


        
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
                    email_list = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//contact-info-field[@placeholder='Email']//input[@type='text']"))
                    )
                    if (email_list): 
                        save_buzzstream_button_exist.click()

                except Exception:
                    print("No Email List or No Valid Emails Found! ")
                    pyautogui.keyDown('ctrl')
                    time.sleep(0.1)
                    pyautogui.press('0')
                    pyautogui.keyUp('ctrl')
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
                    pyautogui.keyDown('ctrl')
                    time.sleep(0.1)
                    pyautogui.press('0')
                    pyautogui.keyUp('ctrl')
                    continue
            except Exception:
                pyautogui.keyDown('ctrl')
                time.sleep(0.1)
                pyautogui.press('0')
                pyautogui.keyUp('ctrl')
                continue

            print(f"Last Date: {time_date_stamp} Moving Forward ")

            # CHECK IF IN SEQUENCE
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[@ng-class=\"{ active: isCurrentPath('/qualify') }\"]"))
                ).click()
            except Exception:
                pyautogui.hotkey("control","0", interval=0.3)
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
                    pyautogui.keyDown('ctrl')
                    time.sleep(0.1)
                    pyautogui.press('0')
                    pyautogui.keyUp('ctrl')
                    driver.switch_to.default_content()
                    continue
            except Exception as e:
                pyautogui.keyDown('ctrl')
                time.sleep(0.1)
                pyautogui.press('0')
                pyautogui.keyUp('ctrl')
                driver.switch_to.default_content()
                continue

            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div/react-component/div/div/div/div[3]/div[1]/div/button"))).click()
                    
            except Exception:
                pyautogui.keyDown('ctrl')
                time.sleep(0.1)
                pyautogui.press('0')
                pyautogui.keyUp('ctrl')
                driver.switch_to.default_content()
                continue
            
            time.sleep(2)
            mouse.position = (1025, 1020)
            mouse.click(Button.left, 1)
            time.sleep(1)
            mouse.position = (1025, 980)
            mouse.click(Button.left, 1)
            time.sleep(1)

            try:
                alert = driver.switch_to.alert
                pyautogui.keyDown('ctrl')
                time.sleep(0.1)
                pyautogui.press('0')
                pyautogui.keyUp('ctrl')
                driver.switch_to.default_content()
                continue
            except NoAlertPresentException:
                pass

            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[@ng-class=\"{ active: isCurrentPath('/') }\"]"))
                ).click()
            
            except Exception:
                continue

            driver.switch_to.default_content()
            pyautogui.keyDown('ctrl')
            time.sleep(0.1)
            pyautogui.press('0')
            pyautogui.keyUp('ctrl')

            print(f"Successfully Sequenced For {links}")

        
        except Exception as e:
            
            print(f"An error occurred: {e}")
           
            continue

if (__name__=="__main__"):

    options = Options()
    options.add_argument('--user-data-dir=/Users/dynas/AppData/Local/Google/Chrome/User Data/HelloWorld29')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    solver = RecaptchaSolver(driver=driver)




    # time.sleep(30)
    counter = 0
    mouse = Controller()

    search_operators =[
    '"trauma" vehicle accident (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca'
    '"traumatic brain injury" + "vehicle accident"(inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"PTSD" mental health (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"depression" + "vehicle accident" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"emotional trauma" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"accident recovery" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"traumatic stress" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"mental health support" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"coping strategies" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"stress management" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma therapy" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"grief counseling" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"emotional healing" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"survivor support" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma recovery" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"accident trauma" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma impacts" intext:wordpress OR intext:squarespace OR intext:weebely OR intext:weebly OR intext:wix OR inurl:resources OR inurl:link after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"psychological trauma" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma symptoms" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma healing" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"accident aftermath" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma intervention" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma research" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma resources" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"emotional distress" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma awareness" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma prevention" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"mental health awareness" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma and society" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca',
    '"trauma recovery programs" (inurl:links OR inurl:resources) AND (intext:wordpress OR intext:squarespace OR intext:weebly OR intext:wix) after:2023 -law -firm -attorney -llc -.au -.uk -.ca'
]




    filtered_urls=[]
    for search_operator in search_operators:
        driver.get(f"https://www.google.com/search?q={search_operator}")

        try:
            
            recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
            solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        except Exception:
            pass

        try:
            time.sleep(random.randrange(1, 5))
            scroll_down()
            hi = get_filter_urls(1, 16)
            check_and_send(hi)
            
        except Exception:
            continue

    #https://www.providencetherapybc.com/resources
    #https://braininjuryconnectionsnw.org/resources/health-care-and-alternative-medical-practices/counselors-and-mental-health/
    # check_and_send(["https://www.goshen1.org/resources/parents/mental_health_resources.php"])
    

    time.sleep(9999)
    driver.quit()