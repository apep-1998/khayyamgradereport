#! /usr/bin/python
"""
	@Author_name : Arsham mohammadi nesyshabori
	@Author_email : arshammoh1998@gmail.com
	@Author_nickname : apep
	@date : 
	@version : 
"""

from telepot.loop import MessageLoop
from BotUser import BotUser
from Variable import *
import Variables
import telepot
import time
import json

BotUser.bot = telepot.Bot(bot_token)
MessageLoop(BotUser.bot, new_message).run_as_thread()
BotUser.load_saved_user()


def new_message(msg):
    text = msg["text"]
    user_id = msg['chat']['id']
    if user_id < 0:
        return
    
    if ":" in text:
        username, password = text.split(":")
        new_user = BotUser.add_user(username, password, user_id)
        if new_user.is_login():
            new_user.send_message(successful_login_message)
            BotUser.save_users()
        else:
            new_user.send_message(fail_login_message)
    elif '/nowgrade' == text:
        BotUser.send_user_grades(user_id)
    
    elif '/examdays' == text:
        BotUser.send_user_exams_time(user_id)
    
    elif '#نظر' in text and Variable.admin_telegram_id is not None:
        BotUser.bot.sendMessage(Variable.admin_telegram_id, text)
        BotUser.get_user(user_id).send_message(successful_feed_back)
    
    elif '/start' == text or '/info' == text:
        BotUser.bot.sendMessage(user_id, wellcome_message)
            
    elif '/aboutme' == text:
        BotUser.bot.sendMessage(user_id, info_message)
    
    elif "#send_all" in text and user_id == Variable.admin_telegram_id:
        text = text.replace("#send_all", '')
        BotUser.broadcast_message(text)
    
    elif text == admin_password:
        Variable.admin_telegram_id = user_id
        BotUser.bot.sendMessage(Variable.admin_telegram_id, successful_admin)


while True:
    print("check for new grade")
    BotUser.check_users_grade()
    time.sleep(60*15)
