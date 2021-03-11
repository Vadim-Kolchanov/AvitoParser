"""
Creating by Vadim Kolchanov, 2021 year
"""
import datetime
import bs4


def address(soup):
    addressBlock = soup.select_one("div.b-search-map.expanded.item-map-wrapper.js-item-map-wrapper")
    if addressBlock:
        lat = addressBlock['data-map-lat']
        lon = addressBlock['data-map-lon']
        return [lat, lon]
    else:
        return [None, None]


def param(soup):
    # wall0, rooms1, level2, totalLevel3, totalArea4, livingArea5, kitchenArea6
    param = [None, None, None, None, None, None, None]
    paramBlock = soup.select('li.item-params-list-item')

    if not paramBlock:
        print("Ошибка в параметрах")
        return param

    for item in paramBlock:
        nameParam = item.get_text().split(sep=":")[0].strip()
        valueParam = item.get_text().split(sep=":")[1].strip()

        if nameParam == "Тип дома":
            param[0] = parseWall(valueParam)
            continue

        if nameParam == "Количество комнат":
            param[1] = parseCountRooms(valueParam)
            continue

        if nameParam == "Этаж":
            splitter = valueParam.split(sep=" ")
            param[2] = splitter[0]
            param[3] = splitter[2]
            continue

        if nameParam == "Общая площадь":
            param[4] = "".join(list(valueParam)[:-3])
            continue

        if nameParam == "Жилая площадь":
            param[5] = "".join(list(valueParam)[:-3])
            continue

        if nameParam == "Площадь кухни":
            param[6] = "".join(list(valueParam)[:-3])

    return param


def price(soup):
    priceBlock = soup.select_one('span.js-item-price')

    if not priceBlock:
        print("Ошибка с ценой")
        return

    return int(priceBlock['content']) / 1_000_000.0


def date(soup):
    dateBlock = soup.select_one('div.title-info-metadata-item-redesign')

    if not dateBlock:
        print("Ошибка с датами")
        return [None, None]

    dateText = dateBlock.get_text().strip()
    monthYear = parse_date(dateText)
    return [parseSeason(monthYear[0]), monthYear[1]]


def parse_date(dateText: str):
    params = dateText.split(" ")
    today = datetime.datetime.today()

    if len(params) == 4:
        monthsMap = {
            'января': 1,
            'февраля': 2,
            'марта': 3,
            'апреля': 4,
            'мая': 5,
            'июня': 6,
            'июля': 7,
            'августа': 8,
            'сентября': 9,
            'октября': 10,
            'ноября': 11,
            'декабря': 12,
        }
        month = monthsMap.get(params[1])
        return [month, today.year]

    if len(params) == 3:
        day = params[0]
        if day == 'сегодня':
            date = [today.month, today.year]
        elif day == 'вчера':
            date = datetime.date.today() - datetime.timedelta(days=1)
            date = [date.month, date.year]
        else:
            print('Не смогли разобрать день: ', dateText)
            return [None, None]

        return date

    print('Не смогли разобрать формат:', dateText)
    return [None, None]


# Зима – 1
# Весна – 2
# Лето – 3
# Осень – 4
def parseSeason(month):
    if 2 < month < 6:
        return 2

    if 5 < month < 9:
        return 3

    if 8 < month < 12:
        return 4

    return 1


def parseWall(wall):
    wall_list = ["блочный", "шлакоблочный", "деревянный", "монолитный", "газобетонный", "панельный", "кирпичный"]
    return wall_list.index(wall) + 1


def parseCountRooms(rooms):
    if rooms == "студия":
        return 1

    try:
        count = int(rooms)
        return count
    except ValueError:
        return None
