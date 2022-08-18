from pyVinted import Vinted
from pyVinted.requester import requester
from bs4 import BeautifulSoup as BS
from lxml import etree as et
import json
import requests
import time
from datetime import datetime, date, timezone
import pytz
import maya


vinted = Vinted()
# search(url, number_of_items, page_number)
# newest_resp = vinted.items.search("https://www.vinted.pl/vetements?search_text=Smartwatch&order=newest_first", 20, i)

days = 86400 * 2


def get_newest():

    i = 1
    while i < 440:
        try:
            newest_resp = vinted.items.search("https://www.vinted.pl/vetements?search_text=&order=newest_first", 10, i)
            for item in newest_resp:
                check_items(item.url)
            # time.sleep(2)
            i += 1
        except:
            pass


def check_items(item):
    try:
        get_item = requester.get(str(item))
        item_soup = BS(get_item.text, "html.parser")
        item_json = item_soup.select_one('script[data-component-name="ItemViewItems"]').text

        res_jsn = json.loads(str(item_json))

        member_id = str(res_jsn['items'][1]['user']['id'])
        member_resp = requester.get(f'https://www.vinted.pl/api/v2/users/{str(member_id)}').text
        member_json = json.loads(str(member_resp))
        member_url = member_json['user']['profile_url']
        amount_member_items = member_json['user']['item_count']
        total_items_count = member_json['user']['total_items_count']
        positive_feedback = member_json['user']['positive_feedback_count']
        neutral_feedback = member_json['user']['neutral_feedback_count']
        negative_feedback = member_json['user']['negative_feedback_count']
        country = member_json['user']['country_code']
        created_at = maya.parse(member_json['user']['created_at']).datetime()
        last_loged = member_json['user']['last_loged_on_ts']

        print(member_id)

        if country == 'PL':
            if positive_feedback == 0 and  neutral_feedback == 0 and negative_feedback == 0:
                if ((datetime.now(pytz.utc) - created_at).total_seconds()) < days:
                    if amount_member_items < 7:
                        res = (f"""URL: {member_url}
                            Items: {total_items_count}
                            Was register:{created_at}
                            Country:{country}""")

                        print(res)
                        with open("result.txt", "a") as file:
                            file.write(res + '\n')


    except:
        pass


get_newest()


