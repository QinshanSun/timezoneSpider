# -*- coding: utf-8 -*-

import json
import re


class TimeZone(object):
    __attrs__ = ['description', 'country', 'code', 'name', 'link', 'utc_timezone']

    def __init__(self):
        self.code = None
        self.name = None
        self.description = None
        self.country = []
        self.link = None
        self.utc_timezone = None


class Entity(object):
    __attrs__ = ['en_name', 'name', 'link']

    def __init__(self):
        self.name = None
        self.en_name = None
        self.link = None

    def get_en_name_for_entity(self, soup):
        en_name_soup = soup.find('h2')
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        re.findall(p1, en_name_soup.text.strip())
        print(en_name_soup.text.strip())
        print(re.findall(p1, en_name_soup.text.strip()))
        en_name_list = re.findall(p1, en_name_soup.text.strip())
        if len(en_name_list) > 0:
            self.en_name = en_name_list[0]


class Country(Entity):
    __attrs__ = ['en_name', 'name', 'city', 'link', 'summer_time', 'is_summer_time', 'utc_timezone']

    def __init__(self):
        super().__init__()
        self.city = []
        self.is_summer_time = None
        self.utc_timezone = None
        self.summer_time = None

    def get_city_info_for_country(self, soup):
        city_list = []
        city_time_zone_td = soup.find('td', class_='col-c1')
        if city_time_zone_td is not None and len(city_time_zone_td) > 0:
            city_link_list = city_time_zone_td.find_all('a')
            for city_link in city_link_list:
                city = City()
                city.name = city_link.text
                city.link = city_link['href']
                city_list.append(city)
                # print(json.dumps(city.__dict__, ensure_ascii=False, cls=ObjectEncoder))
        self.city = city_list
        print(json.dumps(self.__dict__, ensure_ascii=False, cls=ObjectEncoder))
        # country_list.append(json.dumps(country.__dict__, ensure_ascii=False, cls=ObjectEncoder))

    def get_detailed_info_for_country(self, soup):
        data_block_soup = soup.find('div', class_='dataBlock dBColor3')
        city_detailed_info_list = data_block_soup.find_all('div', class_='infoRow')
        city_detailed_info_title_list = data_block_soup.find_all('h3', class_='infoRowTitle')
        if len(city_detailed_info_list) > 0 and len(city_detailed_info_title_list) > 0:
            for index in range(len(city_detailed_info_title_list)):
                if 'GMT' in city_detailed_info_title_list[index].text:
                    # print(city_detailed_info_list[index].text)
                    # print(city_detailed_info_list[index].text.strip().replace(" ", ""))
                    city_offset_time_td = city_detailed_info_list[index].find_all('td')
                    if len(city_offset_time_td) > 0:
                        self.utc_timezone = city_offset_time_td[0].text.strip().replace(" ", "")
                    if len(city_offset_time_td) > 1:
                        self.is_summer_time = city_offset_time_td[1].text.strip().replace(" ", "")

                if '夏令时' in city_detailed_info_title_list[index].text:
                    print(city_detailed_info_list[index].text.strip().replace(" ", ""))
                    self.summer_time = city_detailed_info_list[index].text.strip().replace(" ", "")


class City(Entity):
    __attrs__ = ['en_name', 'name', 'link', 'summer_time', 'longitude', 'latitude', 'is_summer_time', 'utc_timezone']

    def __init__(self):
        super().__init__()
        self.summer_time = None
        self.longitude = None
        self.latitude = None
        self.is_summer_time = None
        self.utc_timezone = None

    def get_detailed_info_for_city(self, soup):
        data_block_soup = soup.find('div', class_='dataBlock dBColor3')
        city_detailed_info_list = data_block_soup.find_all('div', class_='infoRow')
        city_detailed_info_title_list = data_block_soup.find_all('h3', class_='infoRowTitle')
        if len(city_detailed_info_list) > 0 and len(city_detailed_info_title_list) > 0:
            for index in range(len(city_detailed_info_title_list)):
                if 'GMT' in city_detailed_info_title_list[index].text:
                    # print(city_detailed_info_list[index].text)
                    # print(city_detailed_info_list[index].text.strip().replace(" ", ""))
                    city_offset_time_td = city_detailed_info_list[index].find_all('td')
                    if len(city_offset_time_td) > 0:
                        self.utc_timezone = city_offset_time_td[0].text.strip().replace(" ", "")
                    if len(city_offset_time_td) > 1:
                        self.is_summer_time = city_offset_time_td[1].text.strip().replace(" ", "")

                if '夏令时' in city_detailed_info_title_list[index].text:
                    print(city_detailed_info_list[index].text.strip().replace(" ", ""))
                    self.summer_time = city_detailed_info_list[index].text.strip().replace(" ", "")

                if '地理坐标' in city_detailed_info_title_list[index].text:
                    # print(city_detailed_info_list[index].text.strip().replace(" ", ""))
                    city_location_td_list = city_detailed_info_list[index].find_all('td')
                    if len(city_location_td_list) > 0:
                        self.latitude = city_location_td_list[0].text.strip().replace(" ", "")
                    if len(city_location_td_list) > 1:
                        self.longitude = city_location_td_list[1].text.strip().replace(" ", "")


class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (TimeZone, City, Country)):
            return json.dumps(obj.__dict__, ensure_ascii=False, default=lambda o: o.__dict__,
                              sort_keys=True)
        return json.JSONEncoder.default(self, obj)
