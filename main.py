import telebot
import time
import random
import os
from random import randint
from glob import glob


TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)
while True:
    day = 86400
    random_time = randint(day,day*3)
    pic_list = glob(os.getcwd() + '/pic/*.jpg')
    random_image = random.choice(pic_list)
    with open(random_image, 'rb') as photo:
        bot.send_photo(CHAT_ID, photo)
        time.sleep(random_time)
bot.polling(non_stop=True)
