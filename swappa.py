import pandas as pd
import requests
from lxml import html
import os
from random import randint
from time import sleep

iphone_64_gb_list = pd.DataFrame()
iphone_128_gb_list = pd.DataFrame()

# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

def retrieve_page():
    url = 'http://swappa.com/buy/apple-iphone-6-plus-unlocked/us'
    page = requests.get(url)
    tree = html.fromstring(page.text)
    listings = tree.xpath('//div[@id="listing_previews"]/div')
    return listings

def compare_df(df1, df2):
    df = pd.concat([df1, df2])
    df = df.reset_index(drop=True)
    df_gpby = df.groupby(list(df.columns))
    idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
    df.reindex(idx)
    return df    

def listing_post(listings):
    global iphone_64_gb_list
    global iphone_128_gb_list
    iphones_for_sale = []
    categories = ['price','condition','listing_id','storage','color',
        'unknown','seller','location','country','description','link']
    for listing in listings:
        listing_text = listing.text_content().replace('\t','').split('\n')
        listing_data = [x for x in listing_text if x.strip()]
        listing_data[0] = int(listing_data[0].strip('$'))
        listing_data += ['http://swappa.com'+listing.xpath('@data-url')[0]]
        listing_dict = {}
        listing_dict = dict(zip(categories, listing_data))
        iphones_for_sale.append(listing_dict)
    all_df = pd.DataFrame(iphones_for_sale)
    
    new_df_64 = all_df[(all_df['storage'] == '64 GB') & (all_df['price'] < 550)].sort(columns=['price'])
    new_df_128 = all_df[(all_df['storage'] == '128 GB') & (all_df['price'] < 600)].sort(columns=['price'])
    

    new_item_64 = compare_df(new_df_64,iphone_64_gb_list)
    new_item_128 = compare_df(new_df_128,iphone_128_gb_list)

    iphone_64_gb_list = new_df_64
    iphone_128_gb_list = new_df_128

    for index,iphone in new_item_64.iterrows(): 
        # Notification
        notify(title    = 'New Iphone 64 GB - ' + str(iphone['price']),
               subtitle = '',
               message  = iphone['description'])
    for index,iphone in new_item_128.iterrows(): 
        # Notification
        notify(title    = 'New Iphone 64 GB - ' + str(iphone['price']),
               subtitle = '',
               message  = iphone['description'])    

if __name__ == '__main__':
    while True:
        listings = retrieve_page()
        listing_post(listings)
        sleep(randint(1,120))