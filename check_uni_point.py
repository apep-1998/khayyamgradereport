import telepot
from telepot.loop import MessageLoop
import requests
import hashlib
import time
from bs4 import BeautifulSoup
import json

bot = telepot.Bot("<bot token>")
userList = []
last_point = []
start_gp = []


def createList():
	global userList , bot, start_gp, last_point
	f = open('save.dll', 'r')
	for line in f:
		try:
			line = line.split(":")
			newUser = User(line[0].strip(), line[1].strip(),
			               int(line[2].strip()), bool(line[3].strip()))
			# bot.sendMessage(int(line[2]), '''نترس نمره ای اعلام نشده
			# فقط آپدیت دادیم :)))
			# تو این نسخه اگه ربات تو گروهت استارت کنی به و استادی نمره ای اعلام کنه تو گروه میگه فلان استاد ک فلان درسو میده نمراتش اعلام کرد''')
			if newUser.isLogin():
				userList.append(newUser)
		except:
			print('bad')
	f.close()
	with open("info.json", "r") as info:
		temp = json.load(info)
		last_point = temp["last_point"]
		start_gp = temp["start_gp"]


def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate


@static_var("into", 0)
def saveUser(username, password, teleId, status='True'):
	while(saveUser.into == 1):
		pass
	saveUser.into = 1
	f = open('save.dll', 'r')
	text = (f.read()).split('\n')
	print(text)
	f.close()
	f = open('save.dll', 'w')
	for line in text:
		try:
			tmp = line.split(':')
			if tmp[2] != str(teleId):
				f.write(line+'\n')
		except:
			pass
	text = username+':'+password+':'+str(teleId)+':'+status+"\n"
	f.write(text)
	f.close()
	saveUser.into = 0

def say_new_point(info):
	text = "نمرات درس {} استاد {} اعلام شد"
	for gp in start_gp:
		for _ in range(3):
			try:
				bot.sendMessage(gp, text.format(*info))
				break
			except:
				pass

class User:
	def __init__(self, username, password, teleId, flagCheck=True):
			self.username = username
			self.password = password
			self.session = requests.session()
			self.teleId = teleId
			self.lastPage = ''
			self.flaglogin = True
			self.flagcheck = flagCheck
			self.headers = {
                            'Host': 'pooya.khayyam.ac.ir',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate',
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Connection': 'keep-alive',
                        }
			self.login()
			self.lastPage = self.openGradePage()

	def login(self):
		for i in range(2):
			try:
				self.session = requests.session()
				body = {'UserPassword': self.MD5(
					self.password), 'pswdStatus': 'mediocre', 'UserID': self.username, 'DummyVar': ''}
				url = "https://pooya.khayyam.ac.ir/gateway/UserInterim.php"
				r = self.session.get(url, headers=self.headers, timeout=8)  # get cookies
				r = self.session.post(url, data=body, headers=self.headers,
				                      timeout=8)  # login and get cookies
				break
			except:
				time.sleep(3)

	def isLogin(self):
		for i in range(3):
			try:
				r = self.session.get(
					"https://pooya.khayyam.ac.ir/gateway/PuyaMainFrame.php", headers=self.headers, timeout=8)
				if self.username in r.text:
					print(self.username)
					return True
				return False
			except:
				time.sleep(3)
		return False

	def MD5(self, string):
		m = hashlib.md5()
		m.update(string.encode('utf-8'))
		return m.hexdigest()

	def parserGrade(self, text):
		global bot, last_point, start_gp
		try:
			soup = BeautifulSoup(text, "html.parser")
			rows = soup.findAll('tr')
			output = ""
			for row in rows:
				col = row.findAll('td')
				if len(col) == 11:
					output += col[2].get_text() + "-" + col[5].get_text() + '-' + \
                                            col[6].get_text() + '-' + \
                                            col[8].get_text() + "\n"
					print(last_point)
					if col[6].get_text() == 'عادی' and self.MD5(col[2].get_text()+col[4].get_text()) not in last_point:
						last_point.append(self.MD5(col[2].get_text()+col[4].get_text()))
						say_new_point((col[2].get_text(), col[4].get_text()))
						with open("info.json", "w") as info:
							temp = {"last_point": last_point, "start_gp": start_gp}
							json.dump(temp, info)

				elif len(col) == 7:
					output += col[2].get_text() + '-' + col[5].get_text() + \
                                            '-' + col[6].get_text() + '\n'
				elif len(col) == 5:
					output += col[2].get_text() + "-" + col[3].get_text() + "\n"
			bot.sendMessage(self.teleId, output)
		except Exception as e:
			print(e)

	def parserExamDays(self, text):
		global bot
		try:
			soup = BeautifulSoup(text, "html.parser")
			rows = soup.findAll('tr')
			output = "نام درس-ساعت-تاریخ-مکان\n"
			for row in rows:
				col = row.findAll('td')
				if len(col) == 9:
					output += col[2].get_text() + "-" + col[5].get_text() + '-' + \
                                            col[6].get_text() + '-' + \
                                            col[7].get_text() + "\n"
			bot.sendMessage(self.teleId, output)
		except Exception as e:
			print(e)

	def start(self):
		if not self.isLogin():
			if not self.flaglogin or not self.flagcheck:
				return 0
			self.login()
			if not self.isLogin():
				return 0
		try:
			r = self.openGradePage()
			if(self.lastPage != r):
				self.parserGrade(r)
			self.lastPage = r
		except Exception as e:
			print(e)

	def openExamDaysPage(self):
		if not self.isLogin():
                        if not self.flaglogin:
                                return 0
                        self.login()
                        if not self.isLogin():
                                return 0
		for i in range(3):
			try:
				r = self.session.get('https://pooya.khayyam.ac.ir/educ/stu_portal/ShowStExamDays.php',
				                     headers=self.headers, timeout=4)  # send get request with cookies
				return r.text
			except:
				time.sleep(5)

	def openGradePage(self):
		if not self.isLogin():
                        if not self.flaglogin:
                                return 0
                        self.login()
                        if not self.isLogin():
                                return 0
		for i in range(3):
			try:
				r = self.session.get('https://pooya.khayyam.ac.ir/educ/educfac/stuShowEducationalLogFromGradeList.php',
				                     headers=self.headers, timeout=4)  # send get request with cookies
				return r.text
			except:
				time.sleep(5)


