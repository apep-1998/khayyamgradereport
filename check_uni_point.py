import telepot
from telepot.loop import MessageLoop
import requests,hashlib,time
from bs4 import BeautifulSoup

bot = telepot.Bot("547618250:AAHGogoigTHfHCL4R7REwTwFV1AZmVgluxA")
userList = []

def createList():
	global userList
	f = open('save.dll','r')
	for line in f:
		line = line.split(":")
		newUser = User(line[0].strip(),line[1].strip(),int(line[2].strip()))
		if newUser.isLogin():
			userList.append(newUser)
	f.close()

def saveUser(username,password,teleId):
	f = open('save.dll','a')
	text = username+':'+password+':'+str(teleId)+"\n"
	f.write(text)
	f.close()

		

class User:
	def __init__(self,username , password , teleId):
			self.username = username
			self.password = password
			self.session = requests.session()
			self.teleId = teleId
			self.lastPage = ''
			self.flaglogin = True
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
			
	def login(self):
		for i in range(2):
			try:
				body = {'UserPassword':self.MD5(self.password),'pswdStatus':'mediocre','UserID':self.username,'DummyVar':''}
				url = "https://pooya.khayyam.ac.ir/gateway/UserInterim.php"
				
				r = self.session.get(url, headers= self.headers,timeout = 4) # get cookies
				r = self.session.post(url, data = body, headers = self.headers , timeout=4) # login and get cookies
				# /login
				break
			except:
				time.sleep(3)
	
	def isLogin(self):
		for i in range(3):
			try:
				r = self.session.get("https://pooya.khayyam.ac.ir/gateway/PuyaMainFrame.php",headers=self.headers)
				if self.username in r.text:
					return True
				return False
			except:
				time.sleep(3)
		print(1)
		return False

	def MD5(self,string):
		m = hashlib.md5()
		m.update(string.encode('utf-8'))
		return m.hexdigest()
	

	def parser(self,text):
		try:
			soup = BeautifulSoup(text, "html.parser")
			rows = soup.findAll('tr')
			lessons = []
			output = ""
			for row in rows:
				col = row.findAll('td')
				if len(col) == 11:
					lessons.append([col[2].get_text(), col[5].get_text()])
					output += col[2].get_text() + " : " + col[5].get_text() + "\n"
				elif len(col) == 5:
					lessons.append([col[2].get_text(), col[3].get_text()])
					output += col[2].get_text() + " : " + col[3].get_text() + "\n"
			return output
		except Exception as e:
			print(2)
			print(e)

	def start(self):
		if not self.isLogin():
			if not self.flaglogin:
				return 0
			self.login()
			if not self.isLogin():
				self.flaglogin = False
				return 0
		try:
			r = self.session.get('https://pooya.khayyam.ac.ir/educ/educfac/stuShowEducationalLogFromGradeList.php', headers = self.headers , timeout=4) # send get request with cookies
			if(self.lastPage != r.text):
				text = self.parser(r.text)
				bot.sendMessage(self.teleId,text)
			self.lastPage = r.text
		except Exception as e:
			print(e)

def newMessage(msg):
	global userList
	try:
		if(':' in msg['text']):
			text = msg['text'].split(':')
			username = text[0].strip()
			password = text[1].strip()
			for i in userList:
				if i.username == username:
					bot.sendMessage(msg['chat']['id'],'این یوزر قبلا وارد شده است')
					return 0
			newUser = User(username , password ,msg['chat']['id'])
			if newUser.isLogin():
				saveUser(username,password,msg['chat']['id'])
				userList.append(newUser)
				bot.sendMessage(msg['chat']['id'],'شما با موفقیت وارد شدید')
			else:
				bot.sendMessage(msg['chat']['id'],'یوزر نیم یا پسورد شما اشتباه است')
		else:
			bot.sendMessage(msg['chat']['id'],'username : password .برای استفاده از برنامه باید یوزر پسورد پرتال خود را به صورت زیر وارد کنید')
	except:
		pass


createList()

MessageLoop(bot, newMessage).run_as_thread()

while True:
	for user in userList:
		user.start()
	time.sleep(30)