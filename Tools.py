#! /usr/bin/python
"""
    @Author_name : Arsham mohammadi nesyshabori
    @Author_email : arshammoh1998@gmail.com
    @Author_nickname : apep
    @date : 
    @version : 
"""

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import hashlib

def make_md5(string: str):
    """ 
        make md5 of input string
    """
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def create_keyboard(pattern):
    key_pattern = []
    for line_keys in pattern:
        line_keyboard = []
        for button in line_keys:
            text, val = button
            line_keyboard.append(InlineKeyboardButton(text=text, callback_data=val))
        key_pattern.append(line_keyboard)
    return InlineKeyboardMarkup(inline_keyboard=key_pattern)
