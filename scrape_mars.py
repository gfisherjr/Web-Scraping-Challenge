# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser

import pandas as pd
import requests
import time

def scrape():
    # Set executable path
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    #response = requests.get(url)
    
    browser.visit(url)
    time.sleep(5)
    html = browser.html

    #data = response.text
    soup = bs(html, 'html.parser')

    result = soup.find('div', class_='list_text')
    news_title = result.find('div', class_='content_title').text
    news_p = result.find('div', class_='article_teaser_body').text

    # news_title = soup.find("div", class_="content_title").find("a").text.strip()
    # news_p = soup.find("div", class_="rollover_description_inner").text.strip()

    # JPL Mars Space Images - Featured Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html_jpl = browser.html
    soup = bs(html_jpl, "html.parser")

    first_half_featured_url = "https://www.jpl.nasa.gov"
    second_half_featured_url_medium = soup.find("div", class_="carousel_items").find("a")["data-fancybox-href"]
    featured_url_wallpaper_medium = first_half_featured_url + second_half_featured_url_medium

    browser.quit()

    # Mars Weather - Twitter
    browser = Browser('chrome', **executable_path, headless=False)
    
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)
    time.sleep(4)

    html_twitter = browser.html
    soup = bs(html_twitter, "html.parser")

    # Find Twitter Info
    results_1 = soup.find_all("span")

    lines = [span.get_text() for span in results_1]

    weather = []

    for line in lines:
        if "InSight" in line:
            weather.append(line)

    mars_weather = weather[0]
    mars_weather

    browser.quit()

    # Mars Facts
    browser = Browser('chrome', **executable_path, headless=False)
    url_mars_facts = "https://space-facts.com/mars/"
    browser.visit(url_mars_facts)

    tables = pd.read_html(url_mars_facts)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df.set_index("Description", inplace=True)
    mars_facts_df   

    mars_html_table = mars_facts_df.to_html()
    mars_html_table = mars_html_table.replace('\n', '')

    browser.quit()

    # Mars Hemispheres
    browser = Browser('chrome', **executable_path, headless=False)
    mars_hems_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hems_url)

    html_hems = browser.html
    soup = bs(html_hems, "html.parser")

    images = soup.find_all("div", class_="item")

    first_half_url = "https://astrogeology.usgs.gov/"

    hemisphere_images_urls = []

    for image in images:
        title = image.find("h3").text
        picture_url = image.find("a", class_="itemLink product-item")["href"]
        browser.visit(first_half_url + picture_url)
    
        html_picture = browser.html
        soup = bs(html_picture, "html.parser")
    
        full_url = first_half_url + soup.find("img", class_="wide-image")["src"]
    
        hemisphere_images_urls.append({"title": title, "img_url": full_url})

    browser.quit()

    # All Scraped Data
    mars_info = {
        "NASA_News_Title": news_title,
        "NASA_News_Paragraph": news_p,
        "JPL_Featured_Image_URL": featured_url_wallpaper_medium,
        "Mars_Weather": mars_weather,
        "Mars_Facts": mars_html_table,
        "Mars_Hemispheres": hemisphere_images_urls
    }

    return mars_info

if __name__ == '__main__':
    scrape()