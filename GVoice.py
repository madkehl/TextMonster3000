from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import sys

urlDummy = "https://www.poshmark.com"
urlVoice = "https://voice.google.com/about"



def hack_openVoice(OS = 'MAC'):
    options = Options()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(chrome_options = options)
    driver.get(urlDummy)
    time.sleep(3)
    ggl_btn = driver.find_element_by_css_selector('#content > div > div.homepage__hero--desktop > div > div.homepage__hero__text.homepage__hero__text--desktop > div > div > form:nth-child(3) > div > div > span')
    ggl_btn.click()
    
    print('PLEASE LOGIN IN BROWSER')
    key_pressed = input('Press ENTER to continue: ')
    time.sleep(1)
    
    
    body = driver.find_element_by_tag_name("body")
    
    driver.execute_script("window.open('" + urlVoice + "');")
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    time.sleep(3)
    signin_btn = driver.find_element_by_css_selector("#header > div.headerItem.headerRight > a.signUpLink")
    signin_btn.click()
    
    time.sleep(5)
    
    return(driver)
    
def send_texts(driver, phone2text, d1, OS = 'WINDOWS'):
    messages_btn = driver.find_element_by_css_selector('#gvPageRoot > div.gv_root.layout-column.flex > div.layout-row.flex > gv-side-nav > div > div > gmat-nav-list > a:nth-child(2) > div > div > mat-icon > svg')
    messages_btn.click()
    try:
        send_new_msg = driver.find_element_by_css_selector('#messaging-view > div > md-content > div > div > div > div.GYQtq-mpvPNd.flex-none > mat-icon > svg')
        send_new_msg.click()
    except:
        time.sleep(4)
        send_new_msg = driver.find_element_by_css_selector('#messaging-view > div > md-content > div > div > div > div.GYQtq-mpvPNd.flex-none > mat-icon > svg')
        send_new_msg.click()
        
    for i in phone2text.index:
        try:
            print(phone2text.loc[i]['phone'])
            phone_numbers = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/gv-messaging-view/div/div/md-content/gv-thread-details/div/div[1]/gv-recipient-picker/div/md-content/gv-recipient-picker-chips-ng2/mat-chip-list/div/md-input-container/input')
            phone_numbers.click()
            time.sleep(1)
            phone_numbers.send_keys(str(int(phone2text.loc[i]['phone'])))
            time.sleep(3)
            
            phone_numbers.send_keys(Keys.RETURN)

            try:
                text_msg = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/gv-messaging-view/div/div/md-content/gv-thread-details/div/div[2]/gv-message-entry/div/div[2]/md-input-container/textarea')
                text_msg.click()
            except:
                time.sleep(3)
                text_msg = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/gv-messaging-view/div/div/md-content/gv-thread-details/div/div[2]/gv-message-entry/div/div[2]/md-input-container/textarea')
                text_msg.click()
            time.sleep(1)
            text_msg.send_keys(phone2text.loc[i][d1])
            

            text_msg.send_keys(Keys.RETURN)
            time.sleep(2)
            send_new_msg.click()
        else:
            print("NUMBER MISSING")
        
        
    
    print('PLEASE LOGIN IN BROWSER')
    key_pressed = input('Press ENTER to continue: ')
    
    
#won't work with our MFA, use hack fctn
def openGVoice(my_email, my_passw, OS = 'MAC'):

    '''
    INPUT: str formatted username and password for MetricWire account

    OUTPUT: driver for next function, simply opens in a test browser
    '''
    driver = webdriver.Chrome()
    driver.get(urlVoice)

    time.sleep(3)
    signin_btn = driver.find_element_by_css_selector("#header > div.headerItem.headerRight > a.signUpLink")
    signin_btn.click()
    
    email_inp = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")
    
    email_inp.send_keys(my_email)
    
    hit_next = driver.find_element_by_css_selector("#identifierNext > div > button > div.VfPpkd-RLmnJb")
    hit_next.click()
    time.sleep(2)
    try:
        pass_inp = driver.find_element_by_css_selector("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
        pass_inp.send_keys(my_passw)
    except:
        driver.refresh()
        email_inp = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")
        
        email_inp.send_keys(my_email)
        hit_next = driver.find_element_by_css_selector("#identifierNext > div > button > div.VfPpkd-RLmnJb")
        hit_next.click()
        time.sleep(2)
        pass_inp = driver.find_element_by_css_selector("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
        pass_inp.send_keys(my_passw)
        
        
    login_btn = driver.find_element_by_css_selector("#root > div > div > div > div > div > form > div.card-action.border-0.text-right.mt-3 > button > span.MuiButton-label")
    login_btn.click()

    return(driver)
    
def full_text_path(phone2text, d1, OS):

    driver = hack_openVoice(OS = OS)
    send_texts(driver, phone2text, d1, OS)
    
    return

