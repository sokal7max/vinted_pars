from pyVinted import Vinted
from pyVinted.requester import requester
from bs4 import BeautifulSoup as BS
from lxml import etree as et
import json
import requests
import time


vinted = Vinted()
# search(url, number_of_items, page_number)

# newest_resp = vinted.items.search("https://www.vinted.pl/vetements?search_text=Smartwatch&order=newest_first", 20, i)

newest = []
low_rate_members = []


def get_newest():

    i = 1
    while i < 80:
        try:
            newest_resp = vinted.items.search("https://www.vinted.pl/vetements?search_text=&order=newest_first", 10, i)
            for item in newest_resp:
                newest.append(item.url)
            time.sleep(3)
            i += 1
            print("get newest", len(newest))
        except:
            pass


def check_items():
    for item in newest:
        try:
            get_item = requester.get(str(item))
            item_soup = BS(get_item.text, "html.parser")
            item_json = item_soup.select_one('script[data-component-name="ItemViewItems"]').text

            res_jsn = json.loads(str(item_json))

            member_url = res_jsn['items'][1]['user']['profile_url']
            member_id = str(res_jsn['items'][1]['user']['id'])

            get_member = requester.get(member_url)
            member_items_resp = requester.get(f'https://www.vinted.pl/api/v2/users/{str(member_id)}/items?page=1&per_page=20&order=relevance&currency=PLN').text
            member_items_jsn = json.loads(str(member_items_resp))
            amount_member_items = member_items_jsn['pagination']['total_entries']

            if amount_member_items <= 3:
                # low_rate_members.append(member_url)
                with open("result.txt", "w") as file:
                    file.write(member_url + '\n')
            time.sleep(2)
            print("check rate", newest.index(item))

        except:
            pass


get_newest()
check_items()

print(low_rate_members)

# print(len(newest))
# print(amount_member_items)


