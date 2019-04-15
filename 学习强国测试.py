"""
info:
author:Mrmeng
github:https://github.com/Mrmeng-bat/
update_time:2019-3-24
"""
import os
import subprocess
from appium import webdriver
import time
import numpy as np

all_of_text_list = np.load ("text_db.npy").tolist()
all_of_vod_list = np.load ("move_db.npy").tolist()



def init_driver():   #return desired_caps字典
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '5.1.1'
    desired_caps['deviceName'] = 'Nexus One'
    desired_caps['appPackage'] = 'cn.xuexi.android'
    desired_caps['appActivity'] = 'com.alibaba.android.rimet.biz.SplashActivity'
    desired_caps['noSign'] = True
    desired_caps['noReset'] = True
    desired_caps['newCommandTimeout'] = 3600
    return desired_caps

def swipe_y(driver): #x下滑动作
    y = driver.get_window_size()['height']
    driver.swipe(0, 5/10*y, 0, 2/10*y, 200)

def swipe_y2(driver): #x下滑动作
    y = driver.get_window_size()['height']
    for i in range(2):
        for j in range (30):
            driver.swipe(0, 3/10*y, 0, 2/10*y, 500)
            time.sleep (1)
def swipe_x(driver): #x下滑动作
    x = driver.get_window_size()['width']
    driver.swipe(2/10*x, 0, 6/10*x, 0, 200)
def move_to_index(driver): #转到我的学习
    driver.find_element_by_id("cn.xuexi.android:id/home_bottom_tab_icon_large").click()

def move_to_vod(driver):
    driver.find_element_by_xpath('//android.widget.TextView[@text="视频学习"]').click()

def move_to_my_study(driver):
    driver.find_element_by_xpath('//android.widget.TextView[@text="我的"]').click()

def move_to_shi_ping(driver):
    driver.find_element_by_id("cn.xuexi.android:id/home_bottom_tab_icon_large").click()
    driver.find_element_by_xpath('//android.widget.TextView[@text="时评"]').click()

def get_text_list(driver):   #返回未读文章列表
    text_list = []
    lists = driver.find_elements_by_class_name ('android.widget.TextView')
    for d_text in lists:
        if len(text_list) >6:
            break
        if len(d_text.text)<11:
            continue
        if d_text.text not in  all_of_text_list :
            all_of_text_list.append(d_text.text )
            text_list.append(d_text)
            print("找到未读文章：",d_text.text)
    return text_list

def get_vod_list(driver):   #返回未看视频列表
    vod_list = []
    lists = driver.find_elements_by_id('cn.xuexi.android:id/general_card_title_id')
    for d_vod in lists:
        if len(vod_list) >6:
            break
        if d_vod.text not in  all_of_vod_list:
            all_of_vod_list.append(d_vod.text )
            vod_list.append(d_vod )
            print("找到未看视频：",d_vod.text)
    return vod_list

def look_text(driver):
    lists=[]
    time.sleep(2)
    move_to_shi_ping(driver)
    time.sleep(2)
    while len(lists)<7:
        time.sleep(2)
        for_list = get_text_list(driver)
        for d_text in for_list:
            if len(lists)>6:
                break
            d_text.click()
            time.sleep(2)
            print('正在打开',d_text.text)
            swipe_y2(driver)
            time.sleep(30)
            lists.append(d_text.text)
            swipe_x(driver)
            time.sleep(2)
        swipe_y(driver)
    print("文章学习完成")
    
def look_vod(driver):
    lists=[]
    time.sleep(2)
    print("aaaa")
    move_to_vod(driver)
    time.sleep(2)
    while len(lists)<7:
        time.sleep(2)
        for_list = get_vod_list(driver)
        for d_text in for_list:
            if len(lists)>6:
                break
            d_text.click()
            time.sleep(2)
            print('正在打开',d_text.text)
            swipe_y(driver)
            time.sleep(240)
            lists.append(d_text.text)
            swipe_x(driver)
            time.sleep(2)
        swipe_y(driver)
    print("视频学习完成")
def print_log():
    print("等待任务执行")
def job():
    print('正在打开夜神模拟器')
    os.popen( r'E:\yeshen2\Nox\bin\NoxConsole.exe launch -name:夜神模拟器')#这里请更改为你电脑上夜神模拟器的位置
    time.sleep(60)
    print("正在打开appium")
    res = subprocess.Popen('appium', shell=True)
    time.sleep(5)
    driver = webdriver.Remote('http://localhost:4723/wd/hub', init_driver())
    time.sleep(20)
    look_text(driver)
    move_to_index(driver)
    look_vod(driver)
    driver.quit()
    print("任务完成关闭appium")
    os.popen ("taskkill /im /F node.exe")
    print("正在关闭夜神模拟器")
    os.popen (r"E:\yeshen2\Nox\bin\NoxConsole.exe quit -index:0 ")
    time.sleep(5)
    text_list = np.array (all_of_text_list)
    move_list = np.array (all_of_vod_list)
    np.save ('text_db.npy',text_list)
    np.save ('move_db.npy',move_list)
    
if __name__ == '__main__':
    job()
    
