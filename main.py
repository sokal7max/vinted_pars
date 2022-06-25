from pyVinted import Vinted
from pyVinted.requester import requester
from bs4 import BeautifulSoup as BS
from lxml import etree as et
import json
import requests


vinted = Vinted()

# search(url, number_of_items, page_number)
# items = vinted.items.search("https://www.vinted.pl/vetement?order=newest_first&price_to=60&currency=EUR",10,1)
items = vinted.items.search("https://www.vinted.pl/vetements?search_text=Smartwatch&order=newest_first", 10, 1)
# returns a list of objects: item

res = []

for item in items:
    res.append(item.url)



get_item = requester.get(res[2])
print(res[2])
item_soup = BS(get_item.text, "html.parser")
item_json = item_soup.select_one('script[data-component-name="ItemViewItems"]').text

res_jsn = json.loads(str(item_json))

member_url = str(res_jsn['items'][1]['user']['profile_url']) + ".html"

get_member = requester.get(member_url)
member_soup = BS(get_member.content, "html.parser")
member_items = member_soup.find_all('div', class_='feed-grid__item')

# f = open("demofile3.txt", "w")
# f.write(str(member_soup))
# f.close()

# class_='feed-grid__item feed-grid__item--one-fifth'

print(member_url)
# print(member_soup)


