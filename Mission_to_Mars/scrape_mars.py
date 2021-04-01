#Dependencies
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from selenium import webdriver
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_scraped_data = {}    


# URL of the page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

#Assigning a variable to the browser html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

# The results are returned as an iterable list
    results = soup.find_all('div', class_='list_text')[0]
    results

# Collecting the latest news title and paragraph
    news_title = results.find('div', class_='content_title').text
# Identifying and returning paragraph of article
    news_p = results.find('div', class_='article_teaser_body').text
# Identifying and returning the latest date
    date = results.find('div', class_='list_date').text
    mars_scraped_data['news_title'] = news_title
    mars_scraped_data['news_paragraph'] = news_p 

# URL of the page to be scraped
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

#Assigning a variable to the browser html
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

# Splinter is used to click on the button to retreive the full image
    browser.links.find_by_partial_text('FULL IMAGE').click()

#Assigning a variable to the browser html
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    soup3

# Collecting the image url for the current Featured Mars Image
    image_url = soup3.find('img', class_='fancybox-image')['src']
    url = 'https://spaceimages-mars.com/'
    featured_image_url = url+image_url
    mars_scraped_data["featured_image_url"] = featured_image_url
    
# URL of the page to be scraped using pandas
    url4 = 'https://galaxyfacts-mars.com/'
    mars_profile_table = pd.read_html(url4)
    mars_profile_df = mars_profile_table[0]
    mars_profile_df.columns = ['Parameter','Mars', 'Earth']
    mars_profile_df.set_index(['Parameter'], inplace = True)

#Converting the table to a html table string
    mars_profile_html = mars_profile_df.to_html()
    mars_profile_html = mars_profile_html.replace("\n", "")
    mars_scraped_data["mars_profile_table"] = mars_profile_html

# Url of the page to be scraped
    hemisphere_base_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_base_url)

#Assigning a list to the image urls.
    image_urls = []
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img").click()

#Getting cerberus image    
    cerberus_open = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    cerberus_image = browser.html
    soup = BeautifulSoup(cerberus_image, "html.parser")
    cerberus_url = soup.find("img", class_="wide-image")["src"]
    cerberus_image_url = hemisphere_base_url + cerberus_url
    cerberus_title = soup.find("h2",class_="title").text
    browser.back()
    cerberus = {"image title":cerberus_title, "image url": cerberus_image_url}
    image_urls.append(cerberus)

#Getting schiaparelli image 
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
    schiaparelli_open = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    schiaparelli_image = browser.html
    soup = BeautifulSoup(schiaparelli_image, "html.parser")
    schiaparelli_url = soup.find("img", class_="wide-image")["src"]
    schiaparelli_image_url = hemisphere_base_url + schiaparelli_url
    schiaparelli_title = soup.find("h2",class_="title").text
    browser.back()
    schiaparelli = {"image title":schiaparelli_title, "image url": schiaparelli_image_url}
    image_urls.append(schiaparelli)

#Getting syrtis image
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[3]/a/img").click()
    syrtis_major_open = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    syrtis_major_image = browser.html
    soup = BeautifulSoup(syrtis_major_image, "html.parser")
    syrtis_major_url = soup.find("img", class_="wide-image")["src"]
    syrtis_major_image_url = hemisphere_base_url + syrtis_major_url  
    syrtis_major_title = soup.find("h2",class_="title").text   
    browser.back()
    syrtis_major = {"image title":syrtis_major_title, "image url": syrtis_major_image_url}
    image_urls.append(syrtis_major)

#Getting valles_marineris image
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img").click()
    valles_marineris_open = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    valles_marineris_image = browser.html
    soup = BeautifulSoup(valles_marineris_image, "html.parser")
    valles_marineris_url = soup.find("img", class_="wide-image")["src"]
    valles_marineris_image_url = hemisphere_base_url + syrtis_major_url
    valles_marineris_title = soup.find("h2",class_="title").text
    browser.back()
    valles_marineris = {"image title":valles_marineris_title, "image url": valles_marineris_image_url}
    image_urls.append(valles_marineris)

    browser.quit()


    mars_scraped_data["hemisphere_image_urls"] = image_urls

    return mars_scraped_data