def newMessage(msg):
	global userList, last_point, start_gp
	try:
		if(':' in msg['text'] and msg['chat']["id"] > 0):
			text = msg['text'].split(':')
			username = text[0].strip()
			password = text[1].strip()
			for i in userList:
				if i.username == username:
					bot.sendMessage(msg['chat']['id'], 'این یوزر قبلا وارد شده است')
					return 0
			newUser = User(username, password, msg['chat']['id'])
			if newUser.isLogin():
				saveUser(username, password, msg['chat']['id'])
				userList.append(newUser)
				bot.sendMessage(msg['chat']['id'], 'شما با موفقیت وارد شدید')
			else:
				bot.sendMessage(msg['chat']['id'], 'یوزر نیم یا پسورد شما اشتباه است')
		elif('/nowgrade' in msg['text'] and msg['chat']["id"] > 0):
			for user in userList:
				if user.teleId == msg['chat']['id']:
					user.parserGrade(user.openGradePage())
		elif('/exit' in msg['text'] and msg['chat']["id"] > 0):
			for user in userList:
				if user.teleId == msg['chat']['id']:
					user.flagcheck = False
					saveUser(user.username, user.password, user.teleId, 'False')
					bot.sendMessage(msg['chat']['id'], 'ok shod :(D')
		elif('#نظر' in msg['text'] and msg['chat']["id"] > 0):
				bot.forwardMessage(518323244, msg['chat']['id'], msg['message_id'])
				bot.sendMessage(msg['chat']['id'], 'اوکی بهش گفتم ;)')
		elif('/examdays' in msg['text'] and msg['chat']["id"] > 0):
				for user in userList:
					if(user.teleId == msg['chat']['id']):
						user.parserExamDays(user.openExamDaysPage())
		else:
			if '/start' in msg['text']:
				if msg["chat"]["id"] < 0:
					start_gp.append(msg["chat"]["id"])
					bot.sendMessage(msg["chat"]["id"], "ok :)")
					with open("info.json", "w") as info:
						temp = {"last_point": last_point, "start_gp": start_gp}
						json.dump(temp, info)
				else:
					bot.sendMessage(
						msg['chat']['id'], 'username : password .برای استفاده از برنامه باید یوزر پسورد پرتال خود را به صورت زیر وارد کنید')
	except Exception as e:
		print(e)


createList()

MessageLoop(bot, newMessage).run_as_thread()
while True:
	for user in userList:
		user.start()
	time.sleep(60*15)
