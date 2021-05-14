from time import sleep
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import logging

"""
Site-uri de pe care am luat coduri sau ne-am inspirat pentru realizarea proiectului:
1. https://stackoverflow.com/questions/48477688/scrape-page-with-load-more-results-button
2. https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
3. https://stackoverflow.com/questions/37879010/selenium-debugging-element-is-not-clickable-at-point-x-y
4. https://www.youtube.com/watch?v=XVv6mJpFOb0&ab_channel=freeCodeCamp.org
5. https://github.com/lkuffo/web-scraping
"""

driver = webdriver.Chrome('./chromedriver.exe')  # alegem ca browser Chrome pentru a parcurge cu selenium site-ul
driver.get(
    'https://www.elefant.ro/serch?SearchTerm=star+wars&StockAvailability=true&category.lvl0=Carti')  # deschidem în
# Chrome pagina respectivă
sleep(3)  # așteptăm 3 sec pentru a se încărca pagina
driver.refresh()  # dăm refresh la pagină
sleep(5)  # așteptăm 5 sec pentru a se încărca pagina
button = driver.find_element_by_xpath(
    '//button[@class="load-more-products"]')  # creăm o variabilă buton pe care trebuie să îl apăsăm de n ori pentru
# a găsi toate rezultatele

# file=open("fisier.txt","w",encoding="utf-8") #deschidem un fișier folosit doar pentru a vedea întreg codul html și
# pentru a verifica dacă până în acest punct programul face ceea ce dorim

for i in range(16):  # apăsăm butonul de Load more de 16 ori, a 17-a oară load-uind o pagină fără niciun rezultat
    driver.execute_script("arguments[0].click();",
                          button)  # apăsăm butonul pentru a încărca mai multe rezultate ale căutării
    sleep(10)  # așteptăm 10 sec pentru a se încărca următoarele rezultate ale căutării

driver.execute_script(
    "window.scrollTo(0, document.body.scrollHeight);")  # dăm scroll down pentru a se încărca toată pagina și a avea
# codul html complet
sleep(10)  # așteptăm 10 sec pentru a se încărca pagina completă
html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, 'lxml')
# driver.quit()  # închidem browserul Chrome după ce a fost parcurs până la final și am extras codul html din spatele
# site-ului

# file.write(str(soup.prettify()))
# file.close()

carti = soup.find_all('div',
                      class_='product-list-item col-lg-3 col-md-4 col-sm-4 col-xs-6 grid-view lazy')  # observăm că
# fiecare carte este într-un bloc <div> și are clasa  "product-list-item col-lg-3 col-md-4 col-sm-4 col-xs-6
# grid-view lazy"
"""
with open("carti.txt", "w", encoding="utf-8") as f:
    for carte in carti:
        f.write(str(carte))
"""

with open('fisier_json.txt', 'w') as file_json:
    for carte in carti:  # parcurgem blocul <div> al fiecărei cărți pentru a obține titlul, autorul și prețul ei
        try:  # folosim un try pentru a trata "attributeerror: 'nonetype' object has no attribute 'text'" in momentul
            # in care nu returneaza None
            autor = carte.find('a', class_='product-manufacturer').text  # observăm că autorul este într-un bloc <a> cu
            # clasa 'product-manufacturer'
            titlu = carte.find('a', class_='product-title').text  # observăm că titlu este într-un bloc <a> cu clasa
            # 'product-title'
            pret = carte.find('div', class_='current-price').text  # observăm că prețul este într-un bloc <div> cu clasa
            # 'current-price'
        except Exception as e:
            logging.exception(e)
        json.dump({titlu.strip(): [autor.strip(), pret.strip()]}, file_json, indent=4)  # scriem fișierul json ca în
# cadrul Lab8, dar folosim metoda spilt pentru ca șterge spațiile din stânga și dreapta pe care le-ar interpreta ca \n"
