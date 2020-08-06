#! /usr/bin/python
"""
    @Author_name : Arsham mohammadi nesyshabori
    @Author_email : arshammoh1998@gmail.com
    @Author_nickname : apep
    @date : 
    @version : 
"""
from Khayyam import User
from Tools import make_md5, create_keyboard
from Variables import grade_text, grade_change, exam_day
import json

class BotUser(User):
    bot = None
    users = []
    
    @classmethod
    def add_user(cls, username, password, telegram_id):
        for i in range(len(cls.users)):
            if cls.users[i].username == username:
                cls.users[i].password = password
                cls.users[i].telegram_id = telegram_id
                cls.users[i].login()
                return cls.users[i]
        else:
            cls.users.append(cls(username, password, telegram_id))
            return cls.users[-1]
    
    @classmethod
    def save_users(cls):
        with open("users_info.json", "w") as save_file:
            json.dump([user.get_info() for user in cls.users], save_file)
            
    @classmethod
    def send_user_grades(cls, telegram_id):
        for user in cls.users:
            if user.telegram_id == telegram_id:
                user.send_grade()

    @classmethod
    def send_user_exams_time(cls, telegram_id):
        for user in cls.users:
            if user.telegram_id == telegram_id:
                user.send_exams_time()
    
    @classmethod
    def get_user(cls, telegram_id):
        for user in cls.users:
            if user.telegram_id == telegram_id:
                return user
    
    @classmethod
    def load_saved_user(cls):
        user_info = []
        try:
            with open("users_info.json", "r") as user_info_file:
                user_info = json.load(user_info_file)
        except:
            pass
        for user in user_info:
            cls.add_user(**user)
            
    @classmethod
    def check_users_grade(cls):
        for user in cls.users:
            user.check_for_new_grade()
    
    @classmethod
    def broadcast_message(cls, message):
        for user in cls.users:
            user.send_message(message)

    def __init__(self, username, password, telegram_id):
        super().__init__(username, password)
        self.login()

        self.telegram_id = telegram_id

        self.last_grades = self.get_grades()
        self.last_grades_md5 = make_md5(str(self.last_grades))

    def send_message(self, text, **kwargs):
        for _ in range(3):
            try:
                self.bot.sendMessage(self.telegram_id, text, **kwargs)
                break
            except Exception as e:
                print(e)
        
    def check_for_new_grade(self):
        if not self.is_login():
            self.login()
            return
        now_grade = self.get_grades()
        if self.last_grades_md5 != make_md5(str(now_grade)):
            diff_text = self.find_diff(now_grade)
            self.send_grade(diff_text)
            self.last_grades = now_grade
            self.last_grades_md5 = make_md5(str(self.last_grades))
        
    
    def make_grades_table(self, grades):
        key_pattern = []
        for line in grades:
            key_pattern.append(list(zip(line, range(len(line)))))
        return create_keyboard(key_pattern)
    
    def find_diff(self, new_grades):
        text = grade_text
        for last_line, new_line in zip(self.last_grades, new_grades):
            if last_line != new_line:
                text += grade_change.format(new_line[0])
        return text
    
    def send_grade(self, text=None):
        if not self.is_login():
            self.login()
        if text is None:
            text = grade_text
        now_grade = self.get_grades()
        now_grade = [line[::-1] for line in now_grade]
        now_grade[-1] = now_grade[-1][::-1]
        table = self.make_grades_table(now_grade)
        self.send_message(text, reply_markup=table)
    
    def send_exams_time(self):
        if not self.is_login():
            self.login()
        table = self.make_grades_table(self.get_exam_time())
        self.send_message(exam_day, reply_markup=table)
    
    def get_info(self):
        return {
            "username" : self.username,
            "password" : self.password,
            "telegram_id" : self.telegram_id,
        }