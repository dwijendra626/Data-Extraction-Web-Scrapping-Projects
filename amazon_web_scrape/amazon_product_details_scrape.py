from bs4 import BeautifulSoup
import requests
import pandas as pd

#function to extract product title
def get_title(new_soup):   
    try:
        title = new_soup.find("span", attrs = {'class' : 'a-size-large product-title-word-break'}).text.strip()
    except AttributeError:
        title = " "
    return title
    
#function to extract product price
def get_price(new_soup):
    try:
        price = new_soup.find("span", attrs = {'class' : "a-color-price a-text-bold"}).text.strip()
    except AttributeError:
        price = " "    
    return price


#function to extract product rating
def get_rating(new_soup):
    try:
        rating = new_soup.find("i", attrs = {'class' : "a-icon a-icon-star a-star-5"}).text.strip()
    except AttributeError:
        rating = " "
    return rating


# function to extract product_review_count
def get_product_review_count(new_soup):
    try:
        product_review_count = new_soup.find("span", attrs= {'id' : 'acrCustomerReviewText'}).text.strip()
    except AttributeError:
        product_review_count = " "
    return product_review_count


if __name__ == '__main__':
    
    #webpage URL
    URL = 'https://www.amazon.com/s?k=macbook&crid=36RFS9O24MYNP&sprefix=playsmacbook%2Caps%2C370&ref=nb_sb_noss'

    #headers for requests
    Header = ({'User-Agent' : 'https://developers.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes', 'Accept-Language': 'en-US, en;q=0.5'})

    # HTTP request
    webpage = requests.get(URL, headers = Header)

    #soup object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")
    
    # fetch all links from the page
    links = soup.find_all("a", attrs= {'class' : 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

    # store the links
    links_list = []

    # loop for extracting product links only
    for link in links:
        links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[], "reviews":[]}
    
    # Loop for extracting product details from each link 
    for product_link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + product_link, headers=Header)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_product_review_count(new_soup))
        

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df.to_excel("amazon_data.xlsx", index=False)
    amazon_df.to_csv("amazon_data.csv", index=False)

    