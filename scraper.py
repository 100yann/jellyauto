from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time 
import os
from bs4 import BeautifulSoup

def scrape_data():
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


    # Scroll to bottom of page so all orders are loaded
    def scroll_to_bottom(element):
        action = webdriver.ActionChains(driver)
        for i in range(0, 3):
            action.move_to_element(element)
            action.perform()
            time.sleep(2)


    def get_order_data(table_rows):
        for row in table_rows:
            row_data = row.find_all('td')
            editor_initials = row_data[13].find('span').get_text().strip()

            # work on data only if editor matches the editors in the editors_list
            if editor_initials in editors_list:
                editor = editors_list[editor_initials]
                video_name = row_data[1].find('span', class_='text-sm')['data-original-title'].strip()
                video_status = row_data[5].find('span').get_text().strip()

                if editor not in final_data:
                    final_data[editor] = {}

                if "AB" in video_status or 'In Small re-edit' in video_status:
                    video_status = "AB Test"
                elif "Ongoing review" in video_status or "Ongoing re-edit" in video_status:
                    video_status = "review/re-edit"

                if not final_data[editor].get(video_status, 0):
                    final_data[editor][video_status] = {}

                final_data[editor][video_status]['num'] = final_data[editor][video_status].get('num', 0) + 1
                final_data[editor][video_status].setdefault('videos', []).append(video_name)
                final_data[editor]['total_videos'] = final_data[editor].get('total_videos', {})
                final_data[editor]['total_videos']['num'] = final_data[editor]['total_videos'].get('num', 0) + 1
    login()

    production_tab = driver.find_element(By.XPATH, '/html/body/div[1]/div/nav/ul/li[3]/a')
    if not production_tab:
        terminate_scrape('Navbar not found')

    production_tab.click()
    time.sleep(1)

    # get orders in the in progress page
    in_progress_category = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/header/nav/ul/li[3]/h2/a')
    in_progress_category.click()
    time.sleep(8)

    # add filters to filter the orders
    filters = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/section/main/div/div/div[1]/section/div[1]/div[2]').click()

    editors = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/section/main/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div/div[1]/input')
    editors_list = {'P B': 'Patriot Bytyqi', 'H S': 'Hani Sinno', 'B': 'Betim Mehani', 'S K': 'Stoyan Kolev'}

    for val in editors_list.values():
        editors.send_keys(val)
        editors.send_keys(Keys.ENTER)
        time.sleep(1)

    # Scroll to bottom of page so all orders are loaded
    orders_container = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/section/main/div/div/div[1]/div/div/div/div/div/table/tbody')
    scroll_to_bottom(orders_container)

    orders_html = orders_container.get_attribute("outerHTML")
    soup = BeautifulSoup(orders_html, 'html.parser')
    table_rows = soup.find_all('tr')


    final_data = {}
    if table_rows:
        get_order_data(table_rows)
    else:
        terminate_scrape('No orders found in progress')


    # get orders on the ab tests page
    ab_test_page = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/header/nav/ul/li[4]/h2/a')
    ab_test_page.click()
    time.sleep(6)

    orders_container = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section/section/main/div/div/div[1]/div/div/div/div/div/table/tbody')
    scroll_to_bottom(orders_container)

    orders_html = orders_container.get_attribute("outerHTML")
    soup = BeautifulSoup(orders_html, 'html.parser')
    table_rows = soup.find_all('tr')

    if table_rows:
        get_order_data(table_rows)
    else:
        terminate_scrape('No orders found in ab test')

    necessary_columns = ['Ready to edit', 'Ongoing edit', 'review/re-edit', 'AB Test']
    for editor in final_data:
        for col in necessary_columns:
            if col not in final_data[editor]:
                final_data[editor][col] = {'num': 0}

    return final_data

