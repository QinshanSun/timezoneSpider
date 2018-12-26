# -*- coding: utf-8 -*-


class TimeZone(object):

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def set_description(self, description):
        setattr(self, "description", description)

    def get_description(self):
        getattr(self, "description")

    def set_country(self, country):
        setattr(self, "country", country)

    def get_country(self):
        getattr(self, "country")


class Country(object):

    def __init__(self, name):
        self.name = name

    def get_en_name(self):
        getattr(self, 'en_name')

    def set_en_name(self, name):
        setattr(self, 'en_name', name)
