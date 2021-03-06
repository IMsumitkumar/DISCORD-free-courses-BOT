import re
import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen
from datetime import datetime
from datetime import date, datetime, timedelta
from urllib.request import Request, urlopen
from selenium import webdriver
import configration 

def recent_data(data):
    now = datetime.now()
    day_before_yesterday = datetime.now() - timedelta(days=5)
    date_time = now.strftime("%Y-%m-%d")
    day_before_yesterday = day_before_yesterday.strftime("%Y-%m-%d")
    
    data = configration.DATAFRAME
    data = data[(data['date_time'] >= day_before_yesterday)]

    return data

def scrap_free_course(wd, url_dict: dict, df):

    for name, url in url_dict.items():
        wd.get(url.format(q=1))
        time.sleep(1)
        beautify_page = bs4(wd.page_source,"html.parser")

        pages = beautify_page.find_all("li", class_="page-item")
        try:
            total_page = int(pages[-2].a.text)
        except:
            total_page = 1
        
        if total_page >= 2:
            total_page = 2
        else:
            total_page = total_page

        for i in range(1, total_page+1):
            next_url = url.format(q=i)
            wd.get(next_url)
            time.sleep(1)
            next_beautify_page = bs4(wd.page_source,"html.parser")
            
            big_boxes = next_beautify_page.find_all("div",class_='col-xl-4 col-md-6')

            time.sleep(.5)

            for box in big_boxes:
                inside_url = "https://app.real.discount"+str(box.a['href'])
                wd.get(inside_url)
                time.sleep(.5)

                try:
                    duration = wd.find_element_by_xpath('//*[@id="panel"]/div[3]/div[1]/div[1]/div[1]/div[5]/span[3]').text.strip().replace("\n", "")
                except:
                    duration = "Not Available"
                time.sleep(.5)
                try:
                    link = wd.find_element_by_xpath('//*[@id="panel"]/div[3]/div[1]/div[1]/a').get_attribute("href")
                except:
                    link = "https://www.udemy.com/course/the-web-advadeveladnapoper-bootcampnpiabaidbabh/"
                time.sleep(.5)

                page = bs4(wd.page_source,"html.parser")

                try:
                    image = page.find("img", class_="card-img-top")['src']
                except:
                    image = "https://i.imgur.com/NPvfO4I.jpg"
                time.sleep(.5)
                try:
                    category = page.find("div", class_="card-cat-div").text.strip().replace("\n", "")
                except:
                    category = "Not Available"
                time.sleep(.5)
                try:
                    rating = page.find("div", class_="card-rating-div").text.strip().replace("\n", "")
                except:
                    rating = "Not Available"
                time.sleep(.5)
                try:
                    title = page.find("h5", class_="card-title").text.strip().replace("\n", "")
                except:
                    title = "Not Available"
                time.sleep(.5)
                try:
                    desc = page.find("p", class_="card-text").text.strip().replace("\n", "")
                except:
                    desc = "Not Available"
                time.sleep(.5)
                try:
                    now = datetime.now()
                    date_time = now.strftime("%Y-%m-%d")
                except :
                    date_time = "Nothing"

                myDict = {
                    "name":name,
                    "date_time":date_time,
                    "title":title,
                    "rating":rating,
                    "category":category,
                    "image":image,
                    "desc":desc,
                    "duration":duration,
                    "link":link,
                }

                df = df.append(myDict, ignore_index=True)

    wd.close()
    return df
