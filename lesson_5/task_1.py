from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient


def put_in_mongo(data):
    client = MongoClient('localhost', 27017)
    db = client['mvideo']
    collection = db['mvideo']
    for doc in data:
        collection.insert_one(doc)


def parse_top():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://www.mvideo.ru/")

    driver.execute_script("window.scrollTo(0, 1700);")
    driver.find_element(By.XPATH, '//div[@class="mvid-carousel-inner"]/button[2]').click()

    path = driver.find_element(By.XPATH,
                               '//div[contains(@class, mvid-carousel-outer) and contains(@class, mv-hide-scrollbar)]')
    titles = path.find_elements(By.XPATH, "//mvid-product-cards-group//div[@class='title']")
    prices = path.find_elements(By.XPATH, "//mvid-product-cards-group//span[@class='price__main-value']")
    links = path.find_elements(By.XPATH, "//mvid-product-cards-group//div[@class='title']/a")

    res = []
    for title, price, link in zip(titles, prices, links):
        item = dict()
        item['title'] = title.text
        item['price'] = int(price.text.replace(' ', ''))
        item['link'] = link.get_attribute('href')
        res.append(item)

    put_in_mongo(res)


if __name__ == '__main__':
    parse_top()
