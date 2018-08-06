# -*- encoding: utf-8 -*-
import logging
from datetime import datetime
from time import sleep
import calendar
from random import randint
import time
from selenium.common import exceptions
from appium.webdriver.common.touch_action import TouchAction

from Abracadabra.Device.MockDevice import MockDevice as Device

logging.basicConfig(level=logging.DEBUG)

DATE_FORMAT='%Y-%m-%d'


class FlowAgent(object):

    def __init__(self, profile):
        self._profile = profile

        if self._profile.get('device') == 'ios':
            # self.device = ios_agent
            self._ios = True
        else:
            self.device = Device()
            self._android = True

    def run_daka(self):

        user_name = self._profile.get('user_name')
        user_pwd = self._profile.get('user_pwd')
        start_date = datetime.strptime(self._profile.get('start_date'), DATE_FORMAT)
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day

        self.device.launch_app()
        if self._android:
            self.device.login(user_name, user_pwd)
        self.device.click_calendar()
        sleep(2)

        punch_in_btn_location, punch_out_btn_location = self.device.get_punch_btn_coordinates_in_calendar_view()

        self.device.switch_calendar_to_end_month()

        for datetime_data in FlowAgent._get_valid_duration(start_year, start_month, start_day):
            coordinate_of_days = self.get_all_day_btn_coordinates(datetime_data['year'], datetime_data['month'], start_year, start_date, start_day)
            for idx, day_btn_location in enumerate(coordinate_of_days):
                print(datetime_data['year'], datetime_data['month'], 'idx: %d' % idx)

                try:
                    # Choose date
                    print('Coordinate: %d %d' % (day_btn_location[0], day_btn_location[1]))
                    TouchAction(self.driver).tap(x=day_btn_location[0] + 20,
                                                 y=day_btn_location[1] + 20).perform()

                    # 上班
                    TouchAction(self.driver).tap(x=punch_in_btn_location[0] + 20,
                                                 y=punch_in_btn_location[1] + 20).perform()
                    # 非上班日 alert
                    sleep(0.5)
                    if not self.handle_alert(1.5):
                        self.device.punch(self.get_punch_in_time_hour, self.get_punch_in_time_minute)
                        sleep(1)

                    # 下班
                    TouchAction(self.driver).tap(x=punch_out_btn_location[0] + 20,
                                                 y=punch_out_btn_location[1] + 20).perform()

                    self.device.punch(self.get_punch_off_time_hour, self.get_punch_off_time_minute)
                    sleep(0.5)

                except exceptions.NoSuchElementException:
                    continue

            sleep(2)
            self.device.switch_calendar_to_previous_month()
            # punch all days start working time
            # punch all days end working time
            # self._device.select_previous_month()

    @classmethod
    def _get_valid_duration(self, START_YEAR, START_MONTH, START_DAY):
        now = datetime.now()
        if now <= datetime(self.END_YEAR, self.END_MONTH, self.END_DAY):
            self.END_YEAR = now.year
            self.END_MONTH = now.month
            self.END_DAY = now.day - 1  # Notice: 減一因為現在懶得處理今天還沒到下班時間不能打卡的狀況
        if now < datetime(START_YEAR, START_MONTH, START_DAY) or \
                datetime(START_YEAR, START_MONTH, START_DAY) > \
                datetime(self.END_YEAR, self.END_MONTH, self.END_DAY):
            raise Exception('Invalid datetime setting')

        valid_duration = []
        for year in reversed(range(START_YEAR, self.END_YEAR + 1)):
            for month in reversed(range(1, 13)):
                if year == self.END_YEAR and month > self.END_MONTH:
                    continue
                if year == START_YEAR and month < START_MONTH:
                    break
                valid_duration.append({'year': year, 'month': month})

        return valid_duration
    @classmethod
    def _compute_day_num(cls, year, month, end_date):
        if month == end_date.month:
            return end_date.day
        return calendar.monthrange(year, month)[1]

    def get_punch_in_time_hour(self):
        return '09'

    def get_punch_in_time_minute(self):
        return str(randint(0, 30)).rjust(2, '0')

    def get_punch_off_time_hour(self):
        return '18'

    def get_punch_off_time_minute(self):
        return str(randint(30, 59))

    def handle_alert(self, timeout_in_sec):
        start = time.time()
        while(True):
            if(time.time() - start > timeout_in_sec):
                break
            try:
                self.driver.switch_to.alert.accept()
                return True
            except:
                pass
        return False

    def get_punch_btn_coordinates_in_calendar_view(self):
        punch_in_btn = self.device.find_elements()
        punch_out_btn = self.device.find_elements()
        return (punch_in_btn.location['x'], punch_in_btn.location['y']), (punch_out_btn.location['x'], punch_out_btn.location['y'])

    def get_all_day_btn_coordinates(self, year, month, START_YEAR, START_MONTH, START_DAY):
        all_day_btns = self.device.find_elements()

        start_idx = 0
        end_idx = calendar.monthrange(year, month)[1] - 1

        if year == START_YEAR and month == START_MONTH:
            start_idx = START_DAY - 1
        if year == self.END_YEAR and month == self.END_MONTH:
            end_idx = self.END_DAY
        all_day_btns = all_day_btns[start_idx:end_idx]

        return [(x.location['x'], x.location['y']) for x in all_day_btns]


if __name__ == '__main__':

    agent = FlowAgent({
        'device': 'Android',
        'user_name': 'Mock',
        'user_pwd': 'mock',
        'start_date': '2018-08-05',
        'end_date': '2018-08-07'
    })

    agent.run_daka()
