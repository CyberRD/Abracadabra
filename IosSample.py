import unittest
import os
import calendar
from random import randint
from datetime import datetime
from appium import webdriver
from time import sleep
from appium.webdriver.common.touch_action import TouchAction
from selenium.common import exceptions

class IOSLib():
    def setup(self):
        print('setup')

class AbrakadabraTests(unittest.TestCase):
    START_YEAR = 2018 # TODO: Should read start and end date from config and parse them separately
    START_MONTH = 1
    START_DAY = 1
    END_YEAR = 2018
    END_MONTH = 8
    END_DAY = 1

    def setUp(self):
        # set up appium
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',

        self.driver.implicitly_wait(10)
        self.valid_duration = self.handle_punch_duration_setting()

    def tearDown(self):
        self.driver.quit()

    def handle_punch_duration_setting(self):
        now = datetime.now()
        if now <= datetime(self.END_YEAR, self.END_MONTH, self.END_DAY):
            self.END_YEAR = now.year
            self.END_MONTH = now.month
            self.END_DAY = now.day - 1 # Notice: 減一因為現在懶得處理今天還沒到下班時間不能打卡的狀況
        if now < datetime(self.START_YEAR, self.START_MONTH, self.START_DAY) or \
                datetime(self.START_YEAR, self.START_MONTH, self.START_DAY) > \
                datetime(self.END_YEAR, self.END_MONTH, self.END_DAY):
            raise Exception('Invalid datetime setting')

        valid_duration = []
        for year in reversed(range(self.START_YEAR, self.END_YEAR + 1)):
            for month in reversed(range(1, 13)):
                if year == self.END_YEAR and month > self.END_MONTH:
                    continue
                if year == self.START_YEAR and month < self.START_MONTH:
                    break
                valid_duration.append({'year': year, 'month': month, 'day': self.compute_day_num(year, month)})

        return valid_duration

    def test_punch(self):
        self.driver.execute_script('mobile: launchApp', {'bundleId': 'com.cybersoft.had.iDakaApp'})
        self.driver.execute_script('mobile: activateApp', {'bundleId': 'com.cybersoft.had.iDakaApp'});

        # Click calendar
        self.driver.find_element_by_accessibility_id("calendar icon").click()
        sleep(2)
        self.switch_calendar_to_end_month()

        for datetime_data in self.valid_duration:
            for day in range(1, datetime_data['day'] + 1):
                print(datetime_data['year'], datetime_data['month'], day)
                try:
                    # Choose date
                    self.driver.find_element_by_xpath(
                        '//XCUIElementTypeStaticText[@name="%d"]' % day).click()
                    # 上班
                    self.driver.find_element_by_xpath(
                        '//XCUIElementTypeOther[@name="calendar"]/following-sibling::XCUIElementTypeButton[1]').click()
                    # 非上班日 alert
                    sleep(0.5)
                    self.handle_non_workday_alert()

                    self.punch(self.get_punch_in_time_hour, self.get_punch_in_time_minute)
                    # 下班
                    self.driver.find_element_by_xpath(
                        '//XCUIElementTypeOther[@name="calendar"]/following-sibling::XCUIElementTypeButton[2]').click()

                    self.punch(self.get_punch_off_time_hour, self.get_punch_off_time_minute)
                except exceptions.NoSuchElementException:
                    print("Some element not found when %d/%d/%d" % (datetime_data['year'], datetime_data['month'], day))

            sleep(2)
            self.switch_calendar_to_last_month()

    def handle_non_workday_alert(self):
        try:
            self.driver.switch_to.alert.accept()
        except:
            return

    def switch_calendar_to_end_month(self):
        now = datetime.now()
        for i in range(1, now.month - self.END_MONTH + 1):
            TouchAction(self.driver).press(x=74, y=320).wait(100).move_to(x=290, y=319).release().perform()

    def compute_day_num(self, year, month):
        if month == self.END_MONTH:
            return self.END_DAY
        return calendar.monthrange(year, month)[1]

    def switch_calendar_to_last_month(self):
        TouchAction(self.driver).press(x=74, y=320).wait(100).move_to(x=290, y=319).release().perform()

    def parse_date_field(self, date_field_value):
        date = date_field_value.split('月 ')
        month = date[0]
        year = date[1]
        return year, month

    def punch(self, get_time_func_hour, get_time_func_min):
        time_field = self.driver.find_element_by_xpath('//XCUIElementTypeTextField[2]')
        time_field.click()
        hour_wheel = self.driver.find_element_by_xpath(
            '//XCUIElementTypeApplication[@name=\"i-daka\"]/XCUIElementTypeWindow[4]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeDatePicker/XCUIElementTypeOther/XCUIElementTypePickerWheel[1]')
        hour_wheel.send_keys(get_time_func_hour())
        minute_wheel = self.driver.find_element_by_xpath(
            '//XCUIElementTypeApplication[@name=\"i-daka\"]/XCUIElementTypeWindow[4]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeDatePicker/XCUIElementTypeOther/XCUIElementTypePickerWheel[2]')
        minute_wheel.send_keys(get_time_func_min())
        # 完成選時間
        self.driver.find_element_by_accessibility_id("完成").click()
        # 打卡
        self.driver.find_element_by_accessibility_id("打卡").click()
        # Alert 確定
        #self.handle_non_workday_alert()
        self.driver.find_element_by_accessibility_id("確定").click()
        # 回前頁
        self.driver.find_element_by_accessibility_id("Back").click()


    def get_punch_in_time_hour(self):
        return '09'

    def get_punch_in_time_minute(self):
        return str(randint(0, 30)).rjust(2, '0')

    def get_punch_off_time_hour(self):
        return '18'

    def get_punch_off_time_minute(self):
        return str(randint(30, 59))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AbrakadabraTests)
    unittest.TextTestRunner(verbosity=2).run(suite)