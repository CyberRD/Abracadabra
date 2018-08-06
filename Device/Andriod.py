# -*- coding: utf-8 -*-
import logging
from appium import webdriver

class AndriodDevice(object):

    def __init__(self):
        self.driver = AndriodDriver().driver

    def launch_app(self):
        print('launch_app')

    def login(self, user_name, user_pwd):
        print(user_name, user_pwd)
        account = self.driver.find_element_by_id('com.cybersoft.had:id/etAccount')
        account.send_keys(user_name)
        self.back_page()
        password = self.driver.find_element_by_id('com.cybersoft.had:id/etPassword')
        password.send_keys(user_pwd)
        self.back_page()
        login = self.driver.find_element_by_id('com.cybersoft.had:id/btnLogin')
        login.click()


    def click_calendar(self):
        print('click_calendar')
        calender = self.driver.find_element_by_id('com.cybersoft.had:id/ivCalendar')
        calender.click()

    def handle_non_workday_alert(self):
        print('handle_non_workday_alert')

    def punch(self, hour, minute):
        print(hour, minute)
        clock = self.driver.find_element_by_id('com.cybersoft.had:id/btnClock')
        clock.click()
        clock_setting = self.driver.find_element_by_id('com.cybersoft.had:id/hours')
        clock_setting.send_keys(time_str)
        ok = self.driver.find_element_by_id('com.cybersoft.had:id/ok')
        ok.click()
        try:
            confirm = \
                self.driver.find_element_by_id('com.cybersoft.had:id/btnClockInConfirm')
        except:
            confirm = \
                self.driver.find_element_by_id('com.cybersoft.had:id/btnClockOutConfirm')
        confirm.click()
        ok = \
            self.driver.find_element_by_id('com.cybersoft.had:id/md_buttonDefaultPositive')
        ok.click()
        self.back_page()

    def switch_calendar_to_last_month(self):
        print('switch_calendar_to_last_month')

    def back_page(self):
        print('back')
        self.driver.keyevent(4)


class AndriodDriver(object):

    def __init__(self):
        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'
        self.desired_caps['platformVersion'] = '7.0'
        # desired_caps['platformVersion'] = '8.0'
        self.desired_caps['deviceName'] = 'WUJ01N47TY'
        # desired_caps['deviceName'] = 'CB512BKD88'
        self.desired_caps['appPackage'] = 'com.cybersoft.had'
        self.desired_caps['appActivity'] = 'com.cybersoft.had.activity.MainActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.driver.implicitly_wait(10)

    @classmethod
    def find_element_by_xpath(cls, path):
        print('find "%s"' % path)
        return cls

    @classmethod
    def click(cls):
        print('Click()')
        return cls
