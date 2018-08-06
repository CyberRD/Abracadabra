# -*- encoding: utf-8 -*-
import logging
from datetime import datetime
from time import sleep
import calendar
from random import randint

from selenium.common import exceptions

from Device.MockDevice import MockDevice as Device
from Device.Ios import IosDevice

logging.basicConfig(level=logging.DEBUG)

DATE_FORMAT='%Y-%m-%d'


class FlowAgent(object):

    def __init__(self, profile):
        self._profile = profile
        self._ios = False
        self._android = False

        if self._profile.get('device') == 'ios':
            self.device = IosDevice()
            self._ios = True
        else:
            self.device = Device()
            self._android = True

    def run_daka(self):

        user_name = self._profile.get('user_name')
        user_pwd = self._profile.get('user_pwd')
        start_date = datetime.strptime(self._profile.get('start_date'), DATE_FORMAT)
        end_date = datetime.strptime(self._profile.get('end_date'), DATE_FORMAT)

        self.device.launch_app()
        if self._android:
            self.device.login(user_name, user_pwd)
        self.device.click_calendar()

        # valid_duration = self._get_valid_duration(start_date, end_date)
        self.device.switch_calendar_to_end_month(end_date)

        for datetime_data in FlowAgent._get_valid_duration(start_date, end_date):
            for day in range(datetime_data['start_day'], datetime_data['end_day'] + 1):
                logging.debug(datetime_data['year'], datetime_data['month'], day)

                try:
                    # Choose date
                    self.device.choose_date_from_calendar(day)

                    # 上班
                    self.device.click_on_work()
                    # 非上班日 alert
                    sleep(0.5)
                    self.device.handle_non_workday_alert()
                    self.device.punch(self.get_punch_in_time_hour(), self.get_punch_in_time_minute())
                    self.device.back_page()

                    # 下班
                    self.device.click_off_work()
                    self.device.punch(self.get_punch_off_time_hour(), self.get_punch_off_time_minute())
                    self.device.back_page()

                except exceptions.NoSuchElementException:
                    print("Some element not found when %d/%d/%d" % (datetime_data['year'], datetime_data['month'], day))

            sleep(2)
            self.device.switch_calendar_to_previous_month()
            # punch all days start working time
            # punch all days end working time
            # self._device.select_previous_month()

    @classmethod
    def _get_valid_duration(sls, start_date, end_date):
        """

        :param start_date: datetime object with Y-M-D
        :param end_date: datetime object with Y-M-D
        :return:
        """

        now = datetime.now()
        # if now <= datetime(self.END_YEAR, self.END_MONTH, self.END_DAY):
        if now <= end_date:
            # end_date.year = now.year
            # end_date.month = now.month
            # end_date.day = now.day - 1 # Notice: 減一因為現在懶得處理今天還沒到下班時間不能打卡的狀況
            end_date = now
            logging.debug(end_date)
        if now < start_date or start_date > end_date:
            raise Exception('Invalid datetime setting')

        valid_duration = []
        for year in reversed(range(start_date.year, end_date.year + 1)):
            start_month = start_date.month if year == start_date.year else 1
            end_month = end_date.month if year == end_date.year else 12
            for month in reversed(range(start_month, end_month + 1)):
                if year == end_date.year and month == end_date.month:
                    end_day = end_date.day
                else:
                    end_day = calendar.monthrange(year, month)[1]
                if year == start_date.year and month == start_date.month:
                    start_day = start_date.day
                else:
                    start_day = 1
                valid_duration.append({'year': year,
                                       'month': month,
                                       'start_day': start_day,
                                       'end_day': end_day})


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


if __name__ == '__main__':

    agent = FlowAgent({
        'device': 'ios',
        'user_name': 'Mock',
        'user_pwd': 'mock',
        'start_date': '2018-02-01',
        'end_date': '2018-03-01'
    })

    agent.run_daka()
