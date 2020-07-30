from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import ast
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo_db']
mvideo = db.mvideo

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

# Выбираем блок с каруселью хитов
# Как по другому выбрать я не понял. Их несколько каруселей с одинаковыми
# именами классов и прочими атрибутами.
# Карусель с хитами идет второй
hits_block = driver.find_elements_by_class_name('gallery-layout.sel-hits-block ')[1]
time.sleep(10)

# Выбираем кнопку для пролистывания из блока с хитами
next_button = hits_block.find_element_by_class_name('next-btn.sel-hits-button-next')

# Для определения количества кликов вытянем количество страниц
# (они отображаются в виде кликабельных полосок под каруселью)
hits_pages = hits_block.find_element_by_class_name('carousel-paging').find_elements_by_tag_name('a')

mvideo_hits = []

# В карусели 4 товара. При нажатии кнпки дальше, подгружаются еще 4 товара и
# встают в разметке выше предыдущих(при этом предыдущие не исчезают из кода страницы)
# Поэтому будем собирать все элементы из раздела хиты на старнице после каждого клика,
# но обрабатывать будем только 4 первых

for i in range(len(hits_pages)):
    products = hits_block.find_elements_by_class_name('sel-product-tile-title')
    for j in range(4):
        mvideo_hits_dict = {}
        link = products[j].get_attribute('href')
        info = products[j].get_attribute('data-product-info')
        # В info нам возвращается строка со словарем!
        # Чтобы ее перевести в нормальный словарь используем модуль ast
        info = ast.literal_eval(info)
        mvideo_hits_dict['productName'] = info['productName']
        mvideo_hits_dict['productPrice'] = info['productPriceLocal']
        mvideo_hits_dict['productLink'] = link
        mvideo_hits.append(mvideo_hits_dict)

    next_button.click()
    time.sleep(4)

mvideo.insert_many(mvideo_hits)
pprint(mvideo_hits)
driver.close()

