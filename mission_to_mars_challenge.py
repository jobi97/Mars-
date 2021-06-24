#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[24]:


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None


    return news_title, news_p


# In[25]:


# ## JPL space images featured image


# In[26]:


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# In[27]:


# ## Mars facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


# In[28]:


browser.quit()


# In[3]:


# DELIVERABLE 1
#1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[4]:


html = browser.html
soupy = soup(html, 'html.parser')
soupy


# In[16]:


# 2. Create a list to hold the images and titles.
hemisphere_img_urls = [{'image_url': url, 'title_url': title}]

# 3. Write code to retrieve the image urls and titles for each hemisphere.
hemi_url = soupy.find_all('a', class_='itemLink product-item')

for item in hemi_url:
    hemispheres = {}
    try:
        image_url = soupy.find_all('img', class_='itemLink product-item').get('src')
        title = soupy.find_all('h3').get_text()
        
        hemispheres['image_url'] = url = f'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking{image_url}'
        hemispheres['title_url'] = title
    except AttributeError as error:
            print(error)


# In[17]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_img_urls


# In[ ]:


# 5. Quit the browser
browser.quit()

