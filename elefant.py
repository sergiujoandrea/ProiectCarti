from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://www.elefant.ro/serch?SearchTerm=star+wars&StockAvailability=true&category.lvl0=Carti')
sleep(3)
driver.refresh()
sleep(5)
button = driver.find_element_by_xpath('//button[@class="load-more-products"]')

while True:
    try:
        driver.execute_script("arguments[0].click();", button)
        sleep(10)
    except:
        break
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(10)