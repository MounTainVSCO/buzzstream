import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from pynput.mouse import Button, Controller
from selenium.common.exceptions import NoAlertPresentException
import time, pyautogui
from datetime import datetime
from selenium_recaptcha_solver import RecaptchaSolver



def scroll_to_end_of_page():

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for the page to load
        time.sleep(2)  # Adjust the sleep time as necessary
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # If heights are the same, it means we've reached the bottom
        last_height = new_height

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

        try:

            print(f"{i+1}/{len(url_list)} Checking Conditions For {link}")

            has_not_been_logged_flag=False
            
            driver.get(link)
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
                        email_list = WebDriverWait(driver, 3).until(
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
                    pyautogui.hotkey("control", "0", interval=0.3)
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
                        continue
                except Exception as e:
                    pyautogui.keyDown('ctrl')
                    time.sleep(0.1)
                    pyautogui.press('0')
                    pyautogui.keyUp('ctrl')
                    continue

                try:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn') and contains(@class, 'btn-link') and contains(., 'compose')]"))).click()
                except Exception:
                    pyautogui.keyDown('ctrl')
                    time.sleep(0.1)
                    pyautogui.press('0')
                    pyautogui.keyUp('ctrl')
                    continue
                
                time.sleep(2)
                mouse.position = (1025, 1020)
                mouse.click(Button.left, 1)
                time.sleep(1)
                mouse.position = (1025, 980)
                mouse.click(Button.left, 1)
                time.sleep(1)

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
                count += 1
            
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
        except Exception:
            continue
        print("done")
        time.sleep(999)
        driver.quit()

def ahrefs_year_passed(date_str):
    date_provided = datetime.strptime(date_str, "%d %b %Y")
    current_date = datetime.now()
    difference = current_date - date_provided
    has_been_a_year = difference.days >= 365
    return has_been_a_year

if (__name__ == '__main__'):

    options = Options()
    options.add_argument('--user-data-dir=/Users/dynas/AppData/Local/Google/Chrome/User Data/HelloWorld29')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    solver = RecaptchaSolver(driver=driver)

    mouse = Controller()

    ahrefs_listing_links = [
        "https://www.frontlinewildfire.com/",
        "https://afterthefireusa.org/",
        "https://www.fire.ca.gov/what-we-do/wildfire-prevention",
        "https://www.nfpa.org/Public-Education/Fire-causes-and-risks/Wildfire",
        "https://www.redcross.org/get-help/how-to-prepare-for-emergencies/types-of-emergencies/wildfire.html",
        "https://www.firewise.org",
        "https://www.fema.gov",
        "https://www.nwcg.gov",
        "https://www.fs.usda.gov/managing-land/fire",
        "https://www.iafc.org/topics-and-tools/resources/resource/wildland-fire-resources",
        "https://www.fireadapted.org",
        "https://www.nifc.gov",
        "https://www.usfa.fema.gov/prevention/outreach/wildfire.html",
        "https://www.caloes.ca.gov",
        "https://www.fire.ca.gov",
        "https://www.doi.gov/wildlandfire",
        "https://www.readyforwildfire.org"
    ]

    


    

    print(ahrefs_listing_links)

    gather_filtered_links =[]

    for ahrefs_link in ahrefs_listing_links:
        try:
            ahrefs_link = ahrefs_link.split("https://")[1]
            driver.get(f"https://app.ahrefs.com/v2-site-explorer/backlinks?anchorRules=&bestFilter=all&domainNameRules=&dr=0-24&followType=all&grouping=all&highlightChanges=30d&history=all&limit=50&mode=exact&offset=0&refPageAuthorRules=&refPageTitleRules=&refPageUrlRules=&sort=firstseen&sortDirection=desc&surroundingRules=&target=https%3A%2F%2F{ahrefs_link}&targetUrlRules=")
        except Exception:
            continue
        # One link per domain
        try:
            WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[1]/div[2]/main/div[1]/div[3]/div/div/div[1]/div/div/div/div[2]/div/div/div/button'))
            ).click()
            WebDriverWait(driver, 4).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'css-1odnfdc-menuItem') and contains(@class, 'css-1h7hs99-menuItemRightPadding')]"))
            )[1].click()
        except Exception:
            pass
        
        while (True):

            try:
                scroll_to_end_of_page()
                time.sleep(2)

                ahrefs_listing_analytics = WebDriverWait(driver, 4).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tbody[contains(@class, 'css-1lkq3hk-tbody')]/tr[contains(@class, 'css-5xi7tf-row')]"))
                )
                print(ahrefs_listing_analytics)
                for i in ahrefs_listing_analytics: 
                    try:
                        ahrefs_listing_date = i.find_element(By.XPATH, ".//td[contains(@class, 'css-1j01j1v-cell')]/div[contains(@class, 'css-9gw0ms-stack')]/div[contains(@class, 'css-1llwqnd-row')][1]/div/div/div[contains(@class, 'css-a5m6co-text')]").text
                        print(ahrefs_listing_date)
                        if not ahrefs_year_passed(ahrefs_listing_date): 
                            print("passed")
                            try:
                                filtered_link = WebDriverWait(i, 4).until(
                                    EC.presence_of_element_located((By.XPATH, ".(//tr[contains(@class, 'css-5xi7tf-row')]//a[contains(@href, 'https:')])"))
                                ).text
                            except Exception:
                                print("uh oh")
                            print("hai")
                            print(filtered_link)
                            if ("attorney" not in filtered_link and "law" not in filtered_link and "firm" not in filtered_link and "legal" not in filtered_link and "directory" not in filtered_link and "llc" not in filtered_link and ".au" not in filtered_link and ".ca" not in filtered_link and ".uk" not in filtered_link):
                                if ("resource" in filtered_link or "link" in filtered_link or "archive" in filtered_link):
                                    print(filtered_link)
                                    gather_filtered_links.append(filtered_link)
                        else: break
                    except Exception:
                        continue
                
                try:
                    current_button_index = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'css-9hzt1j-button') and contains(@class, 'css-4ct70d-buttonCurrent')]"))
                    ).text
                    if (int(current_button_index) + 1 >= 12):
                        break
                    WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located((By.XPATH, f"//button[@class='css-9hzt1j-button' and text()='{int(current_button_index) + 1}']"))
                    ).click()
                except Exception: break

            except Exception as e:
                continue


    try:
        check_and_send(gather_filtered_links) # gather_filtered_links
    except Exception:
        pass
    
    

        



