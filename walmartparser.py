from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
import xlsxwriter
import threading
from selenium.common.exceptions import TimeoutException

input_path = input('path:')
option = webdriver.FirefoxOptions()
option.set_preference('dom.webdriver.enabled', False)
driver = webdriver.Firefox(options=option,executable_path=input_path)
h_list = []
thread_list = []
all_preitems2 = {'Food,Household and pets/Beverages': 'https://www.walmart.com/cp/beverages/976782',
                 'Food,Household and pets/Coffee': 'https://www.walmart.com/cp/coffee/1086446',
                 'Food,Household and pets/Pantry': 'https://www.walmart.com/cp/meal-solutions-grains-pasta/976794',
                 'Food,Household and pets/Breakfast and cereal': 'https://www.walmart.com/cp/breakfast-food-cereal/976783',
                 'Food,Household and pets/Baking': 'https://www.walmart.com/cp/baking/976780',
                 'Food,Household and pets/plant based food': 'https://www.walmart.com/cp/plant-based-foods/2468673'}
all_links = []

all = ['https://www.walmart.com/m/toys-savings/toys',
       'https://www.walmart.com/browse/sporting-goods-savings/4125_546956_4128?_refineresult=true&_be_shelf_id=70615&search_sort=100&facet=shelf_id:70615',
       'https://www.walmart.com/browse/personal-care-savings-center/0/0/?_refineresult=true&_be_shelf_id=4669738&search_sort=100&facet=shelf_id:4669738',
       'https://www.walmart.com/browse/pet-savings-center-featured/0/0/?_refineresult=true&_be_shelf_id=9611759&search_sort=100&facet=shelf_id:9611759',
       'https://www.walmart.com/browse/beauty-deals/0/0/?_refineresult=true&_be_shelf_id=7598993&search_sort=100&facet=shelf_id:7598993',
       'https://www.walmart.com/browse/automotive-savings/0/0/?_refineresult=true&_be_shelf_id=7855&search_sort=100&facet=shelf_id:7855',
       'https://www.walmart.com/browse/office-supplies-savings/0/0/?_refineresult=true&_be_shelf_id=9061331&search_sort=100&facet=shelf_id:9061331',
       'https://www.walmart.com/browse/home/dorm-bedding/4044_1225301_1225229_9830377?povid=8174172+%7C+2021-07-08+%7C+ShopByCat_Bedding',
       'https://www.walmart.com/browse/home/dorm-bedroom-furniture/4044_1225301_1225229_6830557?povid=8174172+%7C+2021-07-08+%7C+ShopByCat_Furniture',
       'https://www.walmart.com/browse/home/dorm-decor/4044_1225301_1225229_7471338',
       'https://www.walmart.com/browse/workplace-necessities/0/0/?_refineresult=true&_be_shelf_id=8662156&search_sort=100&facet=shelf_id:8662156',
       'https://www.walmart.com/browse/home/dorm-storage/4044_1225301_1225229_4364714',
       'https://www.walmart.com/browse/back-to-school-cleaning-supplies/0/0/?_refineresult=true&_be_shelf_id=7659&search_sort=100&facet=shelf_id:7659',
       'https://www.walmart.com/browse/home/throw-pillows/4044_133012_5991909',
       'https://www.walmart.com/browse/home/desks/4044_103150_97116_91851',
       'https://www.walmart.com/browse/home/dressers/4044_103150_102547_91839',
       'https://www.walmart.com/browse/home/floor-lamps/4044_133012_133113_2803868',
       'https://www.walmart.com/browse/home/folding-tables-chairs/4044_103150_97116_1026080?cat_id=4044_103150_97116_1026080&facet=facet_product_type%3AFolding+Tables',
       'https://www.walmart.com/browse/home/gaming-chairs/4044_103150_97116_9559238',
       'https://www.walmart.com/browse/home/tv-stands/4044_103150_635499_133114',
       'https://www.walmart.com/browse/books/walmart-books-best-sellers/3920_1057224',
       'https://www.walmart.com/browse/food/gluten-free/976759_5004481_5546296',
       'https://www.walmart.com/browse/food/international-food/976759_7404240',
       'https://www.walmart.com/m/Roast-To-Order-Coffee']

