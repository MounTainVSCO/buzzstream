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
from selenium_recaptcha_solver import RecaptchaSolver
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
    serp_listings = WebDriverWait(driver, 10).until(
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
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "buzzstream-extension-form"))
            )
            driver.switch_to.frame(iframe)
                
            try:
                save_buzzstream_button_exist = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//save-button[@ng-click='persistChanges()']/button"))
                    
                )
                has_not_been_logged_flag = True
            except Exception:
                pass

            if (has_not_been_logged_flag):
                try: 
                    email_list = WebDriverWait(driver, 10).until(
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


            # CHECK IF IN SEQUENCE
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//li[@ng-class=\"{ active: isCurrentPath('/qualify') }\"]"))
                ).click()
            except Exception:
                pyautogui.hotkey("command", "0", interval=0.3)
                continue
        
            try:
                # XPath to locate the specified element
                xpath = "//div[@class='pr-4 pl-4']//div[@class='alert alert-warning']//div[contains(text(), 'Warning: Contact is in an active sequence for this project')]"
                element = driver.find_element(By.XPATH, xpath)
                if (element):
                    continue
            except:
                pass
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'card-right')]//button[contains(@class, 'btn-primary') and text()='Add']"))
                ).click()
            except Exception as e:
                pass

            try:
                research_page_url_element = WebDriverWait(driver, 10).until(
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
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex-grow-1') and contains(@class, 'text-right') and contains(@class, 'position-absolute')]//button[contains(@class, 'btn') and contains(@class, 'btn-link') and contains(., 'compose')]"))).click()
            except Exception:
                pyautogui.hotkey("command", "0", interval=0.3)
                continue
            
            time.sleep(2)
            mouse.position = (850, 880)
            mouse.click(Button.left, 1)
            time.sleep(2)

            try:
                WebDriverWait(driver, 10).until(
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
    chrome_options.add_argument('user-data-dir=/Users/dynas/AppData/Local/Google/Chrome/User Data/Default')
    chrome_options.add_argument("--profile-directory=Profile 1")
    chrome_options.add_argument("--start-maximized")
    service = Service(executable_path='/Users/dynas/buzzstream/chromedriver.exe')

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("document.body.style.zoom='70%'")
    action = ActionChains(driver)
    mouse = Controller()
    solver = RecaptchaSolver(driver=driver)


    # mental-health-links, mental-health-resources, mental-health-links
    # gov, no edu, huge websites
    # Outbound links > 20
    # 

    search_operators = [
    "common 'car seat' mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' installation errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' safety tips inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "incorrect 'car seat' usage inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' adjustment mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' strap errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "forward-facing 'car seat' issues inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "rear-facing 'car seat' mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "booster seat common errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "child safety seat installation inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "best 'car seat's for safety inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' law compliance errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "choosing the right 'car seat' inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' belt mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' latch system errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "proper 'car seat' fit guide inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' expiration mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "second-hand 'car seat' risks inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' cleaning errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' manual mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "infant 'car seat' setup errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "convertible 'car seat' mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "all-in-one 'car seat' errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "travel system 'car seat' mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' head support errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' sunshade mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' winter cover errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' mirror setup mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' toy attachment errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' replacement guide inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' recall mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' base installation errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' canopy mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' angle adjuster errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' for preemies mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' for toddlers errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' for small cars mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' weight limit errors inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' height limit mistakes inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023",
    "'car seat' safety standards inurl:wordpress OR inurl:squarespace OR inurl:.org OR inurl:resources OR inurl:link OR inurl:archive after:2023"
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
            hi = get_filter_urls(0, 16)
            check_and_send(hi)
            
        except Exception:
            continue