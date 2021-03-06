# -*- coding: utf-8 -*-
import logging
from appium import webdriver
from datetime import datetime
from appium.webdriver.common.touch_action import TouchAction

class AndriodDevice(object):

    def __init__(self):
        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'
        self.desired_caps['platformVersion'] = '7.0'
        #self.desired_caps['platformVersion'] = '8.0'
        self.desired_caps['deviceName'] = 'WUJ01N47TY'
        #self.desired_caps['deviceName'] = 'CB512BKD88'
        self.desired_caps['appPackage'] = 'com.cybersoft.had'
        self.desired_caps['appActivity'] = 'com.cybersoft.had.activity.MainActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.driver.implicitly_wait(10)

        self.first_day_index = None

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
        try:
            ok = self.driver.find_element_by_id('com.cybersoft.had:id/md_buttonDefaultPositive')
            ok.click()
        except:
            pass
        #TouchAction(self.driver).tap(x=1, y=1).perform()


    def punch(self, hour, minute):
        print(hour, minute)
        time_str = hour.zfill(2) + minute.zfill(2)
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


    def switch_calendar_to_last_month(self):
        print('switch_calendar_to_last_month')
        pre_page = self.driver.find_element_by_id('com.cybersoft.had:id/ibPrev')
        pre_page.click()
        self.first_day_index = None


    def back_page(self):
        print('back')
        self.driver.keyevent(4)


    def _find_xpath_of_day(self, day):

        def get_date_xpath(calender_index):
            return \
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.GridView/android.widget.LinearLayout[{calender_index}]/android.widget.LinearLayout/android.widget.TextView'.format(
                    calender_index=calender_index)
        if not self.first_day_index:
            calender_index = 0
            while True:
                calender_index += 1
                date_xpath = get_date_xpath(calender_index)
                first_day = self.driver.find_element_by_xpath(date_xpath)
                if first_day.text == '1':
                    self.first_day_index = calender_index
                    break
        target_day_index = self.first_day_index + day - 1
        return get_date_xpath(target_day_index)

    def click_on_work(self):
        sign_in = self.driver.find_element_by_id('com.cybersoft.had:id/btnOn')
        sign_in.click()


    def click_off_work(self):
        sign_in = self.driver.find_element_by_id('com.cybersoft.had:id/btnOff')
        sign_in.click()

    def switch_calendar_to_end_month(self, target_date):
        #month = driver.find_element_by_id('com.cybersoft.had:id/tvMonth')
        #month_year = datetime.strptime(month.text, "%B, %Y")
        current_date = datetime.now()
        month_diff = current_date.month - target_date.month
        last_page = self.driver.find_element_by_id('com.cybersoft.had:id/ibPrev')
        for i in range(month_diff):
            last_page.click()
        self.first_day_index = None

    def choose_date_from_calendar(self, day):
        day_xpath = self._find_xpath_of_day(day)
        self.driver.find_element_by_xpath(day_xpath).click()




class AndriodDriver(object):

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
