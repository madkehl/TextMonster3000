from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import sys
from datetime import date
from datetime import timedelta
import math

today = date.today()
yesterday = today - timedelta(days = 1)
anteayer = today - timedelta(days = 2)
# dd/mm/YY
d2 = today.strftime("%d-%m-%Y")
d1 = yesterday.strftime("%d-%m-%Y")
d0 = anteayer.strftime("%d-%m-%Y")


urlMW = "https://app.metricwire.com/"

path_button = "#root > div > main > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-12.MuiGrid-grid-md-8 > div > div.MuiCardContent-root > table > tbody > tr:nth-child(1) > td:nth-child(3) > a"

try:
    date_records = pd.read_csv('stored_vals.csv', index_col = 0)
except pd.errors.EmptyDataError:
    date_records = pd.DataFrame()

if d1 in date_records.columns:
    delete = input("You are about to delete the column for " + d1 + ".  If this is what you want type TRUE")
    if delete == "TRUE":
        date_records = date_records.drop(d1, axis = 1)
        print("DELETED")
    else:
        print("NOT DELETED")
    
pgconst = 4

def loginMetricWire(my_email, my_passw, OS = 'Mac'):
    '''
    INPUT: str formatted username and password for MetricWire account

    OUTPUT: driver for next function, simply opens in a test browser
    '''
    driver = webdriver.Chrome()
    driver.get(urlMW)

    time.sleep(3)
    email_inp = driver.find_element_by_css_selector("#root > div > div > div > div > div > form > div:nth-child(4) > div > input")
    email_inp.send_keys(my_email)

    pass_inp = driver.find_element_by_css_selector("#root > div > div > div > div > div > form > div:nth-child(5) > div > input")
    pass_inp.send_keys(my_passw)

    login_btn = driver.find_element_by_css_selector("#root > div > div > div > div > div > form > div.card-action.border-0.text-right.mt-3 > button > span.MuiButton-label")
    login_btn.click()
    
    return(driver)

def openStudy(study_path, driver, pgconst):
    '''
    INPUT: path to workspace for study of interest

    OUTPUT: None, simply operates in test browser

    Notes: login must be run before running this
    '''

    try:
        sbdl_wksp = driver.find_element_by_css_selector(study_path)
        sbdl_wksp.click()
    except:
        time.sleep(3)
        sbdl_wksp = driver.find_element_by_css_selector(study_path)
        sbdl_wksp.click()

    time.sleep(1)
    sbdl_study = driver.find_element_by_css_selector("#root > div > main > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-4 > div:nth-child(2) > a > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-8")
    sbdl_study.click()

    time.sleep(1)
    sbdl_view = driver.find_element_by_css_selector("#root > div > main > div > div > div > div > table > tbody > tr > td:nth-child(4) > a > button > span.MuiButton-label")
    sbdl_view.click()

    time.sleep(5)
    part_btn = driver.find_element_by_css_selector("#root > div > main > div > div > header > div > div > div > div > div > button:nth-child(6)")
    part_btn.click()

    time.sleep(4)

    #expand_btn = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div/div/div[2]/div/div/div/table/tfoot/tr/td/div/div[2]/div")
    #expand_btn.click()

    #sel300 = driver.find_element_by_xpath("/html/body/div[" + str(pgconst) + "]/div[3]/ul/li[3]")
    #sel300.click()
    try:
        sort_btn = driver.find_element_by_css_selector("#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.jss97 > div > div > div > table > thead > tr > th:nth-child(10) > span > div")
        sort_btn.click()
    except:
        sort_btn = driver.find_element_by_css_selector("#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.jss96 > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(10) > div > div > div > span")
        sort_btn.click()
        pass
    return(driver)

def get_emails(date, driver):
    '''
    INPUT: date of enrollment that you are interested in grabbing
    
    OUTPUT: result list of email and number of submissions
    '''
    try:
        page = 'jss97'
        table = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.'+ page + ' > div > div > div > table > tbody')

    except:
        try:
            time.sleep(2)
            table = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.'+ page + ' > div > div > div > table > tbody')
        except:
            page = 'jss96'
            table = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.'+ page + ' > div > div > div > table > tbody')

