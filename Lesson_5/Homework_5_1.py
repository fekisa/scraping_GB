from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

#опции
chrome_options = Options()
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('--headless')

#драйвер
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)

#БД
client = MongoClient('localhost', 27017)
db = client['mail_inbox_db']
collection = db.letters

# опять-таки решила воспользоваться мобильной версией
driver.get('https://m.mail.ru/login')

#время на загрузку
authorization = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Login")))

#авторизация
authorization.send_keys('study.ai_172@mail.ru')
authorization = driver.find_element_by_name('Password')
authorization.send_keys('NextPassword172')
authorization.send_keys(Keys.RETURN)

driver.get(driver.find_element_by_class_name('messageline__link').get_attribute('href'))  # первое письмо

#собираем все нужное и переходим на следующее в цикле
while True:
    letters_data = {}

    collection.insert_one(letters_data)

    from_whom = driver.find_element_by_xpath('//strong').text
    date_shipment = driver.find_element_by_class_name('readmsg__mail-date').text
    title = driver.find_element_by_class_name('readmsg__theme').text
    text = driver.find_element_by_id('readmsg__body').text.replace('\n', '').replace('  ', '')

    letters_data['from_whom'] = from_whom
    letters_data['date'] = date_shipment
    letters_data['theme'] = title
    letters_data['text'] = text

    try:
        next_page = driver.find_element_by_xpath("//div[@class='readmsg__horizontal-block__right-block']"
                                                 "/a[@class='readmsg__text-link']").get_attribute('href')
    except Exception:
        break
    driver.get(next_page)

driver.close()

for i in collection.find({}):
    print(i)