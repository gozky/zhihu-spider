# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re,sys, cookielib

url = 'http://www.zhihu.com'

form = {'email': 'xxx@gmail.com',
	'password': 'passwd' }
reload(sys)
sys.setdefaultencoding('utf8')

def login(account=None, password=None):
	
	if isLogin() == True:
		print("你已经登录过了")
		return True
	if account == None:
		sys.stdout.write("请输入登录帐号：")
		account = raw_input()
		sys.stdout.write("请输入密码：")
		password = raw_input()
	form_data = build_form(account, password)

	results = upload_form(form_data)
	
	return results




def isLogin():
	# check session
	url = 'http://www.zhihu.com/settings/profile'
	r = requests.get(url, allow_redirects=False)
	status_code = int(r.status_code)
	#print status_code, r.history

	if status_code == 301 or status_code == 302:
		return False
	elif status_code == 200:
		return True
	else:
		print("网络故障")
		return None

def build_form(account, password):
	if re.match(r"^1\d{10}$", account):
		account_type = "phone"
	elif re.match(r"^\S+\@\S+\.\S+$", account): account_type="email"
	else: print("帐号类型错误")

	form = {account_type: account, "password": password, "remember_me": True }
	form['_xsrf'] = search_xsrf()

	return form
def search_xsrf():
	url = 'http://zhihu.com/'
	r = requests.get(url, verify=False)
	if int(r.status_code) != 200:
		print "连接失败"
	results = re.compile(r"\<input\stype=\"hidden\"\sname=\"_xsrf\"\svalue=\"(\S+)\"").findall(r.text)
	if len(results) < 1:
		print ("提取XSRF 代码失败" )
		return None
	return results[0]

def upload_form(form):
	s = requests.Session()
	if "email" in form: url = "http://www.zhihu.com/login/email"
	elif "phone" in form: url = "http://www.zhihu.com/login/phone_num"
	else: raise ValueError(u"账号类型错误")
	headers = {
	'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
	        'Host': "www.zhihu.com",
	        'Origin': "http://www.zhihu.com",
	        'Pragma': "no-cache",
	        'Referer': "http://www.zhihu.com/",
	        'X-Requested-With': "XMLHttpRequest"
	}
	r = s.post(url, data=form, headers=headers)
	#print r.status_code
	m_cookies = r.cookies
	test_url = 'http://www.zhihu.com/people/cha-men-hu-de-xiao-bei-xin'
	#print m_cookies
	res = s.get(test_url, headers=headers, cookies=m_cookies,verify=False)

	return res.text

r = login('xxx@gmail.com', 'passwd')
f = open("xx.html", 'w')
f.write(r)
f.close()






