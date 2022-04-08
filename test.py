import os
import telebot
from dotenv import load_dotenv

load_dotenv()

API_KEY_TEST = os.getenv('API_KEY_TEST')
API_KEY = os.getenv('API_KEY')
USER_ID = os.getenv('USER_ID')


bot = telebot.TeleBot(API_KEY)
def message(msg):
    bot.send_message(USER_ID, msg)
    #bot.send_message(USER_ID_2, msg)
    
testbot = telebot.TeleBot(API_KEY_TEST)
def testmessage(msg):
    testbot.send_message(USER_ID, msg)

message('msg')