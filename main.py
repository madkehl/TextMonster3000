from MW import full_email_path
from GVoice import full_text_path
import pandas as pd

try:
    email_phone = pd.read_csv('./email_phone.csv', index_col = 0)
except pd.errors.EmptyDataError:
    print("NO EMAILS OR PHONES")

def main():
    email = input('metricwire email: ')
    passw = input('metricwire password: ')
    OS = input('Are you using MAC or WINDOWS? (enter in all caps)')
    texts_today = full_email_path(email = email, passw = passw, pgconst = '4', OS = OS).reset_index()
    phone2text = texts_today.merge(email_phone, left_on = 'index', right_on = 'email', how = 'left')
    full_text_path(phone2text)
    
if __name__ == '__main__':
    main()


