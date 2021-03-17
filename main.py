"""
Creating by Vadim Kolchanov, 2021 year
"""
import parser_avito

URL_Ekaterinburg = 'https://www.avito.ru/ekaterinburg/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Perm = 'https://www.avito.ru/perm/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Penza = 'https://www.avito.ru/penza/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Kazan = 'https://www.avito.ru/kazan/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Novosibirsk = 'https://www.avito.ru/novosibirsk/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Chelyabinsk = 'https://www.avito.ru/chelyabinsk/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Moskva = 'https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Sankt_peterburg = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Nizhniy_novgorod = 'https://www.avito.ru/nizhniy_novgorod/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Pyatigorsk = 'https://www.avito.ru/pyatigorsk/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Rostov_na_donu = 'https://www.avito.ru/rostov-na-donu/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Habarovsk = 'https://www.avito.ru/habarovsk/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Krasnodar = 'https://www.avito.ru/krasnodar/kvartiry/prodam-ASgBAgICAUSSA8YQ'

URL_Saratov = 'https://www.avito.ru/saratov/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Tyumen = 'https://www.avito.ru/tyumen/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Tolyatti = 'https://www.avito.ru/tolyatti/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Izhevsk = 'https://www.avito.ru/izhevsk/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Barnaul = 'https://www.avito.ru/barnaul/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Ulyanovsk = 'https://www.avito.ru/ulyanovsk/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Irkutsk = 'https://www.avito.ru/irkutsk/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Yaroslavl = 'https://www.avito.ru/yaroslavl/kvartiry/prodam-ASgBAgICAUSSA8YQ'
URL_Vladivostok = 'https://www.avito.ru/vladivostok/kvartiry/prodam-ASgBAgICAUSSA8YQ'

'''
1 шаг.
Создаём экземпляр класса AvitoParser из файла parser_avito.py
Конструктор класса __init__(self, urlCity: str = None, indexCity: int = None, city: str = None):
- urlCity: ссылка на город, в котором нужно запарсить квартиры
- indexCity: индекс города (выбирается любое число, нужен для кодировки городов)
- city: название города
'''
# 1 шаг
# avito = parser_avito.AvitoParser(urlCity=URL_Ekaterinburg, indexCity=1, city="Ekaterinburg")
# avito = parser_avito.AvitoParser(urlCity=URL_Perm, indexCity=2, city="Perm")
# avito = parser_avito.AvitoParser(urlCity=URL_Kazan, indexCity=3, city="Kazan")
# avito = parser_avito.AvitoParser(urlCity=URL_Novosibirsk, indexCity=4, city="Novosibirsk")
# avito = parser_avito.AvitoParser(urlCity=URL_Chelyabinsk, indexCity=5, city="Chelyabinsk")
#avito = parser_avito.AvitoParser(urlCity=URL_Moskva, indexCity=6, city="Moskva")
#avito = parser_avito.AvitoParser(urlCity=URL_Sankt_peterburg, indexCity=7, city="Sankt_peterburg")
#avito = parser_avito.AvitoParser(urlCity=URL_Nizhniy_novgorod, indexCity=8, city="Nizhniy_novgorod")
#avito = parser_avito.AvitoParser(urlCity=URL_Pyatigorsk, indexCity=9, city="Pyatigorsk")
#avito = parser_avito.AvitoParser(urlCity=URL_Rostov_na_donu, indexCity=10, city="Rostov_na_donu")
#avito = parser_avito.AvitoParser(urlCity=URL_Habarovsk, indexCity=11, city="Habarovsk")
#avito = parser_avito.AvitoParser(urlCity=URL_Penza, indexCity=12, city="Penza")
#avito = parser_avito.AvitoParser(urlCity=URL_Krasnodar, indexCity=13, city="Krasnodar")
#avito = parser_avito.AvitoParser(urlCity=URL_Saratov, indexCity=14, city="Saratov")

avito = parser_avito.AvitoParser(urlCity=URL_Tyumen, indexCity=15, city="Tyumen")

#avito = parser_avito.AvitoParser(urlCity=URL_Tolyatti, indexCity=16, city="Tolyatti")
#avito = parser_avito.AvitoParser(urlCity=URL_Izhevsk, indexCity=17, city="Izhevsk")
#avito = parser_avito.AvitoParser(urlCity=URL_Barnaul, indexCity=18, city="Barnaul")
#avito = parser_avito.AvitoParser(urlCity=URL_Irkutsk, indexCity=19, city="Irkutsk")
#avito = parser_avito.AvitoParser(urlCity=URL_Yaroslavl, indexCity=20, city="Yaroslavl")
#avito = parser_avito.AvitoParser(urlCity=URL_Vladivostok, indexCity=21, city="Vladivostok")



'''
2 шаг.
При помощи метода filesInit() по этим путям:
- self.pathURLs
- self.pathParsedPage
создаются два файла. В одном будут запарсенные ссылки на квартиры, в другом запарсенные квартиры. 
'''
# 2 шаг
#avito.filesInit()

'''
3 шаг.
При помощи метода parsePageAll(self, limit: int = None) парсятся ссылки на квартиры.
Аргументы метода:
- limit: указывается лимит на кол-во парсинга страниц, если не указано, 
         то при помощи метода getPaginationLimit() 
         найдется максимальное число доступных страниц
'''
# 3 шаг
#avito.parsePageAll()

'''
4 шаг.
При помощи метода writeParsePage() парсятся параметры квартир
'''
# 4 шаг
avito.writeParsePage()

