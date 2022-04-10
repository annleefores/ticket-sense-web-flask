#ticketsense.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os
import telebot
from dotenv import load_dotenv

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sqlite3



def browser_config():

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("-headless")
    chrome_options.add_argument("--disable-dev-shm-usage")


    try:
        global browser
        global ser
        ser = Service('./chromedriver')
        browser = webdriver.Chrome(
            service=ser, options=chrome_options)
    except:
        browser = webdriver.Chrome(
            options=chrome_options)

browser_config()

#Telegram bot code
load_dotenv()

API_KEY_TEST = os.getenv('API_KEY_TEST')
API_KEY = os.getenv('API_KEY')
USER_ID = os.getenv('USER_ID')


bot = telebot.TeleBot(API_KEY)
def message(msg):
    bot.send_message(USER_ID, msg)

def db_connection():
    db = sqlite3.connect('ticketsense.db')
    db.row_factory = sqlite3.Row
    return db

def db_select(arg1, arg2=''):
    db = db_connection()
    out = db.execute(arg1, arg2)
    return out.fetchall()


def platform(link):
    mainlink = ((link.rsplit('/'))[2])
    bookingsite = ((mainlink.rsplit('.'))[1])
    return bookingsite


def notify(count, show, link, filmname, DATE, MON, YEAR):
    print(count, f'- Ticket booking started for {show.text}')
    if filmname.lower() in show.text.lower():
        print(f'Found ticket for {show.text} - {link}/{YEAR}{MON}{DATE}')
        message(f'Found ticket for {show.text} - {link}/{YEAR}{MON}{DATE}')

def checkout(date, venue, shows, link, filmname, DATE, MON, YEAR):
    po = re.compile(r"\d\d")
    pp = po.search(date.text)
    p = pp.group()

    if p == DATE:
        print(f'{platform(link)}: {venue.text} {DATE}/{MON}/{DATE} slot opened!!!')
        if platform(link) == 'bookmyshow':
            for count, show in enumerate(shows, start=1):
                notify(count, show, link, filmname, DATE, MON, YEAR)
        else:
            for count, show in enumerate(shows[1:], start=1):
                notify(count, show, link, filmname, DATE, MON, YEAR)

        print('-'.center(80, '-'))
    else:
        print(f'{platform(link)}: {venue.text} not yet open')
        print('-'.center(80, '-'))
    return 1


def senseticket_bms(link, filmname, DATE, MON, YEAR):

    browser.get(link + f'/{YEAR}{MON}{DATE}')
    try:
        date = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'showDates')))

        venue = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a.venue-heading')))

        shows = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a.nameSpan')))

        checkout(date, venue, shows, link, filmname, DATE, MON, YEAR)

    except:
        print(f'{platform(link)}: Was not able to find an element with that name.')
        print('-'.center(80, '-'))


def senseticket_tnew(link, filmname, DATE, MON, YEAR):
    browser.get(link + f'/{YEAR}{MON}{DATE}')
    try:
        venue = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="divTheatreInfo"]/h2')))

        shows = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, 'tn-entity-details')))

        date = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'li.ui-tabs-tab.ui-corner-top.ui-state-default.ui-tab.ui-tabs-active.ui-state-active'
            )))

        checkout(date, venue, shows, link, filmname, DATE, MON, YEAR)

    except:
        print(f'{platform(link)}: Was not able to find an element with that name.')
        print('-'.center(80, '-'))




def loopy():
    browser_config()
    data = db_select("SELECT * FROM ticketsensedata ORDER BY link")
    for i in data:
        link = i["link"]
        DATE = i["day"]
        MON = i["month"]
        YEAR = i["year"]
        filmname = i["name"]
        site = platform(link)

        if site == "bookmyshow":
            senseticket_bms(link, filmname, DATE, MON, YEAR)
        else:
            senseticket_tnew(link, filmname, DATE, MON, YEAR)

    browser.close()
    browser.quit()