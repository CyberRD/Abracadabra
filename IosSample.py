import unittest
import calendar
from LocateType import LocateType
from random import randint
from datetime import datetime
from appium import webdriver
from time import sleep
from appium.webdriver.common.touch_action import TouchAction
from selenium.common import exceptions

class AbrakadabraTests(unittest.TestCase):
    START_YEAR = 2018 # TODO: Should read start and end date from config and parse them separately
    START_MONTH = 1
    START_DAY = 1
    END_YEAR = 2018
    END_MONTH = 1
    END_DAY = 31
    is_punch_view_element_cached = False
    punch_view_loc = dict()

    def setUp(self):
        # set up appium
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                # TODO: Fill in
            })
        self.driver.implicitly_wait(3)
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
                valid_duration.append({'year': year, 'month': month})

        return valid_duration

    def test_punch(self):
        self.driver.execute_script('mobile: launchApp', {'bundleId': 'com.cybersoft.had.iDakaApp'})
        self.driver.execute_script('mobile: activateApp', {'bundleId': 'com.cybersoft.had.iDakaApp'});
        # Click calendar
        self.driver.find_element_by_accessibility_id("calendar icon").click()
        sleep(2)
        punch_in_btn_location, punch_out_btn_location = self.get_punch_btn_coordinates_in_calendar_view()
        self.switch_calendar_to_end_month()

        for datetime_data in self.valid_duration:
            coordinate_of_days = self.get_all_day_btn_coordinates(datetime_data['year'], datetime_data['month'])
            for idx, day_btn_location in enumerate(coordinate_of_days):
                print(datetime_data['year'], datetime_data['month'], 'idx: %d' % idx)
                try:
                    # Choose date
                    print('Coordinate: %d %d' % (day_btn_location[0], day_btn_location[1]))
                    TouchAction(self.driver).tap(x=day_btn_location[0]+20,
                                                 y=day_btn_location[1]+20).perform()
                    sleep(0.5)
                    # 上班
                    TouchAction(self.driver).tap(x=punch_in_btn_location[0] + 20,
                                                 y=punch_in_btn_location[1] + 20).perform()
                    sleep(0.5)
                    # 非上班日 alert
                    if not self.handle_alert():
                        self.punch_view_routine(self.get_punch_in_time_hour, self.get_punch_in_time_minute)
                        sleep(1)
                        # 下班
                        TouchAction(self.driver).tap(x=punch_out_btn_location[0] + 20,
                                                     y=punch_out_btn_location[1] + 20).perform()
                        self.punch_view_routine(self.get_punch_off_time_hour, self.get_punch_off_time_minute)
                    sleep(1)
                except exceptions.NoSuchElementException:
                    continue
            sleep(2)
            self.switch_calendar_to_previous_month()

    def get_punch_btn_coordinates_in_calendar_view(self):
        punch_in_btn = self.driver.find_element_by_xpath(
            '//XCUIElementTypeOther[@name="calendar"]/following-sibling::XCUIElementTypeButton[1]')
        punch_out_btn = self.driver.find_element_by_xpath(
            '//XCUIElementTypeOther[@name="calendar"]/following-sibling::XCUIElementTypeButton[2]')
        return (punch_in_btn.location['x'], punch_in_btn.location['y']), (punch_out_btn.location['x'], punch_out_btn.location['y'])

    def get_all_day_btn_coordinates(self, year, month):
        all_day_btns = self.driver.find_elements_by_xpath(
            '//XCUIElementTypeOther[@name="calendar"]/XCUIElementTypeOther[2]/XCUIElementTypeOther[4]/XCUIElementTypeCollectionView/descendant::XCUIElementTypeStaticText[string-length(@name) > 0]'
        )

        start_idx = 0
        end_idx = calendar.monthrange(year, month)[1] - 1

        if year == self.START_YEAR and month == self.START_MONTH:
            start_idx = self.START_DAY - 1
        if year == self.END_YEAR and month == self.END_MONTH:
            end_idx = self.END_DAY
        all_day_btns = all_day_btns[start_idx:end_idx]

        return [(x.location['x'], x.location['y']) for x in all_day_btns]

    def handle_alert(self):
        try:
            self.driver.find_element_by_accessibility_id("確定").click()
            return True
        except:
            return False

    def switch_calendar_to_end_month(self):
        now = datetime.now()
        for i in range(1, now.month - self.END_MONTH + 1):
            TouchAction(self.driver).press(x=74, y=320).wait(100).move_to(x=290, y=319).release().perform()

    def switch_calendar_to_previous_month(self):
        TouchAction(self.driver).press(x=74, y=320).wait(100).move_to(x=290, y=319).release().perform()

    def parse_date_field(self, date_field_value):
        date = date_field_value.split('月 ')
        month = date[0]
        year = date[1]
        return year, month

    def punch_view_routine(self, get_time_func_hour, get_time_func_min):
        # 點選時間
        sleep(0.5)
        clock_field_loc = self.get_punch_view_location('clock', LocateType.XPATH, '//XCUIElementTypeTextField[2]')
        TouchAction(self.driver).tap(x=clock_field_loc[0] + 10,
                                     y=clock_field_loc[1] + 10).perform()
        sleep(0.5)
        hour_wheel = self.driver.find_element_by_xpath(
            '//XCUIElementTypeApplication[@name=\"i-daka\"]/XCUIElementTypeWindow[4]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeDatePicker/XCUIElementTypeOther/XCUIElementTypePickerWheel[1]')
        hour_wheel.send_keys(get_time_func_hour())
        minute_wheel = self.driver.find_element_by_xpath(
            '//XCUIElementTypeApplication[@name=\"i-daka\"]/XCUIElementTypeWindow[4]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeDatePicker/XCUIElementTypeOther/XCUIElementTypePickerWheel[2]')
        minute_wheel.send_keys(get_time_func_min())
        sleep(0.5)
        # 完成選時間
        finish_time_btn_loc = self.get_punch_view_location('finish_time', LocateType.ACCESSIBILITY_ID, '完成')
        TouchAction(self.driver).tap(x=finish_time_btn_loc[0] + 5,
                                     y=finish_time_btn_loc[1] + 5).perform()
        sleep(0.5)
        punch_btn_loc = self.get_punch_view_location('punch', LocateType.ACCESSIBILITY_ID, '打卡')
        TouchAction(self.driver).tap(x=punch_btn_loc[0] + 5,
                                     y=punch_btn_loc[1] + 5).perform()
        # Alert 確定
        self.handle_alert()
        # 回前頁
        sleep(0.5)
        back_btn_loc = self.get_punch_view_location('back', LocateType.ACCESSIBILITY_ID, 'Back')
        TouchAction(self.driver).tap(x=back_btn_loc[0] + 5,
                                     y=back_btn_loc[1] + 5).perform()

    def get_punch_view_location(self, field_name, type, locator):
        if field_name not in self.punch_view_loc:
            if type == LocateType.XPATH:
                element = self.driver.find_element_by_xpath(locator)
            elif type == LocateType.ACCESSIBILITY_ID:
                element = self.driver.find_element_by_accessibility_id(locator)
            else:
                raise Exception("Unsupported locate type")
            self.punch_view_loc[field_name] = (element.location['x'], element.location['y'])
        return self.punch_view_loc[field_name]

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
