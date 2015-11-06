import requests
from lxml import html
import os
from random import randint
from time import sleep

iphone_list = []

# The notifier function
def sendnotify(title, subtitle, message, link):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    u = '-open {!r}'.format(link)



    os.system('terminal-notifier {}'.format(' '.join([m, t, s, u])))

def notify(listing_dict):
    sendnotify(title = 'New Iphone 6+ in '+ listing_dict['condition']  + ' condition - $' + str(listing_dict['price']),
               subtitle = listing_dict['storage'],
               message  = listing_dict['color'],
               link = listing_dict['link'])    

def retrieve_page():
    # Change this URL to fetch other phones
    url = 'http://swappa.com/buy/apple-iphone-6-plus-unlocked/us'
    page = requests.get(url)
    tree = html.fromstring(page.text)
    listings = tree.xpath('//div[@id="listing_previews"]/div')
    return listings

def listing_post(listings):
    global iphone_list
    new_iphones_fetched = []
    categories = ['price','condition','listing_id','storage','color',
        'unknown','seller','location','country','description','link']
    for listing in listings:
        listing_text = listing.text_content().replace('\t','').split('\n')
        listing_data = [x for x in listing_text if x.strip()]
        listing_data[0] = int(listing_data[0].strip('$'))
        listing_data += ['http://swappa.com'+listing.xpath('@data-url')[0]]
        listing_dict = {}
        listing_dict = dict(zip(categories, listing_data))
        if not any(d[2] == listing_dict['listing_id'] for d in iphone_list):
            notify(listing_dict)
        new_iphones_fetched.append(listing_data)

    iphone_list = new_iphones_fetched

if __name__ == '__main__':
    while True:
        listings = retrieve_page()
        listing_post(listings)
        sleep(randint(1,120))