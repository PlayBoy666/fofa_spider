# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from pyquery import PyQuery as pq
from config import *
import pymongo


# 中文编码设置
reload(sys)
sys.setdefaultencoding('utf-8')
Type = sys.getfilesystemencoding()

#连接mongodb数据库
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


#创建浏览器
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser,10)
browser.set_window_size(1400, 900)

#登录操作
def login():
    try:
        browser.get('https://i.nosec.org/login?service=http%3A%2F%2Ffofa.so%2Fusers%2Fservice')
        input_user = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#username')))
        input_pass = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#password')))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-form > table > tbody > tr:nth-child(4) > td > button')))
        input_user.send_keys(FOFA_USERNAME)
        input_pass.send_keys(FOFA_PASSWORD)
        submit.click()
        browser.implicitly_wait(30)
    except TimeoutException:
        return login()

#搜索操作（加入搜索关键字）
def search(keyword):
    try:
        input_keyword = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#search_form > input.search_tj')))
        input_keyword.send_keys(keyword)
        submit.click()
        browser.implicitly_wait(30)
    except TimeoutException:
        return search(keyword)
#翻页操作
def next_page(page_number):
    try:
        submit_next=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#will_page > a.next_page')))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ajax_content')))
        submit_next.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#will_page > em'),str(page_number)))
        get_products()
    except TimeoutException:
        return next_page(page_number)

#获取数据
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ajax_content')))
    #browser.implicitly_wait(30)
    html = browser.page_source
    doc = pq(html)
    items = doc('.list_main .list_mod_all #ajax_content .download_loader .list_mod').items()

    for item in items:
        product={
            'url':item.find('.list_mod_t').text(),
            'info':item.find('.list_mod_c .row .col-lg-4 .list_sx1').text()
        }
        #print(product)
        save_to_mongo(product)

#存储到mongodb
def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('sucess', result)
    except Exception:
        print('faild', result)

def main():
    login()
    str1=FOFA_SEARCH_KEYWORD
    search(str1)
    for i in range(2,int(PAGE)):
        next_page(i)


if __name__ == '__main__':
    main()
    browser.quit()



