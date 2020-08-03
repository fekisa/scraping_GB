from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import json
import time

# опции
chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)

# БД
client = MongoClient('localhost', 27017)
db = client['mvideo']
collection = db.mvideo

# драйвер
driver.get('https://www.mvideo.ru/')

# ожидание
region = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "(//a[@class='next-btn sel-hits-button-next'])[2]")))

actions = ActionChains(driver)
actions.move_to_element(region).click().perform()

#времени не было посмотреть варианты покороче путей
#можно сделать и через while как в пятерочке
all_products = []
product_ids = []
page = 0
for i in range(4):
    block = driver.find_element_by_xpath('//*[contains(text(), "Хиты")]//parent::div//parent::div//parent::div')
    actions = ActionChains(driver)
    actions.move_to_element(block).perform()
    time.sleep(1)

    page_products = driver.find_elements_by_xpath("//*[contains(text(), 'Хиты')]//parent::div//parent::div//parent::div//li[@class='gallery-list-item height-ready']//div[@class='c-product-tile-picture__holder']/a")
    for product in page_products:
        attr = json.loads(product.get_attribute('data-product-info'))
        if attr['productId'] not in product_ids:
            product_ids.append(attr['productId'])
            all_products.append(attr)

    next_button = driver.find_element_by_xpath('//*[contains(text(), "Хиты")]//parent::div//parent::div//parent::div//a[contains(@class, "sel-hits-button-next")]')
    page += 1
    if page < 4:
        actions = ActionChains(driver)
        actions.move_to_element(next_button).click().perform()
        time.sleep(1)

driver.quit()

client = MongoClient('localhost', 27017)
db = client['products']
mvideo = db.mvideo

for element in all_products:
    mvideo.insert_one(element)

for user in mvideo.find({}):
    print(user)

