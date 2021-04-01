#Dependencies
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_scraped_data = {}    

#### NASA Mars News
# Scrape the Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.

# Setup splinter
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)

# URL of the page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

#Assigning a variable to the browser html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

# Examine the results, then determine element that contains sought info
    #print(soup.prettify())

# The results are returned as an iterable list
    results = soup.find_all('div', class_='list_text')[0]
    results

# Collecting the latest news title and paragraph
    news_title = results.find('div', class_='content_title').text
# Identifying and returning paragraph of article
    news_p = results.find('div', class_='article_teaser_body').text
# Identifying and returning the latest date
    date = results.find('div', class_='list_date').text
    #print(f'Date: {date}')
    #print(f'News Title: {news_title}')
    #print(f'News Paragraph: {news_p}')
    mars_scraped_data['news_title'] = news_title
    mars_scraped_data['news_paragraph'] = news_p 

    #browser.quit()


# ### JPL Mars Space Images - Featured Image

# Setup splinter
#    executable_path = {'executable_path': ChromeDriverManager().install()}
#    browser = Browser('chrome', **executable_path, headless=False)

# URL of the page to be scraped
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

#Assigning a variable to the browser html
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

# Examine the results, then determine element that contains sought info
    #print(soup2.prettify())

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
    #print(f'Featured image url: {featured_image_url}')
    mars_scraped_data["featured_image_url"] = featured_image_url
    #browser.quit()

# URL of the page to be scraped using pandas
    url4 = 'https://galaxyfacts-mars.com/'

    mars_planet_profile_table = pd.read_html(url4)
    mars_planet_profile_df = mars_planet_profile_table[0]
    mars_planet_profile_df.columns = ['Parameter','Mars', 'Earth']
    mars_planet_profile_df.set_index(['Parameter'], inplace = True)

#Saving the table as a html file
    #mars_planet_profile_html = mars_planet_profile_df.to_html('mars_planet_profile.html')

#Converting the table to a html table string
    mars_planet_profile_html = mars_planet_profile_df.to_html()
    mars_planet_profile_html = mars_planet_profile_html.replace("\n", "")
    mars_scraped_data["mars_profile_table"] = mars_planet_profile_html
#### Mars Hemispheres

# Setup splinter
#    executable_path = {'executable_path': ChromeDriverManager().install()}
#    browser = Browser('chrome', **executable_path, headless=False)

# Url of the page to be scraped
    hemisphere_base_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_base_url)

#Assigning a list to the image urls.
    image_urls = []
#Using xpath to click on the exact element on the page
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img").click()
#Using xpath to click on the open button on the page
    cerberus_open = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
#Using the browser and BeautifulSoup to extract the image src
    cerberus_image = browser.html
    soup = BeautifulSoup(cerberus_image, "html.parser")
    cerberus_url = soup.find("img", class_="wide-image")["src"]
#Obtaining the url for the image
    cerberus_image_url = hemisphere_base_url + cerberus_url
    #print(cerberus_image_url)
#Obtaining the title of the image
    cerberus_title = soup.find("h2",class_="title").text
    #print(cerberus_title)
#Navigating to the previous page using the back function
    browser.back()
#Appending the url list with the first dictionary of image records
    cerberus = {"image title":cerberus_title, "image url": cerberus_image_url}
    image_urls.append(cerberus)

#Using xpath to click on the exact element on the page
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
#Using xpath to click on the open button on the page
    schiaparelli_open = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
#Using the browser and BeautifulSoup to extract the image src
    schiaparelli_image = browser.html
    soup = BeautifulSoup(schiaparelli_image, "html.parser")
    schiaparelli_url = soup.find("img", class_="wide-image")["src"]
#Obtaining the url for the image
    schiaparelli_image_url = hemisphere_base_url + schiaparelli_url
    #print(schiaparelli_image_url)
#Obtaining the title of the image
    schiaparelli_title = soup.find("h2",class_="title").text
    #print(schiaparelli_title)
#Navigating to the previous page using the back function
    browser.back()
#Appending the url list with the second dictionary of image records
    schiaparelli = {"image title":schiaparelli_title, "image url": schiaparelli_image_url}
    image_urls.append(schiaparelli)

#Using xpath to click on the exact element on the page
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[3]/a/img").click()
#Using xpath to click on the open button on the page
    syrtis_major_open = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
#Using the browser and BeautifulSoup to extract the image src
    syrtis_major_image = browser.html
    soup = BeautifulSoup(syrtis_major_image, "html.parser")
    syrtis_major_url = soup.find("img", class_="wide-image")["src"]
#Obtaining the url for the image
    syrtis_major_image_url = hemisphere_base_url + syrtis_major_url
    #print(syrtis_major_image_url)
#Obtaining the title of the image
    syrtis_major_title = soup.find("h2",class_="title").text
    #print(syrtis_major_title)
#Navigating to the previous page using the back function
    browser.back()
    syrtis_major = {"image title":syrtis_major_title, "image url": syrtis_major_image_url}
    image_urls.append(syrtis_major)

#Using xpath to click on the exact element on the page
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img").click()
#Using xpath to click on the open button on the page
    valles_marineris_open = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
#Using the browser and BeautifulSoup to extract the image src
    valles_marineris_image = browser.html
    soup = BeautifulSoup(valles_marineris_image, "html.parser")
    valles_marineris_url = soup.find("img", class_="wide-image")["src"]
#Obtaining the url for the image
    valles_marineris_image_url = hemisphere_base_url + syrtis_major_url
    #print(valles_marineris_image_url)
#Obtaining the title of the image
    valles_marineris_title = soup.find("h2",class_="title").text
    #print(valles_marineris_title)
#Navigating to the previous page using the back function
    browser.back()
    valles_marineris = {"image title":valles_marineris_title, "image url": valles_marineris_image_url}
    image_urls.append(valles_marineris)

    browser.quit()

#Printing the list of dictionaries of the images obtained
    #image_urls

    mars_scraped_data["hemisphere_image_urls"] = image_urls

    return mars_scraped_data