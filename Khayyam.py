#! /usr/bin/python
"""
    @Author_name : Arsham mohammadi nesyshabori
    @Author_email : arshammoh1998@gmail.com
    @Author_nickname : apep
    @date :
    @version :
"""

from Tools import make_md5
from bs4 import BeautifulSoup
import requests
import time


class User(object):
    headers = {
            'Host': 'pooya.khayyam.ac.ir',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive'}

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()

    def login(self):
        url = "https://pooya.khayyam.ac.ir/gateway/UserInterim.php"
        body = {'UserPassword': make_md5(
                self.password), 'pswdStatus': 'mediocre',
                'UserID': self.username, 'DummyVar': ''}

        for _ in range(3):
            try:
                r = self.session.get(url, headers=self.headers, timeout=8)  # get cookies
                r = self.session.post(url, data=body,
                        headers=self.headers,
                                        timeout=8)  # login and get cookies
                return True
            except:
                    time.sleep(3)

        return False

    def is_login(self):
        url = "https://pooya.khayyam.ac.ir/gateway/PuyaMainFrame.php"
        page_html = ""
        for i in range(3):
            try:
                r = self.session.get(url, headers=self.headers, timeout=8) #get user info
                page_html = r.text
            except:
                time.sleep(3)

        if self.username in page_html:
            return True

        return False


    def _parser_grade(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        rows = soup.findAll('tr')
        grades = []
        try:
            for row in rows:
                col = row.findAll('td')
                if len(col) == 11:
                    grades.append([col[2].get_text(), col[5].get_text(), col[6].get_text(), col[8].get_text()])
                elif len(col) == 7:
                    grades.append([col[2].get_text(), col[5].get_text(), col[6].get_text()])
                elif len(col) == 5:
                    grades.append([col[3].get_text(), col[2].get_text()])
        except Exception as e:
                print(e)
        
        return grades

    def _parser_exam_time(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        rows = soup.findAll('tr')
        exams = []
        try:
            for row in rows:
                col = row.findAll('td')
                if len(col) == 9:
                    exams.append([col[6].get_text(), col[5].get_text(), col[2].get_text()])
        except Exception as e:
            print(e)

        return exams

    def get_exam_time(self):
        url = 'https://pooya.khayyam.ac.ir/educ/stu_portal/ShowStExamDays.php'
        page_html = ""
        for i in range(3):
            try:
                r = self.session.get(url, headers=self.headers, timeout=4)  # send get request with cookies
                page_html = r.text
            except:
                time.sleep(5)

        return self._parser_exam_time(page_html)

    def get_grades(self):
        url = 'https://pooya.khayyam.ac.ir/educ/educfac/stuShowEducationalLogFromGradeList.php'
        page_html = ""
        for i in range(3):
            try:
                r = self.session.get(url, headers=self.headers, timeout=4)  # send get request with cookies
                page_html = r.text
            except:
                time.sleep(5)
        return self._parser_grade(page_html)


if __name__ == "__main__":
    test = User("user", "password")
    test.login()
    if test.is_login():
        print(test.get_exam_time())
        print(test.get_grades())
