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

    def handle_non_workday_alert(self):
        print('handle_non_workday_alert')

    def punch(self, hour, minute):
        print(hour, minute)
        self.back_page()

    def switch_calendar_to_last_month(self):
        print('switch_calendar_to_last_month')

    def back_page(self):
        print('back')


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
