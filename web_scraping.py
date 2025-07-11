from bs4 import BeautifulSoup
import lxml
import requests
import pandas


url = 'https://books.toscrape.com'


# scrape data from web
def extract_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    book_cards = soup.find_all('article', class_='product_pod')
    books = []

    for card in book_cards:
        # get title; check if h3.a exists
        title = card.h3.a['title']
            
        # get link
        # link = card.h3.a['href']
        # imageURL = card.find('img')['href']
        rating = card.find('p', class_='star-rating')['class'][1]
        price = card.find('p', class_='price_color').text.strip()
        availability = card.find('p', class_='instock availability').text.strip()

        book = {
            'title': title,
            # 'link': link,
            # 'imageURL': imageURL,
            'rating': rating,
            'price': price,
            'availability': availability
        }

        print(book)
        books.append(book)

    return books

# transform the data
def transform_the_data(df):

    # Convert list into data frame
    data = pandas.DataFrame(df)

    # 1. Inspect the raw data
    print("Basic overview of the data:")
    print(data.head())

    print("\nShape of the data: ",  data.shape)

    print("\nInfo:")
    data.info()

    print("\nDescribe:")
    print(data.describe(include='all'))

    # 2. Check if there are missing values per column
    print(data.isnull().sum())

    # if there are missing title we want to drop those rows
    data = data.dropna(subset=['title'])

    # 3. Convert to string all column data type
    data['title'] = data['title'].astype(str)
    data['price'] = data['price'].astype(str)
    data['availability'] = data['availability'].astype(str)

    # 4. Clean the data
    # I want the ratings to be a float number equivalent.

    # Mapping dictionary
    rating_map = {
        'One': 1.0,
        'Two': 2.0,
        'Three': 3.0,
        'Four': 4.0,
        'Five': 5.0
    }
    data['rating_num'] = data['rating'].map(rating_map)

    # I also want to clean the price and make a new column wioth currency
    data['price_clean'] = data['price'].str.replace('Â£', '')
    data['currency'] = data['price'].astype(str).str[1]

    return data


# RUN ETL
df = extract_data(url)
data = transform_the_data(df)