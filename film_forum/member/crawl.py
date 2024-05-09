from urllib.request import urlopen as uReq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import time
# import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import csv
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from .models import Movies



driver = webdriver.Chrome()

# 我用相對路徑找csv
with open('member/link.csv', 'r', encoding='utf-8') as f:
    file = csv.reader(f)
    for data in file:

        url = data[0]

        driver.get(url)
        infor = driver.find_element(By.CLASS_NAME, "ipc-page-section--bp-xs")


        try:
            test =infor.find_elements(By.CLASS_NAME, "sc-92625f35-7")

            if test:
            
                # IMG : 
                img = infor.find_element(By.CSS_SELECTOR, "img.ipc-image")
                src = img.get_attribute("src")

                # year、time、age
                details_elements = infor.find_elements(By.CLASS_NAME, "sc-d8941411-2 li")
                num_details = len(details_elements)

                year = ''
                age = 'G'
                times = '2h 35m'

                for detail in details_elements:
                    try:
                        a_tag = detail.find_element(By.TAG_NAME, "a")
                        text = a_tag.get_attribute("innerText")
                        
                        if details_elements.index(detail) == 0:
                            year = text
                        elif details_elements.index(detail) == 1:
                            age = text

                    except NoSuchElementException:
                        if num_details != 1:
                            text = detail.get_attribute("innerText")
                            times = text

                # NAME : 
                try:
                    name_div = infor.find_element(By.CLASS_NAME, "sc-d8941411-1")
                    name = name_div.text.strip().split(": ")[1]
                except NoSuchElementException:
                    name =  infor.find_element(By.CLASS_NAME, "hero__primary-text").get_attribute("innerText")


                # INTROUDUCTION
                introu = infor.find_element(By.CLASS_NAME, "kpMXpM").get_attribute("innerText")
                if introu == '':
                    introu = "Unfortunately, there is no information available about this movie at the moment."


                # TAG
                tags = infor.find_elements(By.CLASS_NAME, "ipc-chip__text")
                texts = []
                for index, tag in enumerate(tags):
                    text = tag.get_attribute("innerText")

                    if index != 3:
                        texts.append(text)
                m_tag = ','.join(texts)


                # Director
                direc = infor.find_element(By.CLASS_NAME, "ipc-metadata-list-item__list-content-item").get_attribute("innerText")


                # STARS
                star_sel = driver.find_element(By.CLASS_NAME, "jgUBLM")
                stars = star_sel.find_elements(By.CLASS_NAME, "sc-bfec09a1-1")
                star = []

                for i in stars:
                    s = i.get_attribute("innerText")
                    star.append(s)

                star = ','.join(star)

                movie = Movies(name=name, year=year, time=times, age=age, introduction=introu, img=src,director=direc, star=star,tag=m_tag, rating='0')

                movie.save()
                
        except NoSuchElementException:
            print('\n' + "NoSuchElementException" + '\n')

print("END")
driver.quit()
