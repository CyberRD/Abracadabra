# -*- encoding: utf-8 -*-
import logging
from datetime import datetime
from time import sleep
import calendar

DATE_FORMAT=''


class FlowAgent(object):

    def __init__(self, profile):
        self._profile = profile

        if self._profile.get('device') == 'ios':
            self.device = ios_agent
            self._ios = True
        else:
            self.device = android_agent
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

        valid_duration = self._get_valid_duration(start_date, end_date)

        for datetime_data in FlowAgent._get_valid_duration(start_date, end_date):
            for day in range(1, datetime_data['day'] + 1):
                logging.debug(datetime_data['year'], datetime_data['month'], day)

                try:
                    # Choose date
                    self.device.driver.find_element_by_xpath(
                        # '//XCUIElementTypeStaticText[@name="%d"]' % day).click()
                        self.device.loc.get(day)).click()
                    # 上班
                    self.device.driver.find_element_by_xpath(
                        '//XCUIElementTypeOther[@name="calendar"]/following-sibling::XCUIElementTypeButton[1]').click()
                    # 非上班日 alert
                    sleep(0.5)
                    self.handle_non_workday_alert()

                    self.punch(self.get_punch_in_time_hour, self.get_punch_in_time_minute)
                    # 下班
                    self.device.driver.find_element_by_xpath(
                        '//XCUIElementTypeOther[@name="calendar"]/following-sibling::XCUIElementTypeButton[2]').click()

                    self.punch(self.get_punch_off_time_hour, self.get_punch_off_time_minute)
                except exceptions.NoSuchElementException:
                    print("Some element not found when %d/%d/%d" % (datetime_data['year'], datetime_data['month'], day))

            sleep(2)
            self.switch_calendar_to_last_month()
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
            end_date.year = now.year
            end_date.month = now.month
            end_date.day = now.day - 1 # Notice: 減一因為現在懶得處理今天還沒到下班時間不能打卡的狀況
        if now < start_date or start_date > end_date:
            raise Exception('Invalid datetime setting')

        valid_duration = []
        for year in reversed(range(start_date.year, end_date.year + 1)):
            for month in reversed(range(1, 13)):
                if year == end_date.year and month > end_date.month:
                    continue
                if year == start_date.year and month < start_date.month:
                    break
                valid_duration.append({'year': year, 'month': month, 'day': FlowAgent._compute_day_num(year, month)})

        return valid_duration

    @classmethod
    def _compute_day_num(cls, year, month, end_date):
        if month == end_date.month:
            return end_date.day
        return calendar.monthrange(year, month)[1]
