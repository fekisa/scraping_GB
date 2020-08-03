from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')


import time
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://5ka.ru/special_offers/')
pages = 0
while pages < 5:
    try:
        button = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,'special-offers__more-btn'))
        )
        # button = driver.find_element_by_class_name('special-offers__more-btn')
        button.click()
        pages +=1
        print(f'Обработана {pages} страница')
    except:
        print(f'Всего {pages} страниц')
        break
goods = driver.find_elements_by_xpath("//a[@class='sale-card']")
for good in goods:
    name = good.find_element_by_class_name('sale-card__title').text
    price = float(good.find_element_by_class_name('sale-card__price--new')
                  .find_element_by_xpath('span[1]')
                  .text)/100
    print(name, price)

