import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from pynput.mouse import Button, Controller
from selenium.common.exceptions import NoAlertPresentException
import time, pyautogui, random
from datetime import datetime, timedelta

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
    
    for i, link in enumerate(url_list):
        time.sleep(2)


        print(f"{i+1}/{len(url_list)} Checking Conditions For {link}")

        has_not_been_logged_flag=False
        
        driver.get(link)
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
                pyautogui.hotkey("control-law -firm -attorney ", "0-law -firm -attorney ", interval=0.3)
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
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn') and contains(@class, 'btn-link') and contains(., 'compose')]"))).click()
                    
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

            print(f"Successfully Sequenced For {link}")

        
        except Exception as e:
            
            print(f"An error occurred: {e}")
           
            continue


def ahrefs_year_passed(date_str):
    date_provided = datetime.strptime(date_str, "%d %b %Y")
    current_date = datetime.now()
    difference = current_date - date_provided
    has_been_a_year = difference.days >= 365
    return has_been_a_year, difference.days

if (__name__ == '__main__'):
    options = Options()
    options.add_argument('--user-data-dir=/Users/dynas/AppData/Local/Google/Chrome/User Data/HelloWorld29')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    mouse = Controller()

    search_topic = [
    ]
    for topic in search_topic:
        driver.get(f"https://www.google.com/search?q={topic}")
        ahrefs_listing_links = []

        try:
            serp_listings = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "MjjYud"))
            )
            if (len(serp_listings) > 10): serp_listings[:10] 
            for listing in serp_listings: 
                try:
                    listing_link = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    ahrefs_listing_links.append(listing_link)
                except Exception:
                    continue
        except Exception:
            continue


    gather_filtered_links =[]
    
    for ahrefs_link in ahrefs_listing_links:
        
        driver.get(f"https://app.ahrefs.com/v2-site-explorer/refdomains/subdomains?target={ahrefs_link}")

        try:
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/main/div[1]/div[3]/div/div/div[2]/div/div[1]/div/div/table/tbody[1]/tr/th[2]/div').click()

            ahrefs_listing_analytics = driver.find_element(By.XPATH, '//tr[@class="css-5xi7tf-row"]')

            for ahrefs_dashboard_listing in ahrefs_listing_links:
                try:
                    ahrefs_listing_date = ahrefs_dashboard_listing.find_elements(By.XPATH, "css-1llwqnd-row css-1mq5fur-row css-87ebjr-rowAlign")[0]
                except Exception:
                    continue
                try:
                    ahrefs_listing_da = ahrefs_dashboard_listing.find_elements(By.XPATH, "css-1j01j1v-cell css-0 css-wyn6ja css-i12leo css-l1bucl-cellBorderTop css-s2uf1z css-hd1s65-cellVAlign css-epvm6")[0]
                except Exception:
                    continue

                if (ahrefs_year_passed(ahrefs_listing_date)):
                    if (0 <= ahrefs_listing_da <= 16):
                        try:
                            filtered_link = ahrefs_dashboard_listing.find_element(By.XPATH, 'css-syaaed-url css-p3817k-linkBreakWord')[0]
                            gather_filtered_links.append(filtered_link)
                        except Exception:
                            pass
                    else: break

                try:
                    driver.find_elements(By.XPATH, "css-9hzt1j-button")[0].click()
                except Exception:
                    continue
                    
        except Exception:
            continue


    try:
        check_and_send(gather_filtered_links)
    except Exception:
        pass
        



