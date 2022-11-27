import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
from time import sleep
ua = UserAgent()

def scrape_go(category, city, state, pages):
    items_list = []
    col1, col2 = st.columns(2)
    progress = col1.metric('Pages scraped', 0)
    n = 0
    for x in range(0, int(pages * 10), 10):
        n = n + 1
        headers = {'User-Agent': ua.random}
        response = requests.get(f'https://www.yelp.com/search?find_desc={category}&find_loc={city}, {state}&start={x}', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select('.padding-l3__09f24__IOjKY')
        progress.metric('Pages scraped', n)
        k = 0
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
                tags = [t.text for t in tags]
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
            soup = BeautifulSoup(response.text, 'html.parser')
            bar = soup.select_one('.stickySidebar__09f24__wATYu')

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
    col2.metric('Total data scraped', len(df))
    st.dataframe(df)

    csv = df.to_csv().encode('utf-8')
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name = 'yelp-data.csv',
    mime='text/csv',
    )

if __name__ == "__main__":
    st.title('YELP SCRAPER')
    with st.sidebar:
        st.caption('Select the category to scrape')
        restaurant = st.selectbox('Select what you want',
        ('Restaurants', "Delivery", "Reservations", "Burger", "Japanese", "Chinese", "Mexican", "Italian", "Thai"),
        label_visibility = 'collapsed'
    )   
    
        home_service = st.selectbox(
            'Choose what you want',
            ('Home services', 'Contractors', 'Landscaping', 'Electricians', "Locksmiths",
            'Homecleaning', 'Movers', 'HVAC', 'Plumbers'),
            label_visibility = 'collapsed'
        )

        auto_service = st.selectbox(
            'Choose what you want',
            ('Auto services','Auto repair', 'Car dealers', 'Auto detailing', 'Oil change', 'Body shops', 'Parking',
            'Car wash', 'Towing'), label_visibility = 'collapsed'
            )

        more = st.selectbox(
            'Choose what you want',
            ('Dry cleaning', 'Hair salon', 'Phone repair', 'Gyms', 'Bars', 'Massage',
            'Nightlife', 'Shopping'), label_visibility = 'collapsed'
        )

        if restaurant:
            category = restaurant
        elif home_service:
            category = home_service
        elif auto_service:
            category = auto_service
        elif more:
            category = more

        city = st.text_input('Input the city. EX: Miami')
        state = st.text_input('Input the state. EX: Florida')

        start_scraping = st.button('Scrape!')

    with st.form('Scraper'):
        st.caption("Choose the category and location in the sidebar")
        st.caption('Fields to be scraped are: Name, Website, Phone, Address, Tags, Rating, Review and Yelp link')
        pages = st.number_input('Number of pages to scrape') + 1
        start_scraping = st.form_submit_button('Scrape!')

    if start_scraping :
        scrape_go(category, city, state, pages)
        st.snow()
        st.success('Done!')