a_list = all[0:9]
b_list = all[9:18]
c_list = all[18:27]


def get_html(url, params):
    r = requests.get(url, params=params)
    return r


def get_html2(url, driver1):
    try:
        driver1.get(url)
        html = driver.page_source
    except:
        html = ''
        pass
    return html


def anti_captcha(soup):
    time.sleep(4)
    try:
        button = driver.find_element_by_xpath(
            '/html/body/div/div/div[1]/div/div')
    except:
        pass  # //*[@id="AdOFdDDdjQLJPKK"]  //*[@id="IBDDBZCSmnZjBCt"]
    else:
        ActionChains(driver).click_and_hold(button).perform()
        time.sleep(20)
        try:
            ia = soup.find('div', 're-captcha').find_next('p').find_next('p') != None
        except:
            ia = None
        if ia != None:
            time.sleep(4)
            button = driver.find_element_by_xpath(
                '/html/body/div/div/div[1]/div/div')  # //*[@id="AdOFdDDdjQLJPKK"]  //*[@id="IBDDBZCSmnZjBCt"]
            ActionChains(driver).click_and_hold(button).perform()
            time.sleep(10)


def get_links():
    for preitem in all:
        driver.set_page_load_timeout(15)
        try:
            test_html = get_html2(preitem, driver)
            test_soup = BeautifulSoup(test_html, 'lxml')
        except TimeoutException:
            pass
        else:
            test_items = test_soup.find_all('div', class_='search-result-product-title gridview')
            if not bool(test_items):
                anti_captcha(test_soup)
                test_html = get_html2(preitem, driver)
                test_soup = BeautifulSoup(test_html, 'lxml')
            items = test_soup.find_all('div', class_='search-result-product-title gridview')
            for item in items:
                all_links.append('https://www.walmart.com/' + item.find_next('a').get('href'))
                print('https://www.walmart.com/' + item.find_next('a').get('href'))
            print(len(all_links))


all_data = {'Название': [], 'Ссылка': [],
            'UPC': [], 'Цена': []}


def get_data():
    for link in all_links:
        driver.set_page_load_timeout(15)
        print(link)
        driver.get(link)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        try:
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
        except TimeoutException:
            pass
        else:
            print(soup.find('h1'))
            if soup.find('span', 'price display-inline-block arrange-fit price price--stylized') == None:
                anti_captcha(soup)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
            try:
                title = soup.find('h1').text
            except:
                title = ''
            print(title)
            try:
                price = soup.find('span', 'price display-inline-block arrange-fit price price--stylized').find_next(
                    'span').text
            except:
                price = ''
            print(price)
            b = 0
            for h in html:
                if h == 'u':
                    b = 1
                elif h == 'p' and b == 1:
                    b = 2
                elif h == 'c' and b == 2:
                    b = 3
                elif b == 3:
                    h_list.append(h)
                else:
                    b = 0
            newh_list = []
            for hh in h_list:
                try:
                    int(hh.strip())
                except:
                    print(hh)
                else:
                    newh_list.append(hh.strip())
                    print(hh)
            print(newh_list)
            all_data['Название'].append(title)
            all_data['Цена'].append(price)
            all_data['Ссылка'].append(link)
            all_data['UPC'].append(''.join(newh_list))
            h_list.clear()
            newh_list.clear()


excelfile = input('название файла:')


def save_everything():
    workbook = xlsxwriter.Workbook(excelfile)
    excel = workbook.add_worksheet('Walmart')
    for i, ob in enumerate(all_data.keys()):
        excel.write(0, i, ob)
    for g, obt in enumerate(all_data.values()):
        for f, o in enumerate(obt):
            excel.write(f + 1, g, o)
    workbook.close()


get_links()
get_data()
save_everything()
