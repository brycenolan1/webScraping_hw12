from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    
    #retrieve latest headline & headline teaser paragraph
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    soup = bs(browser.html, 'lxml')
    
    news_title = []
    title = soup.find('div', class_='content_title')
    
    title_text = title.text.strip()
    news_title.append(title_text)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    soup = bs(browser.html, 'lxml')
    
    news_p = []
    paragraph = soup.find('div', class_='article_teaser_body')
    
    paragraph_text = paragraph.text.strip()
    news_p.append(paragraph_text)

    #retrieve latest featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    soup = bs(browser.html, 'lxml')
    
    base_url = 'https://www.jpl.nasa.gov'
    
    image_url = soup.find('article', class_='carousel_item').a['data-fancybox-href']
    featured_image_url = f'{base_url}{image_url}'

    #retrieve latest Mars weather tweet
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    soup = bs(browser.html, 'lxml')

    mars_tweet = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather = mars_tweet.text.strip()

    #retrieve Mars data table
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    soup = bs(browser.html, 'lxml')

    mars_table = soup.find('tbody')

    space_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(space_url)
    mars_df = mars_table[1]
    mars_df.columns = ['description', 'value']
    mars_df.set_index('description', inplace=True)
    mars_df.head()

    mars_table_2 = mars_df.to_html()

    #retrieve Mars hemisphere images
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    soup = bs(browser.html, 'lxml')

    base_url = 'https://astrogeology.usgs.gov'
    thumb_results = soup.find_all('img', class_ = 'thumb')

    image_url = []

    for thumb_result in thumb_results:
            partial_img_link = thumb_result['src']
            image_url.append(base_url + partial_img_link)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    soup = bs(browser.html, 'lxml')

    base_url = 'https://astrogeology.usgs.gov'
            
    title_results = soup.find_all('div', class_ = 'description')
    title = []

    for variable in title_results:
            titles = variable.h3.text.strip()
            title.append(titles)

    hemisphere_image_urls = [
            {"title": title[0], "img_url": image_url[0]},
            {"title": title[1], "img_url": image_url[1]},
            {"title": title[2], "img_url": image_url[2]},
            {"title": title[3], "img_url": image_url[3]},
            ]

    mars_data = {
        "news_title": title_text,
        "news_paragraph": paragraph_text,
        "featured_image": featured_image_url,
        "mars_weather": mars_weather,
        "mars_table": mars_table_2,
        "hemisphere_images": hemisphere_image_urls
    }

    browser.quit()

    return mars_data