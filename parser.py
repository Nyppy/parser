import requests
import codecs # библиотека для ткрытия файлов
from bs4 import BeautifulSoup # библиотека для анализа html страниц
import os # библиотека для работы с ОС
import time # работа с часами 
from selenium import webdriver # библиотека обеспечивает взаимодействие с Geckodriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class parser(object):
    """docstring for parser"""
    def __init__(self):
        text_site = ''
        url_image = []

        self.text_site = text_site
        self.url_image = url_image


    def search_image(self, image_name):
        '''Поиск и сохранение страницы с картинками'''

        options = FirefoxOptions() # инициализация Гекодрайвера
        options.add_argument("--headless") # настройки для запуска без открытия браузера

        gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
        binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
        # driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko+'.exe') # режим с открытием браузера
        driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko+'.exe', options=options)

        driver.get('https://yandex.ru/images') # открывает ссылку в браузере
        time.sleep(5) # ожидание 5 сек
        element = driver.find_element_by_class_name("input__control") # поиск окна для ввода текста 
        g_req = image_name # ввод названия картинки
        element.send_keys(g_req, Keys.RETURN) # нажатие Enter
        
        time.sleep(5) # ожидание 5 сек
    
        # цикл для прокрутки страницы вниз. Для отоброжения большего количества картинк
        for i in range(1500):
            driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN) 
            if i%20==0:
                time.sleep(1.5)

        time.sleep(10) # ожидание 10 сек
        
        str = driver.page_source # сохранение страницы

        # запись страницы в файл
        with open(r'C:\Users\atlas\Desktop\hakaton\parser\test.html', 'wb') as output_file:
            output_file.write(str.encode('utf-8'))
        
        driver.quit() # закрытие браузера
 
    def read_file_image(self):
        '''Чтение файла и поиск ссылок на картинки. Запись ссылок в переменную'''

        with codecs.open(r'C:\Users\atlas\Desktop\hakaton\parser\test.html', "r", "utf_8_sig" ) as file_obj:
            for i in file_obj:
                self.text_site += i

        soup = BeautifulSoup(self.text_site) # инициализация библиотеки по анализу html страниц

        # поиск класса 'serp-item__thumb justifier__thumb' в теге 'img'
        images_text = soup.find_all('img', {'class': 'serp-item__thumb justifier__thumb'}) 
        for i in images_text:
            # поиск ссылок на картинки и запись в переменную
            self.url_image.append('http:' + i['src'])

    def download_image(self, length=100):
        '''Скачивание картинок. Количество скачиваний по умолчанию 100 картинок'''
        for i in range(length):
            print(self.url_image[i])
            r = requests.get(self.url_image[i])
            path = 'C:/Users/atlas/Desktop/hakaton/parser/image/img'+ str(i) +'.jpg'

            with open(path, 'wb') as output_file:
                output_file.write(r.content)


pars = parser()
pars.search_image('Свалка')
pars.read_file_image()
pars.download_image()