import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from pynput.mouse import Button, Controller
from selenium.common.exceptions import NoAlertPresentException
import time, pyautogui, random, re, csv
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

def get_urls(min_da, max_da):
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
                print(f"Domain Authority: {da_number} Link: {listing_link}")
                urls.append(listing_link)
        except Exception as e:
            print(e)
            continue
    return urls

if (__name__ == '__main__'):
    options = Options()
    options.add_argument('--user-data-dir=/Users/dynas/AppData/Local/Google/Chrome/User Data/HelloWorld29')
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    solver = RecaptchaSolver(driver=driver)

    search_queries = [
    "bodybuilding coach",  # Focus on building muscle mass and strength
    "nutrition coach",  # Focus on developing healthy eating habits and meal planning
    "weight loss coach",  # Focus on helping individuals lose weight through diet and exercise
    "functional fitness trainer",  # Focus on improving overall strength and mobility for everyday tasks
    "sports performance coach",  # Focus on enhancing athletic performance in specific sports
    "yoga instructor",  # Focus on promoting physical and mental well-being through yoga practice
    "pilates instructor",  # Focus on improving flexibility, strength, and endurance through pilates exercises
    "HIIT coach",  # Focus on high-intensity interval training for cardiovascular health and fat loss
    "boxing coach",  # Focus on teaching boxing techniques for fitness and self-defense
    "circuit training coach",  # Focus on full-body workouts incorporating various exercises in a circuit format
    "mindfulness coach",  # Focus on promoting mindfulness and stress reduction techniques
    "stretching coach",  # Focus on improving flexibility and preventing injuries through stretching routines
    "bootcamp instructor",  # Focus on intense group workouts combining cardio, strength, and endurance exercises
    "barre instructor",  # Focus on low-impact exercises inspired by ballet, yoga, and pilates
    "dance fitness instructor",  # Focus on choreographed dance routines for cardiovascular fitness and fun
    "triathlon coach",  # Focus on training individuals for triathlon competitions, including swimming, cycling, and running
    "marathon coach",  # Focus on preparing individuals for long-distance running events such as marathons
    "cycling coach",  # Focus on improving cycling performance and technique for races or leisure
    "swimming coach",  # Focus on teaching swimming skills and improving stroke technique
    "strength and conditioning coach",  # Focus on developing strength, power, and endurance for athletes
    "mobility coach",  # Focus on improving joint mobility and flexibility for enhanced movement
    "kettlebell instructor",  # Focus on incorporating kettlebell exercises for strength and conditioning
    "TRX trainer",  # Focus on suspension training using TRX straps for a full-body workout
    "rowing coach",  # Focus on improving rowing technique and fitness for rowing competitions or general fitness
    "parkour instructor",  # Focus on teaching parkour techniques for movement efficiency and agility
    "bodyweight training coach",  # Focus on using bodyweight exercises for strength and conditioning
    "group fitness instructor",  # Focus on leading group exercise classes in various formats such as cardio, strength, or dance
    "functional movement coach",  # Focus on improving movement patterns for everyday activities and sports performance
    "rehabilitation coach",  # Focus on designing exercise programs to aid in injury recovery and prevention
    "posture coach",  # Focus on correcting posture imbalances and promoting proper alignment
    "agility coach",  # Focus on improving agility, coordination, and reaction time for athletes
    "aerial yoga instructor",  # Focus on yoga practice using suspended hammocks for added challenge and fun
    "meditation instructor",  # Focus on teaching meditation techniques for stress reduction and mental clarity
    "kayaking coach",  # Focus on teaching kayaking skills and techniques for recreational or competitive purposes
    "virtual fitness coach",  # Focus on providing online coaching and workout programs for remote clients
    "post-natal fitness coach",  # Focus on safe and effective exercises for postpartum women to regain strength and fitness
    "senior fitness coach",  # Focus on tailored exercise programs for older adults to improve mobility and independence
    "adaptive fitness coach",  # Focus on modifying exercises for individuals with disabilities or special needs
    "youth fitness coach",  # Focus on promoting physical activity and healthy habits for children and teenagers
    "Bikini Coach"
]


    # Change the mode to 'a' for appending data to the existing CSV file.
    with open("email_out/emails.csv", 'a', newline="") as f:
        writer = csv.writer(f)

        for query in search_queries:
            driver.get(f"https://www.google.com/search?q={query}")
            try:
                
                recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
                solver.click_recaptcha_v2(iframe=recaptcha_iframe)
            except Exception:
                pass
            scroll_down()
            try:
                
                urls = get_urls(15, 61)

                for url in urls:
                    try:
                        driver.get(url)
                        time.sleep(0.5)
                        domain = url.split("//")[-1].split("/")[0]
                        regex = r"[a-zA-Z0-9._%+-]+@" + re.escape(domain)
                        html = driver.page_source
                        emails = list(set(re.findall(regex, html)))
                        print(emails)
                        if emails:
                            # Open the CSV file in append mode here within the loop
                            with open("email_out/emails.csv", 'a', newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow(emails)
                    except Exception as e:
                        print(e)
                        continue
            except Exception:
                print(e)
                continue

    driver.quit()
