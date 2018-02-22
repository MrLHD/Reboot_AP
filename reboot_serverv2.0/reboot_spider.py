import os
import time
from selenium import webdriver
from  selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_NAME = 'super'
USER_PWD = 'gaosiedu.com'
PATH = os.getcwd()
browser = webdriver.Chrome()
web_wait = WebDriverWait(browser,10)

#加载ip列表
def GET_Ip():
    path = PATH+'\\ip_list.txt'
    with open(path,'r') as file:
        for ip in file.readlines():
            ip = ip.strip()
            reboot_spiders(ip)

#重启方法
def reboot_spiders(ip_arg):
    if len(ip_arg) > 0:
        try:
            browser.get("https://{IP}/login.asp".format(IP=ip_arg))

            # 获取用户名输入框
            login_name = web_wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="login-username"]')))
            # 获取输入密码的输入框
            login_pwd = web_wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="password"]')))
            #获取登录的按钮
            button = web_wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="loginform"]/input')))
            #在输入用户名的位置输入用户名
            login_name.send_keys(USER_NAME)
            #在输入密码的输入框输入密码
            login_pwd.send_keys(USER_PWD)
            #点击登录按钮
            button.click()
            #分析已经登录的页面
            #登录成功，开始分析页面!
            #找到第一个frame标签（左侧栏）
            browser.switch_to.frame("navframe")
            #切换进去，执行Reboot Now这个按钮，
            reboot_bo = web_wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/dl[3]/dd/ul/li[2]/a')))
            #执行操作，得到右边Reboot Now的重启按钮
            reboot_bo.click()
            #跳出当前的frame标签
            browser.switch_to.default_content()
            #找到执行完后右边的frame标签
            browser.switch_to.frame('mainframe')
            #进入标签后找到重启的按钮
            reboot_boot = web_wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="adminform"]/table/tbody/tr[1]/td/input[2]')))
            #执行重启的操作
            reboot_boot.click()
            #关闭浏览器
            #完成后关闭
            timee = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            s_log = "时间 %s  ip地址[%s]重启成功" %(timee,ip_arg)
            Success_log(s_log)
        except Exception as e:
            timeee = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            r_log = "时间 %s  ip地址[%s]重启失败" %(timeee,ip_arg)
            Error_log(r_log)
    else:
        pass

def Error_log(args):
    path = PATH+'\\error.txt'
    with open(path, 'a+', encoding='utf-8') as file:
        file.write('\n%s'%args)
        file.close()

def Success_log(args):
    path = PATH+'\\success.txt'
    with open(path,'a+',encoding='utf-8') as file:
        file.write('\n%s'%args)
        file.close()

if __name__ == '__main__':
    GET_Ip()
    browser.quit()
