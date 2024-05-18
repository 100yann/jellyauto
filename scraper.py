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

EDITORS = {'P B': 'Patriot Bytyqi', 'H S': 'Hani Sinno', 'B': 'Betim Mehani', 'S K': 'Stoyan Kolev'}


def login():
    login = driver.find_element(By.ID, "loginInput")
    login.send_keys(os.environ.get('jelly_email'))
    password = driver.find_element(By.ID, 'passwordInput')
    password.send_keys(os.environ.get('jelly_password'))

    sign_in = driver.find_element(By.CLASS_NAME, 'jsk-button')
    sign_in.click()
    time.sleep(2)


def apply_filters():
    filters = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/section/main/div/div/div[1]/section/div[1]/div[2]').click()
    editors = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/section/main/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div/div[1]/input')

    for val in EDITORS.values():
        editors.send_keys(val)
        time.sleep(1)
        editors.send_keys(Keys.ENTER)
        time.sleep(1)


def scroll_to_bottom(element, amount):
    action = webdriver.ActionChains(driver)
    for i in range(0, amount):
        action.move_to_element(element)
        action.perform()
        time.sleep(3)


def scrape_data():
    driver.get("https://core.jellysmack.com/#/dashboard")
    time.sleep(1)


    # Scroll to bottom of page so all orders are load


    def get_order_data(table_rows, page=None):
        for row in table_rows:
            row_data = row.find_all('td')
            editor_initials = row_data[13].find('span').get_text().strip()

            # work on data only if editor matches the editors in the EDITORS
            if editor_initials in EDITORS:
                editor = EDITORS[editor_initials]
                video_name = row_data[1].find('span', class_='text-sm')['data-original-title'].strip()
                video_status = row_data[5].find('span').get_text().strip()
                video_url = row_data[1].select_one('div > a')['href']
                if page == 'stock' or 'delivered':
                    ...
                
                else:
                    if "AB" in video_status or 'In Small re-edit' in video_status:
                        video_status = "AB Test"
                    elif "Ongoing review" in video_status or "Ongoing re-edit" in video_status:
                        video_status = "review/re-edit"

                    final_data[editor][video_status]['num'] += 1
                    final_data[editor][video_status]['videos'][video_name] = f'https://core.jellysmack.com/{video_url}'
                    final_data[editor]['total_videos'] = final_data[editor].get('total_videos', {})
                    final_data[editor]['total_videos']['num'] = final_data[editor]['total_videos'].get('num', 0) + 1


    login()

    production_tab = driver.find_element(By.XPATH, '/html/body/div[1]/div/nav/ul/li[3]/a')
    production_tab.click()
    time.sleep(1)

    # get orders in the in progress page
    in_progress_category = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/header/nav/ul/li[3]/h2/a')
    in_progress_category.click()
    time.sleep(8)

    # add filters to filter the orders
    apply_filters()

    # Scroll to bottom of page so all orders are loaded
    orders_container = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/section/main/div/div/div[1]/div/div/div/div/div/table/tbody')
    scroll_to_bottom(orders_container, 3)

    orders_html = orders_container.get_attribute("outerHTML")
    soup = BeautifulSoup(orders_html, 'html.parser')
    table_rows = soup.find_all('tr')

    VIDEO_STATUSES = ['Ready to edit', 'Ongoing edit', 'review/re-edit', 'AB Test']
    EDITORS = ['Hani Sinno', 'Patriot Bytyqi', 'Betim Mehani', 'Stoyan Kolev']

    final_data = {editor: {status: {'num': 0, 'videos': {}} for status in VIDEO_STATUSES} for editor in EDITORS}

    if table_rows:
        get_order_data(table_rows)


    # get orders on the ab tests page
    ab_test_page = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/header/nav/ul/li[4]/h2/a')
    ab_test_page.click()
    time.sleep(6)

    orders_container = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/section/main/div/div/div[1]/div/div/div/div/div/table/tbody')
    scroll_to_bottom(orders_container, 3)

    orders_html = orders_container.get_attribute("outerHTML")
    soup = BeautifulSoup(orders_html, 'html.parser')
    table_rows = soup.find_all('tr')

    if table_rows:
        get_order_data(table_rows)


    orders_html = orders_container.get_attribute("outerHTML")
    soup = BeautifulSoup(orders_html, 'html.parser')
    table_rows = soup.find_all('tr')

    if table_rows:
        get_order_data(table_rows, page='stock')


    return final_data



