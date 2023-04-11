from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_photo_url(soup):   
    try:
        photo_url = soup.find("td", attrs = {'class' :'col-avatar'}).find("img")['data-src']
    except AttributeError:
        photo_url = " "
    return photo_url

def get_player_url(soup):   
    try:
        player_url = "https://sofifa.com" + soup.find("td", attrs = {'class' :'col-name'}).find("a")['href']
    except AttributeError:
        player_url = " "
    return player_url

def get_full_name(soup):   
    try:
        full_name = soup.find("td", attrs = {'class' :'col-name'}).find("a")['aria-label']
    except AttributeError:
        full_name = " "
    return full_name

def get_short_name(soup):   
    try:
        short_Name = soup.find("td", attrs = {'class' :'col-name'}).find("a").text
    except AttributeError:
        short_Name = " "
    return short_Name

if __name__ == '__main__':

    URL = 'https://sofifa.com/players?r=230021&set=true'

    data = {'photo_url' : [], 'player_url' : [], 'full_name' : [], 'short_name' : []}

    for offset in range(0,2):
        URL = URL + str(offset)
        
        webpage = requests.get(URL)
        
        # p_soup = p_html.text #will get the textual html format
        soup = BeautifulSoup(webpage.content, "html.parser")
        table = soup.find('tbody') #finding the body of the table
        for i in table.findAll('tr'):   # to check entire the table having Table row 
            td = i.findAll('td')
        
            # Function calls to display all necessary product information
            data['photo_url'].append(get_photo_url(soup))
            data['player_url'].append(get_player_url(soup))
            data['full_name'].append(get_full_name(soup))
            data['short_name'].append(get_short_name(soup))

