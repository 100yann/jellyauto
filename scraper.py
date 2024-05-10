from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time 
import os
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get("https://core.jellysmack.com/#/dashboard")
time.sleep(1)


def terminate_scrape(message: str):
    print(message)
    exit()


def login():
    login = driver.find_element(By.ID, "loginInput")
    if not login:
        terminate_scrape('Login field does not exist')

    login.send_keys(os.environ.get('jelly_email'))
    password = driver.find_element(By.ID, 'passwordInput')
    password.send_keys(os.environ.get('jelly_password'))

    sign_in = driver.find_element(By.CLASS_NAME, 'jsk-button')
    sign_in.click()
    time.sleep(2)


login()

production_tab = driver.find_element(By.XPATH, '/html/body/div[1]/div/nav/ul/li[3]/a')
if not production_tab:
    terminate_scrape('Navbar not found')

production_tab.click()
time.sleep(1)


in_progress_category = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/header/nav/ul/li[3]/h2/a')
in_progress_category.click()
time.sleep(8)

# add filters to filter the orders
filters = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/section/main/div/div/div[1]/section/div[1]/div[2]').click()

editors = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/section/main/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div/div[1]/input')
editors_list = ['Patriot Bytyqi', 'Hani Sinno', 'Betim Mehani', 'Stoyan Kolev']

for i in editors_list:
    editors.send_keys(i)
    editors.send_keys(Keys.ENTER)
    time.sleep(1)

# Scroll to bottom of page so all orders are loaded
orders_container = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/section/main/div/div/div[1]/div/div/div/div/div/table/tbody')
action = webdriver.ActionChains(driver)
for i in range(0, 3):
    action.move_to_element(orders_container)
    action.perform()
    time.sleep(2)



