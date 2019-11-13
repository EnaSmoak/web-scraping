import re
import datetime
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def main():
    # get property information
    def property_info(properties_list):
        property_name = []
        property_beds = []
        property_showers = []
        property_garages = []
        property_area = []
        property_description = []
        property_price = []
        property_currency = []
        property_rent_period = []
        property_urls = []
        property_address = []
        property_time_posted = []

        for link in properties_list:
            url = base_url + link.find('a').attrs['href']
            names = (
                link.find('div', {'class': 'mqs-prop-dt-wrapper'}).find('h2').text).strip()
            beds = noValue(link.find('li', {'class': 'bed'}))
            showers = noValue(link.find('li', {'class': 'shower'}))
            garages = noValue(link.find('li', {'class': 'garage'}))
            area = noValue(link.find('li', {'class': 'area'}))
            address = link.find('a').img['title'].split('at')[1]
            time_posted = link.find('p', {'class': 'wsnr'}).text

            description = link.find('p', {'class': ''}).text
            price, currency, rent_period = extractPriceCurrencyPeriod(
                link.find('p', {'class': 'h3'}).text)

            property_urls.append(url)
            property_name.append(names)
            property_beds.append(beds)
            property_showers.append(showers)
            property_garages.append(garages)
            property_area.append(area)
            property_description.append(description)
            property_price.append(price)
            property_currency.append(currency)
            property_rent_period.append(rent_period)
            property_address.append(address)
            property_time_posted.append(time_posted)

        df_properties = pd.DataFrame({'property': property_name,
                                      'beds': property_beds,
                                      'showers': property_showers,
                                      'garage': property_garages,
                                      'area': property_area,
                                      'description': property_description,
                                      'price': property_price,
                                      'currency': property_currency,
                                      'rent_period': property_rent_period,
                                      'url': property_urls,
                                      'address': property_address,
                                      'time_posted': property_time_posted
                                      })
        return(df_properties)

    # function to extract price
    # def extractPrice(x):
    #     x = x.replace('Price', '').replace(':', '').replace(',', '')
    #     if 'GH₵' in x:
    #         price = x.strip().replace('GH₵', '').split('/')[0].strip()
    #         currency = 'GH₵'
    #     elif '$' in x:
    #         price = x.strip().replace('$', '').split('/')[0].strip()
    #         currency = '$'
    #     else:
    #         price = 'Not Available'
    #         currency = None
    #     return currency, price

    def extractPriceCurrencyPeriod(x):
        x = x.replace('Price', '').replace(':', '').replace(',', '')
        if 'GH₵' in x:
            a = x.strip().replace('GH₵', '').split('/')
            price = a[0].strip()
            currency = 'GH₵'
            period = a[1] if len(a) > 1 else None
        elif '$' in x:
            a = x.strip().replace('$', '').split('/')
            price = a[0].strip()
            currency = '$'
            period = a[1] if len(a) > 1 else None
        else:
            price = 'Not Available'
            currency = None
            period = None
        return price, currency, period

    # function to extract currency
    # def extratCurrency(x):

    # add 0 where there is empty / no value exists

    def noValue(x):
        if x is None:
            return 0
        else:
            return x.text

    # write to csv
    def save_data(df):
        file_time = datetime.datetime.now()
        file_time = file_time.strftime('%Y-%m-%d')
        file_name = 'meqasa_'+file_time+'.csv'

        df.to_csv(file_name, index=False)

    df_final = pd.DataFrame([])

    base_url = 'https://meqasa.com'
    results = requests.get('https://meqasa.com/houses-for-rent-in-ghana')

    soup = BeautifulSoup(results.content, 'lxml')
    properties_list = soup.find_all(
        'div', {'class': 'row mqs-featured-prop-inner-wrap clickable'})

    len(properties_list)
    df_final = property_info(properties_list)
    save_data(df_final)

    # print 10 rows
    print(df_final.head(10))

    df_final


if __name__ == "__main__":
    main()
