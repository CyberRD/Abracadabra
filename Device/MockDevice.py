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

    def click_on_work(self):
        print('click on work')

    def click_off_work(self):
        print('click_off_work')

    def switch_calendar_to_previous_month(self):
        print('switch_calendar_to_last_month')

    def switch_calendar_to_end_month(self):
        print('switch_calendar_to_end_month')

    def back_page(self):
        print('back')

    def choose_date_from_calendar(self, day):
        pass


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
