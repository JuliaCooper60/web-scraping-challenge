# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
# from datetime import datetime
# import os
# import time
from webdriver_manager.chrome import ChromeDriverManager 

def init_browser():
   # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser
   
def scrape():
    browser = init_browser()
    # Mars News URL of page to be scraped
    browser.visit('https://mars.nasa.gov/news/')
    # add waittime to delay loading the page in case page loads slow- splinter function
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Retrieve the latest news title and paragraph
    article_soup=soup(browser.html,'html.parser')
    article_text = article_soup.select_one('div.list_text')
    news_title = article_text.find('div', class_= 'content_title').get_text() 
    news_p = article_text.find('div', class_= 'article_teaser_body').get_text() 

    # Mars Image to be scraped
    browser.visit('https://spaceimages-mars.com')
    full_image_button = browser.find_by_tag('button')[1]
    full_image_button.click()
    img_soup = soup(browser.html, 'html.parser')
    # Retrieve featured image link
    relative_image_url = img_soup.find('img', class_='fancybox-image').get('src')
    featured_image_url = f'https://spaceimages-mars.com/{relative_image_url}'
    
     # Mars facts to be scraped, converted into html table
    fact_table = pd.read_html('https://galaxyfacts-mars.com')[0]
    fact_table.columns=['Description', 'Mars', 'Earth']
    fact_table.set_index('Description', inplace=True)
    mars_fact_table_html = fact_table.to_html(classes= ["table", "table-striped"], justify = "left")
    
    # Mars hemisphere name and image to be scraped
    browser.visit('https://marshemispheres.com')
    Mars_hemisphere_image_urls = [] 
    item_links = browser.find_by_css('a.product-item img')
    item_links[0].click()
    img_soup = soup(browser.html, 'html.parser')
    #go to the page that has all of the hemispheres on it 
    browser.visit('https://marshemispheres.com')
    # Iterate through each hemisphere data
    for i in range(len(item_links)):
        hemisphere = {}
        
        browser.find_by_css('a.product-item img')[i].click()
    
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href'] 
        
        hemisphere['title'] = browser.find_by_css('h2.title').text
        Mars_hemisphere_image_urls.append(hemisphere)
        browser.back()

    mars_data = {
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url": featured_image_url,
    "fact_table": mars_fact_table_html,
    "hemisphere_images": Mars_hemisphere_image_urls
        }

    browser.quit()

    return mars_data 

if __name__ == "__main__":
    scrape()
