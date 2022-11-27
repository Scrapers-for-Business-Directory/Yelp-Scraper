import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
from time import sleep
ua = UserAgent()

items_list = []
for x in range(0, 20, 10):
    headers = {'User-Agent': ua.random}
    response = requests.get(f'https://www.yelp.com/search?find_desc=Doctors&find_loc=Miami, FLorida&start={x}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.select('.padding-l3__09f24__IOjKY')
    print(f'Page {x}')
    
    n = 0
    for card in cards:
        try:
            name = card.select_one('.css-1m051bw').text
        except:
            name = None
        try:
            link = 'https://www.yelp.com' + card.select_one('.css-1m051bw')['href']
        except:
            link = None
        try:
            tags = card.select('.css-11bijt4')
            [t.text for t in tags]
        except:
            tags = None
        try:
            rate = card.select_one('.css-gutk1c').text
        except:
            rate = None
        try:
            reviews = card.select_one('.css-chan6m').text.replace('(','').replace(')', '')
        except:
            reviews = None

        response = requests.get(link)
        sleep(2)
        soup = BeautifulSoup(response.text, 'html.parser')
        bar = soup.select_one('.stickySidebar__09f24__wATYu')
        n = n + 1
        print(f'Doctors {n}')

        try:
            if bar.select_one('.border-color--default__09f24__NPAKY+ .border--top__09f24__exYYb .css-na3oda+ .css-1p9ibgf').text:
                phone = bar.select_one('.border-color--default__09f24__NPAKY+ .border--top__09f24__exYYb .css-na3oda+ .css-1p9ibgf').text
            else:
                phone = bar.select_one('.css-na3oda+ .css-1p9ibgf').text
        except:
            phone = None
        try:
            address = bar.select_one('.css-qyp8bo').text
        except:
            address = None
        try:
            website = bar.select_one('.css-na3oda+ .css-1p9ibgf .css-1um3nx').text
        except:
            website = None

        items = {
            'Name': name,
            'Website': website,
            'Phone': phone,
            'Address': address,
            'Tags': tags,
            'Rating': rate,
            'Reviews': reviews,
            'Yelp link': link
        }
        items_list.append(items)

df = pd.DataFrame(items_list)
df.to_csv('data.csv', index = False)
print(df)
