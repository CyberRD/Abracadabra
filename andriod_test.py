import unittest
from appium import webdriver
from time import sleep
from datetime import datetime
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.0'
#desired_caps['platformVersion'] = '8.0'
desired_caps['deviceName'] = 'WUJ01N47TY'
#desired_caps['deviceName'] = 'CB512BKD88'
desired_caps['appPackage'] = 'com.cybersoft.had'
desired_caps['appActivity'] = 'com.cybersoft.had.activity.MainActivity'
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(10)
def login():
    account = driver.find_element_by_id('com.cybersoft.had:id/etAccount')
    account.send_keys('edwardwu')
    driver.keyevent(4)
    password = driver.find_element_by_id('com.cybersoft.had:id/etPassword')
    password.send_keys('c6f6ohKK#')
    driver.keyevent(4)
    login = driver.find_element_by_id('com.cybersoft.had:id/btnLogin')
    login.click()
    sleep(3)
    calender = driver.find_element_by_id('com.cybersoft.had:id/ivCalendar')
    calender.click()

def back():
    driver.keyevent(4)

def find_xpath_of_day(day):
    def get_date_xpath(calender_index):
        return \
    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.GridView/android.widget.LinearLayout[{calender_index}]/android.widget.LinearLayout/android.widget.TextView'.format(calender_index=calender_index)
    calender_index = 0
    while True:
        calender_index += 1
        date_xpath = get_date_xpath(calender_index)
        first_day = driver.find_element_by_xpath(date_xpath)
        if first_day.text == '1':
            first_day_index = calender_index
            break
    target_day_index = first_day_index + day - 1
    return get_date_xpath(target_day_index)

def switch_month(target_date):
    month = driver.find_element_by_id('com.cybersoft.had:id/tvMonth')
    month_year = datetime.strptime(month.text, "%B, %Y")
    month_diff = month_year.month - target_date.month
    pre_page = driver.find_element_by_id('com.cybersoft.had:id/ibPrev')
    for i in range(month_diff):
        pre_page.click()

def go_to_work_page():
    sign_in = driver.find_element_by_id('com.cybersoft.had:id/btnOn')
    sign_in.click()

def get_off_work_page():
    sign_in = driver.find_element_by_id('com.cybersoft.had:id/btnOff')
    sign_in.click()

def punch(time_str):
    clock = driver.find_element_by_id('com.cybersoft.had:id/btnClock')
    clock.click()
    clock_setting = driver.find_element_by_id('com.cybersoft.had:id/hours')
    clock_setting.send_keys(time_str)
    ok = driver.find_element_by_id('com.cybersoft.had:id/ok')
    ok.click()
    try:
        confirm = \
        driver.find_element_by_id('com.cybersoft.had:id/btnClockInConfirm')
    except:
        confirm = \
        driver.find_element_by_id('com.cybersoft.had:id/btnClockOutConfirm')
    confirm.click()
    ok = \
    driver.find_element_by_id('com.cybersoft.had:id/md_buttonDefaultPositive')
    ok.click()




def get_pagesize():
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        return (x, y)

def swipe_left():
      s = get_pagesize()
      import pdb;pdb.set_trace() 
      sx = s[0] * 0.95
      sy = s[1] * 0.7
      ex = s[0] * 0.10
      ey = sy
      driver.swipe(sx, sy, ex, ey)
login()
go_to_work_page()
punch('8:30')
back()
get_off_work_page()
punch('17:40')
back()
#switch_month(datetime(2015,5,13,12,0,0))
#find_xpath_of_day(6)
