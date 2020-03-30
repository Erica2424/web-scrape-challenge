# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import pprint
import pandas as pd
from time import sleep

def mars_scrape():
    mars = {}

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    sleep(1)
    ourwebpage = browser.html
    soup = bs(ourwebpage, 'html.parser')
    x = soup.body.find_all(class_="content_title")
    alltitle= []

    for i in x[1:]:
        alltitle.append(i.find('a').text.strip())

    alltitle = alltitle[0]

    mars['title'] = alltitle

    paragraph = soup.body.find_all(class_="article_teaser_body")

    news_p = []

    for i in paragraph:
        #print(i.text)
        news_p.append(i.text)
    news_p = news_p[0]

    mars['news_paragraph'] = news_p

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    sleep(1)


    browser.click_link_by_id('full_image')

    z = browser.find_link_by_partial_text("more info")
    z.click()
    sleep(1)

    imgwebpage = browser.html
    soup2 = bs(imgwebpage, 'html.parser')

    image_path = soup2.find(class_="main_image")['src']
    image_full_path = "https://www.jpl.nasa.gov" + image_path

    mars["feature_img"]= image_full_path

    mars_table = pd.read_html("https://space-facts.com/mars/")[0]
    mars_table.rename(columns={0: "Category", 1: "Value"}, inplace=True)

    mars["mars_table"]= mars_table

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    sleep(1)

    image = []

    for i in range(4):
        browser.find_by_css("a.product-item h3")[i].click()
        sleep(1)
        html_image = browser.html
    
        soupitem = bs(html_image, 'html.parser')


        zz = soupitem.find('a', text="Sample")
        image.append(zz['href'])
    
        browser.back()
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": image[0]},
    {"title": "Cerberus Hemisphere", "img_url": image[1]},
    {"title": "Schiaparelli Hemisphere", "img_url": image[2]},
    {"title": "Syrtis Major Hemisphere", "img_url": image[3]},
]

    mars["mars_image"]= hemisphere_image_urls

    return mars 




    






    



