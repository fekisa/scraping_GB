from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
driver = webdriver.Chrome()

driver.get('https://geekbrains.ru/login')

username = driver.find_element_by_id('user_email')
username.send_keys('study.ai_172@mail.ru')

password = driver.find_element_by_id('user_password')
password.send_keys('Password172')

password.send_keys(Keys.RETURN)

time.sleep(1)
user_profile = driver.find_element_by_class_name('avatar')
driver.get(user_profile.get_attribute('href'))

edit_profile = driver.find_element_by_class_name('text-sm')
driver.get(edit_profile.get_attribute('href'))

gender = driver.find_element_by_name('user[gender]')
# options = gender.find_elements_by_tag_name('option')


# for option in options:
#     if option.text == 'Женский':
#         option.click()

select = Select(gender)
select.select_by_value('1')

gender.submit()

driver.back()
driver.forward()
driver.refresh()

# driver.close()

