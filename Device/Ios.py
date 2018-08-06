# -*- encoding: utf-8 -*-
from datetime import datetime
from appium import webdriver
from time import sleep
from appium.webdriver.common.touch_action import TouchAction

class IosDevice():
    def launch_app(self):
        self.setUp()
        self.driver.execute_script('mobile: launchApp', {'bundleId': 'com.cybersoft.had.iDakaApp'})
        self.driver.execute_script('mobile: activateApp', {'bundleId': 'com.cybersoft.had.iDakaApp'})

    def setUp(self):
        # set up appium
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': 'com.cybersoft.had.iDakaApp',
                'platformName': 'iOS',
                'platformVersion': '11.4',
                'deviceName': 'iPhone 8',
                'xcodeOrgId': '',
                'xcodeSigningId': 'iPhone Developer',
                'udid': '',
                'showXcodeLog': True,
                'updatedWDABundleId': 'com.cybersoft.had.iDakaApp'
            })
        self.driver.implicitly_wait(3)

    def click_calendar(self):
        self.driver.find_element_by_accessibility_id("calendar icon").click()

    def switch_calendar_to_end_month(self, end_date):
        sleep(3)
        now = datetime.now()
        end_month = end_date.month
        for i in range(0, now.month - end_month):
            TouchAction(self.driver).press(x=74, y=320).wait(100).move_to(x=290, y=319).release().perform()

    def choose_date_from_calendar(self, day):
        self.driver.find_element_by_xpath(
            '//XCUIElementTypeStaticText[@name="%d"]' % day).click()

    def click_on_work(self):
        self.driver.find_element_by_xpath(
            '//XCUIElementTypeOther[@name="calendar"]/following-sibling::XCUIElementTypeButton[1]').click()

    def punch(self, punch_time_hour, punch_time_minute):
        time_field = self.driver.find_element_by_xpath('//XCUIElementTypeTextField[2]')
        time_field.click()
        hour_wheel = self.driver.find_element_by_xpath(
            '//XCUIElementTypeApplication[@name=\"i-daka\"]/XCUIElementTypeWindow[4]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeDatePicker/XCUIElementTypeOther/XCUIElementTypePickerWheel[1]')
        hour_wheel.send_keys(punch_time_hour)
        minute_wheel = self.driver.find_element_by_xpath(
            '//XCUIElementTypeApplication[@name=\"i-daka\"]/XCUIElementTypeWindow[4]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeDatePicker/XCUIElementTypeOther/XCUIElementTypePickerWheel[2]')
        minute_wheel.send_keys(punch_time_minute)
        # 完成選時間
        self.driver.find_element_by_accessibility_id("完成").click()
        # 打卡
        self.driver.find_element_by_accessibility_id("打卡").click()
        # Alert 確定
        self.driver.find_element_by_accessibility_id("確定").click()

    def back_page(self):
        self.driver.find_element_by_accessibility_id("Back").click()

    def handle_non_workday_alert(self):
        try:
            self.driver.switch_to.alert.accept()
        except:
            return

    def click_off_work(self):
        self.driver.find_element_by_xpath(
            '//XCUIElementTypeOther[@name="calendar"]/following-sibling::XCUIElementTypeButton[2]').click()

    def switch_calendar_to_previous_month(self):
        TouchAction(self.driver).press(x=74, y=320).wait(200).move_to(x=290, y=319).release().perform()
