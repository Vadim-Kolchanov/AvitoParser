"""
Creating by Vadim Kolchanov, 2021 year
"""
import parser_page
from collections import namedtuple
import time

import csv
import bs4
import requests
import cfscrape
import urllib.parse

dataBlock = namedtuple('Block',
                       'indexCity, lat, lon, wall, rooms,'
                       'level, totalLevel, totalArea, livingArea, kitchenArea,'
                       'season, year, price, url')


class Block(dataBlock):

    def __str__(self):
        return f'{self.indexCity};{self.lat};{self.lon};{self.wall};{self.rooms};{self.level};{self.totalLevel};{self.totalArea};{self.livingArea};{self.kitchenArea};{self.season};{self.year};{self.price};{self.url}'


class AvitoParser:

    def __init__(self, urlCity: str, indexCity: int = None, city: str = None):
        self.pathURLs = './DataURLsCity/' + 'URLs-' + city
        self.pathParsedPage = './DataParsedPageCity/' + 'Apartments-' + city
        self.city = city
        self.indexCity = indexCity
        self.urlCity = urlCity

        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        self.site = cfscrape.create_scraper(sess=self.session)

    def getProxy(self):
        proxy = ["140.238.80.23:3128", "78.109.196.162:3128", "89.74.114.10:3128", "62.23.15.92:3128"]

    # Получаем текст страницы по url адресу
    def getPage(self, page: int = None, url: str = None):
        params = {}
        if page and page > 1:
            params['p'] = page

        r = self.site.get(url, params=params)
        if not r.status_code == 200:
            print("Ошибка с подключением на сайт, код ошибки:", r.status_code)
            time.sleep(60)
            return self.getPage(page=page, url=url)

        return r.text

    # Преобразуем html страницу при помощи супа
    def getSoupPage(self, url: str = None, page: int = None):
        # Получаем html текст страницы
        text = self.getPage(url=url, page=page)
        if not text:
            print("Ошибка в получении разметки страницы")
            return

        # Преобразуем html-text при помощи супа
        soup = bs4.BeautifulSoup(text, 'lxml')
        return soup

    # Получаем значение последней страницы на сайте
    def getPaginationLimit(self):
        soup = self.getSoupPage(url=self.urlCity)

        # Выбираем блок со страницами и ищём последнюю
        lastPage = soup.select('a.pagination-page')[-1]

        href = lastPage.get('href')
        if not href:
            return 1

        # Парсим параметр "р"
        r = urllib.parse.urlparse(href)
        params = urllib.parse.parse_qs(r.query)
        return int(params['p'][0])

    # Парсим блок, достаём ссылку на квартиру
    def parseURL(self, item):
        # Выбрать блок со ссылкой
        urlBlock = item.select_one('div.iva-item-titleStep-2bjuh a')
        if not urlBlock:
            return

        href = urlBlock.get('href')
        if href:
            url = 'https://www.avito.ru' + href
            return url

        return None

    # Парсим страницу с квартирой
    def parsePage(self, url: str = None):
        soup = self.getSoupPage(url=url)

        # Парсим блок с параметрами квартиры
        # Широта и Долгота
        lat, lon = parser_page.address(soup)
        # Тип стен, кол-во комнат, этаж, этажность, общая площадь, жилая площадь, площадь кухни
        wall, rooms, level, totalLevel, totalArea, livingArea, kitchenArea = parser_page.param(soup)
        # Сезон, год
        season, year = parser_page.date(soup)
        # Цена за квартиру
        price = parser_page.price(soup)

        return Block(
            indexCity=self.indexCity,
            lat=lat,
            lon=lon,
            wall=wall,
            rooms=rooms,
            level=level,
            totalLevel=totalLevel,
            totalArea=totalArea,
            livingArea=livingArea,
            kitchenArea=kitchenArea,
            season=season,
            year=year,
            price=price,
            url=url,
        )

    # Получаем список квартир
    def getBlock(self, page: int = None):
        soup = self.getSoupPage(url=self.urlCity, page=page)

        # Выбираем блок с квартирами
        container = soup.select_one('div.items-items-38oUm')
        if not container:
            print("Ошибка с получением блоков с квартирами")
            return

        # Список имеющихся ссылок на квартиры
        listURL = self.readURL()
        # Записываем ссылки на квартиры
        with open(self.pathURLs + '.csv', 'a') as csvfile:
            # Парсим каждый предмет в блоке
            for item in container:
                url = self.parseURL(item=item)
                if url and not (url in listURL):
                    csvfile.writelines(url + "\n")

            print("записано")
            csvfile.close()

    # Парсим все указанные страницы
    def parsePageAll(self, limit: int = None):
        if not limit:
            limit = self.getPaginationLimit()

        print("Всего страниц:", limit)
        for i in range(1, limit + 1):
            print("Текущая страница:", i)
            self.getBlock(page=i)
            time.sleep(10)

    # Читаем все имеющиеся ссылки из файла
    def readURL(self):
        listURL = []
        with open(self.pathURLs + '.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                listURL += row
            csvfile.close()
        return listURL

    # Записываем парсинг квартиры в файл
    def writeParsePage(self):
        # Получаем сылки которые надо запарсить
        listURL = self.readURL()

        # Читаем ссылки которые уже были запарсены
        listParsePageURL = self.readParsePageURL()

        # Удаляем все ссылки из списка, которые уже были запарсены
        for link in listParsePageURL:
            listURL.remove(link)

        if not listURL:
            print("Ссылок в файле для парсинга нет")
            return

        print("Всего ссылок в очереди на парсинг:", len(listURL))
        with open(self.pathParsedPage + '.csv', 'a') as csvfile:
            for link in listURL:
                block = self.parsePage(url=link)
                if block:
                    print(block)
                    csvfile.writelines(block.__str__() + "\n")
                csvfile.flush()
                time.sleep(5)

            csvfile.close()

    # Читаем ссылки из файла которые уже запарсены
    def readParsePageURL(self):
        listParsePageURL = []
        csv.register_dialect(";", delimiter=';')
        with open(self.pathParsedPage + '.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, ";")
            for row in reader:
                listParsePageURL += row[-1:]
            csvfile.close()

        return listParsePageURL[1:]

    # Инициализация файла с заголовками
    def filesInit(self):
        with open(self.pathURLs + '.csv', 'w') as csvfile:
            csvfile.close()

        columns = ["Индекс город", "Широта", "Долгота", "Тип стен", "Количество комнат", "Этаж", "Этажность",
                   "Общая площадь", "Жилая площадь", "Площадь кухни", "Сезон", "Год", "Стоимость квартиры", "URL"]
        csv.register_dialect(";", delimiter=';')
        with open(self.pathParsedPage + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, ";")
            writer.writerow(columns)

            csvfile.close()