#iterate through participants
    isDate = False
    participant_email = []
    participant_subm = []
    for row in table.find_elements_by_css_selector('tr'):
        try:
            row_num = row.get_attribute("index")
            row_num = int(row_num) + 2
            print('ROWNUM: ' + str(row_num))
            try:
                last_submit = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.'+ page +' > div > div > div > table > tbody > tr:nth-child('+ str(row_num) + ') > td:nth-child(12)')
                enroll_date = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.'+ page +' > div > div > div > table > tbody > tr:nth-child(' + str(row_num) + ') > td:nth-child(10)')
            except:
                time.sleep(3)
                enroll_date = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.'+ page + ' > div > div > div > table > tbody > tr:nth-child(' + str(row_num) + ') > td:nth-child(10)')
                last_submit = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.'+ page + ' > div > div > div > table > tbody > tr:nth-child('+ str(row_num) + ') > td:nth-child(12)')
                print(enroll_date.text)
                print(last_submit.text)
            print(enroll_date.text)
            print(last_submit.text)
            if (enroll_date.text[:10] != d0) and (enroll_date.text[:10] != d2) and ('2020' in enroll_date.text):
                isDate = True
                email_ob = driver.find_element_by_css_selector('#root > div > main > div > div > div > div > div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1.MuiPaper-rounded > div > div > div > div.'+ page +' > div > div > div > table > tbody > tr:nth-child(' + str(row_num) + ') > td:nth-child(5)')
                email = email_ob.text.split('@')[0]
                print(email)
                participant_email.append(email)
                if last_submit.text[:10] == d1 or last_submit.text[:10] == d2:
                    participant_subm.append(1)
                    print(email + 'has participated within the last 24 hours')
                else:
                    participant_subm.append(0)
            else:
                    if isDate == True:
                        break
        except:
            pass
    return participant_email, participant_subm
    
def update_df(part_ls, subm_ls):
    for i in range(len(part_ls)):
        print(i)
        print(part_ls)
        date_records.loc[part_ls[i], d1] = subm_ls[i]
    date_records.to_csv('stored_vals.csv')
    return
        
def assign_text(d1):
    texts_today = pd.DataFrame()
    for i in range(len(date_records[d1])):
        index = date_records.index.values[i]
        if math.isnan(date_records.loc[index, d1]) == False:
            val = int(date_records.loc[index, d1])
            current_row = date_records.loc[index]
            print(current_row)
            streaks = (current_row.groupby((current_row != current_row.shift()).cumsum()).cumcount() + 1)
            curr_val_streak =streaks[len(streaks) - 1]
            if val == 0:
                if curr_val_streak >= 1:
                    texts_today.loc[index, d1] = 'Hey, this is PPOL! You have missed surveys for ' + str(curr_val_streak) + ' days. Please contact us at ppolpitt@pitt.edu if you are having technical issues.'
                else:
                    texts_today.loc[index, d1] = None
            elif val == 1:
                texts_today.loc[index, d1] = 'You answered surveys yesterday!  You are on a ' + str(curr_val_streak) + ' day streak!'
        else:
            print('Participant ' + str(index) + ' not yet enrolled.')
    return texts_today
        
    
        
def full_email_path(email, passw, pgconst, OS = 'MAC', study_path = path_button):
    '''
    INPUT: study_path, date of enrollment
    
    OUTPUT: result df
    
    Runs everything above in sequence
    '''
    driver = loginMetricWire(email, passw, OS = OS)
    print('LOGGED IN')
    driver =openStudy(study_path, driver, pgconst)
    print('STUDY OPENED')
    participant_email, participant_subm = get_emails(date, driver)
    print('GOT EMAILS + SUBM')
    update_df(participant_email, participant_subm)
    print('DF UPDATED')
    texts_today = assign_text(d1)
    print('TEXTS CREATED')
    print(texts_today)
    
    return texts_today, d1
