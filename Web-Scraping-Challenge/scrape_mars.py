# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")

        news_title = slide_element.find("div", class_="content_title").get_text()

        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph

# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper
def featured_image(browser):
    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")
    try:
        img_url = img.get("src")
    except AttributeError:
        return None 

    img_url = f"https://www.jpl.nasa.gov{img_url}"
    return img_url

# Mars Facts Web Scraper
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    try:
        df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)

    return df.to_html(classes="table table-striped")

# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}

        browser.find_by_css("a.product-item h3")[item].click()

        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

        hemisphere["title"] = browser.find_by_css("h2.title").text

        hemisphere_image_urls.append(hemisphere)
        
        browser.back()
    return hemisphere_image_urls

# Helper Function
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere

def scrape_all():
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())