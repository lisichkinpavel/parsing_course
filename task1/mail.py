# Собирать письма буду по-одному.Скролл так и не удалось нормально реализовать
# Заходим в первое письмо и дальше переходим к другому письму
# по кнопке.
# На последнем письме кновка станем некликабельной и ее класс станет другим,
# получим исключение, обработав которое выйдем из цикла и завершим работу.

from pprint import pprint
import re
from datetime import date
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['mails_db']
mails = db.mails

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mail.ru/')

login = driver.find_element_by_id('mailbox:login')
login.send_keys('study.ai_172@mail.ru')
login.send_keys(Keys.RETURN)

password = driver.find_element_by_id('mailbox:password')
password.send_keys('NextPassword172')
password.send_keys(Keys.RETURN)
time.sleep(5)

first_leter = driver.find_element_by_class_name('llc.js-tooltip-direction_letter-bottom.js-letter-list-item.llc_normal')
first_leter.send_keys(Keys.RETURN)
time.sleep(2)

# функция для перевода даты в нужный формат
def date_convertor(mail_date_time):
    month_dict = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }
    if mail_date_time.find('Сегодня') == -1:
        date_string = re.findall(r'(\d+) (\w+)( \w+)?', mail_date_time)[0]
        month = month_dict[date_string[1]]
        if not date_string[-1]:
            year = date.today().year
            return f'{date_string[0]}/{month}/{year}'
        else:
            year = date_string[-1].replace(' ', '')
            return f'{date_string[0]}/{month}/{year}'
    else:
        return date.today().strftime("%d/%m/%y")


letters = []

while True:
    try:
        letters_dict = {}
        letter_from = driver.find_element_by_class_name('letter-contact')
        letters_dict['author'] = letter_from.text
        letters_dict['author_mail'] = letter_from.get_attribute('title')
        date_time = driver.find_element_by_class_name('letter__date').text
        letters_dict['date'] = date_convertor(date_time)
        letters_dict['body'] = driver.find_element_by_class_name('letter__body').text
        letters.append(letters_dict)

        next_button = driver.find_element_by_class_name('button2.button2_has-ico.button2_arrow-down.button2_pure'
                                                        '.button2_short.button2_ico-text-top.button2_hover-support.js'
                                                        '-shortcut')
        next_button.click()
        time.sleep(2)
    except NoSuchElementException:
        break

mails.insert_many(letters)
pprint(letters)
pprint(len(letters))
