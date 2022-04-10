#ticketsense.py

# selenium used for web scraping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# re module for regular expressions
import re

# os module used for getting env variables
import os
# telegram module to interact with telegram chat app
import telebot

# used to source data from .env
from dotenv import load_dotenv

import sqlite3


# function to configure chrome browser and chrome driver
def browser_config():

    # configures chrome to run in headless and other modes
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("-headless")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # sets up browser to be automated also catches any errors
    try:
        global browser
        global ser
        ser = Service('./chromedriver')
        browser = webdriver.Chrome(
            service=ser, options=chrome_options)
    except:
        browser = webdriver.Chrome(
            options=chrome_options)


# loads dotenv to collect data from .env
load_dotenv()

# assigns value collected from .env to variables
API_KEY_TEST = os.getenv('API_KEY_TEST')
API_KEY = os.getenv('API_KEY')
USER_ID = os.getenv('USER_ID')

# code to initialize telegram bot function
bot = telebot.TeleBot(API_KEY)
def message(msg):
    bot.send_message(USER_ID, msg)

# connect to SQLite database
def db_connection():
    db = sqlite3.connect('ticketsense.db')
    db.row_factory = sqlite3.Row
    return db

# function to simplify inserting commands to SQLite
def db_select(arg1, arg2=''):
    db = db_connection()
    out = db.execute(arg1, arg2)
    return out.fetchall()

# function that retrieves booking site detail from the link
def platform(link):
    mainlink = ((link.rsplit('/'))[2])
    bookingsite = ((mainlink.rsplit('.'))[1])
    return bookingsite

# function to check whether the tickets have opened -- if yes prints and sends message using telegram app
def notify(count, show, link, filmname, DATE, MON, YEAR):
    print(count, f'- Ticket booking started for {show.text}')
    if filmname.lower() in show.text.lower():
        print(f'Found ticket for {show.text} - {link}/{YEAR}{MON}{DATE}')
        message(f'Found ticket for {show.text} - {link}/{YEAR}{MON}{DATE}')

# main function loop through the database and perfrom functions
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

# function to scrap through bookmyshow website
def senseticket_bms(link, filmname, DATE, MON, YEAR):

    browser.get(link + f'/{YEAR}{MON}{DATE}')
    try:
        # collectes data based on given ID, class or other unique tags
        date = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'showDates')))

        venue = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a.venue-heading')))

        shows = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a.nameSpan')))

        # run checkout function
        checkout(date, venue, shows, link, filmname, DATE, MON, YEAR)

    # if an error occured print
    except:
        print(f'{platform(link)}: Was not able to find an element with that name.')
        print('-'.center(80, '-'))

# function to scrap through ticketnew website
def senseticket_tnew(link, filmname, DATE, MON, YEAR):
    browser.get(link + f'/{YEAR}{MON}{DATE}')
    try:
         # collectes data based on given ID, class or other unique tags
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



# a function that controls all the above functions, this function is called by app.py to start scraping
def loopy():
    # runs browser config code
    browser_config()
    # selectes data from database and sorts it based on the link
    data = db_select("SELECT * FROM ticketsensedata ORDER BY link")

    # loops through the database and passes on the values to the functions
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

    # closes browser after scraping is done
    browser.close()
    browser.quit()