from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from datetime import datetime
from pynput.mouse import Button, Controller
import time, pyautogui, random


chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-geolocation")
chrome_options.add_argument("--remote-allow-origins=*")
chrome_options.add_argument('user-data-dir=/Users/williamzhao/Library/Application Support/Google/Chrome/')
chrome_options.add_argument("--profile-directory=Profile 1")
# chrome_options.add_argument("--start-maximized")
service = Service(executable_path='/opt/homebrew/bin/chromedriver')

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.execute_script("document.body.style.zoom='80%'")

wait = WebDriverWait(driver, 10)


d={"Nicholas":1, "Katrina":1, "Akemi":1, "Luke":1, "Dylan":1, "Michael":1,"Congxing":1,"PJ":1,"Peter":1,"Brian":1,"Andrew":1,"Anita":1,
   "Isaiah":1,"Bastian":1,"Alice":1,"Jon":1,"Rena":1,"Iman":1,"Justin":1,"Daniel":1,"Kate":1,"Tracy":1,"Tameca":1,"Penelope":1,"Claribel":1,
   "Charlie":1,"Eric":1,"Risa":1,"Jack":1,"Sam":1,"Allison":1,"Bretton":1,"Nick":1,"Brian":1,"Jace":1, "Mark":1,"Lauren":1,"Todd":1,"Alec":1,
   "Alexanderia":1,"Shane":1,"Jen":1,"Peiyuan":1,"Bimarsh":1,"Tony":1,"Joel":1,"Fawaz":1,"Charles":1,"Nicholas":1,"Steven":1,"Briggs":1,"Ashley":1,
   "Ian":1,"Katherine":1,"Marchem":1}


q=[]
curr_page = 0

while curr_page < int(100):
    curr_page += 1
    driver.get(f"https://ucsc.joinhandshake.com/stu/postings?page={curr_page}&per_page=150&sort_direction=desc&sort_column=default&job.messageable_job_user_profile=true&job.salary_types%5B%5D=1")
    try:
        all_listing = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"style__card-content___wF9WK")]')))
        for listing in all_listing:
            try:
                title = listing.find_element(By.XPATH, "//div[contains(@class, 'style__title___cxDSR')]").text
                name = listing.find_element(By.XPATH, "//div[contains(@class, 'style__name___tkPbe')]").text
                first_name = name.split(" ")[0]

                print(f"title {title} and name {name}")
                
                message = f"""
                Hi my name is {first_name}
                I recently noticed your profile and was intrigued by your business.
                As someone who's passionate about helping businesses shine online, I couldn't help but think about the untapped potential of your website. I specialize in SEO, turning websites into revenue-generating assets by connecting you with the right audience.
                I'd love to chat about your goals and see if there are some straightforward ways to enhance your site's performance in Google.
                Would you be up for a quick call to show you what I’ve done for other businesses?
                Looking forward to potentially chatting with you!
                Best, {name}
                """

                if first_name not in d and any(word in title for word in ["Owner", "CEO", "COO", "Director", "Manager", "Marketing", "Lead", "CMO"]):
                    d[name] = 1
                    listing.click()
                    
                    send_message_button = WebDriverWait(listing, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'style__action-button___') and contains(., 'Send a message')]")))
                    send_message_button.click()

                    text_area = wait.until(EC.presence_of_element_located((By.XPATH, "span[contenteditable='true'][id='message']")))
                    text_area.clear()
                    text_area.send_keys(message)

                    # time.sleep(2)
                    WebDriverWait(listing, 10).until(EC.presence_of_element_located(By.XPATH, "//button[span[text()='Send message']]"))
                
            except NoSuchElementException:
                print("Element not found, continuing to next listing")

    except Exception as e:
        print(f"Exception occurred: {e}")
        break

print(q)




time.sleep(9999)