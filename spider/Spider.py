# -*- coding: utf-8 -*-
import json
import logging
import os

import requests
import re
from bs4 import BeautifulSoup
import configparser

from spider.Model import TimeZone, ObjectEncoder, City, Country

logging.basicConfig(level=logging.INFO, filename='output.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

basic_url = u'https://24timezones.com'


class Spider(object):

    def __init__(self):
        self.base_url = u'https://24timezones.com'

    def get_time_zone_basic_info(self):
        soup = self.get_response_from_url(basic_url + '/shi_jie3.php')
        time_zone_table = soup.find('table', class_='dataTab1 genericBlock')
        time_zone_table_rows = time_zone_table.find_all('tr')
        time_zones = []
        for time_zone_table_row in time_zone_table_rows:
            time_zone_table_data = time_zone_table_row.find_all('td')
            if len(time_zone_table_data) > 0:
                time_zone = TimeZone()
                time_zone.code = time_zone_table_data[0].text.strip()
                time_zone.link = time_zone_table_data[0].a['href']
                time_zone.name = time_zone_table_data[1].text.strip()
                # print(time_zone.name)
                # print(json.dumps(time_zone.__dict__, ensure_ascii=False))
                time_zone = self.get_time_zone_detailed_info(time_zone)
                logging.info(json.dumps(time_zone.__dict__, ensure_ascii=False))
                time_zones.append(time_zone)
        print(json.dumps(time_zones, ensure_ascii=False, cls=ObjectEncoder))

    def get_time_zone_detailed_info(self, time_zone):
        time_zone_detailed_info_url = time_zone.link
        soup = self.get_response_from_url(basic_url + time_zone_detailed_info_url)
        time_zone_detailed_info_soup = soup.find('div', class_='dataBlock dBColor3')
        time_zone_detailed_info = time_zone_detailed_info_soup.find_all('div', class_='infoRow')
        time_zone_detailed_info_title = time_zone_detailed_info_soup.find_all('h3', class_='infoRowTitle')
        # print(time_zone_detailed_info)
        if len(time_zone_detailed_info) > 2 and len(time_zone_detailed_info_title) > 2:
            if time_zone.code + " " in time_zone_detailed_info_title[0].text:
                time_zone.description = time_zone_detailed_info[0].text.strip()
            if 'GMT' in time_zone_detailed_info_title[1].text:
                time_zone.offset_time = time_zone_detailed_info[1].text.strip().replace(" ", "")
        return time_zone

    def get_country_info(self):
        soup = self.get_response_from_url(basic_url + '/shi_jie2.php')
        country_time_zone_tables = soup.find_all('table', class_='dataTab1 genericBlock')
        country_list = []

        if len(country_time_zone_tables) == 2:
            for country_time_zone_table in country_time_zone_tables:

                country_time_zone_tr_list = country_time_zone_table.find_all('tr')
                for country_time_zone_tr in country_time_zone_tr_list:
                    country_link = country_time_zone_tr.find('a', class_='country_link')
                    if country_link is not None:
                        country = Country()
                        country.name = country_link.text
                        country.link = country_link['href']
                        country_soup = self.get_response_from_url(basic_url + country.link)
                        country.get_en_name_for_entity(country_soup)
                        # print(json.dumps(country.__dict__, ensure_ascii=False, cls=ObjectEncoder))
                        country.get_city_info_for_country(country_time_zone_tr.find_next_sibling())
                        country.get_detailed_info_for_country(country_soup)
                        if len(country.city) > 0:
                            for city in country.city:
                                city_soup = spider.get_response_from_url(basic_url + city.link)
                                city.get_en_name_for_entity(city_soup)
                                city.get_detailed_info_for_city(city_soup)
                        country_list.append(country)

        print(json.dumps(country_list, ensure_ascii=False, cls=ObjectEncoder))
        # print(json.dumps(country_list, ensure_ascii=False, cls=ObjectEncoder))

    @staticmethod
    def get_response_from_url(url):
        response = requests.get(url, headers=headers)
        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        else:
            print(response.status_code)


spider = Spider()
# spider.get_time_zone_basic_info()
# spider.get_country_info()
# city = City()
spider.get_time_zone_basic_info()
# city.link = '/zh_shi/tirana_shi_zhong.php'
# city.name = u"地拉那"

# city_soup = spider.get_response_from_url(basic_url + city.link)
# city.get_en_name_for_entity(city_soup)
# city.get_detailed_info_for_city(city_soup)
# print(json.dumps(city, ensure_ascii=False, cls=ObjectEncoder))
