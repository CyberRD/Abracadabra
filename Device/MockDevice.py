# -*- coding: utf-8 -*-
import logging


class MockDevice(object):

    def __init__(self):
        self.driver = MockDriver()

    def launch_app(self):
        print('launch_app')

    def login(self, user_name, user_pwd):
        print(user_name, user_pwd)

    def click_calendar(self):
        print('click_calendar')

    def punch(self, hour, minute):
        print(hour, minute)
        self.back_page()

    def switch_calendar_to_end_month(self):
        print('switch_calendar_to_last_month')

    def switch_calendar_to_previous_month(self):
        print('switch_calnedar_to_previous_month')

    def back_page(self):
        print('back')

    def get_all_day_btn_coordinates(self, year, month):
        print('get_all_day_btn_coordinates')

    def punch_view_routine(self, get_time_func_hour, get_time_func_min):
        print('punch_view_routine')

    def find_elements(self):
        print('find elements')

class MockDriver(object):

    def __init__(self):
        pass

    @classmethod
    def find_element_by_xpath(cls, path):
        print('find "%s"' % path)
        return cls

    @classmethod
    def click(cls):
        print('Click()')
        return cls
