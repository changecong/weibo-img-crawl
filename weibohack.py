#! /usr/bin/env python
# -*- coding: utf-8 -*-
########################################################
# File Name: weibohack.py
# Created By: Zhicong Chen -- chen.zhico@husky.neu.edu
# Creation Date: [2012-11-07 13:47]
# Last Modified: [2012-11-07 23:21]
# Licence: chenzc (c) 2012 | all rights reserved
# Description:  
########################################################

import urllib, urllib2, cookielib, re, gl
from bs4 import BeautifulSoup
from threading import Thread
from Queue import Queue
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf8')

q = Queue()
NUM = 15
JOBS = 16 

uid = ''

weibo_img_list = []
connect = 0
pagecount = 1

## fake header
headers = {
	'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/2010010    1 Firefox/16.0'
}

## step 1: login
def weibo_login(usr, pwd):
	url = 'http://3g.sina.com.cn/prog/wapsite/sso/login.php?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F%3Fs2w%3Dlogin&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt='

	## cookie
	cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
	urllib2.install_opener(opener)

	## get content
	content = urllib2.urlopen(url).read()

	## analysis
	soup = BeautifulSoup(content)

	## find vk
	vk_input = soup.findAll('postfield', attrs={'name':'vk'})[0]

	vk_r = re.compile('\d+')
	vk = vk_r.findall(str(vk_input))
	## find 'password_xxxx'
	pwd_num = 'password_' + vk[0]

	## generate postdata
	postdata = urllib.urlencode({
		'mobile':usr,
		pwd_num:pwd,
		'remember':'on',
		'backURL':'http%3A%2F%2Fweibo.cn%2F%3Fs2w%3Dlogin',
		'backTitle':'新浪微博',
		'vk':vk_input['value'],
		'submit':'登录'
	})

	## fake header
#	headers = {
#		'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0'
#	}

	## send request
	req = urllib2.Request(
		url = 'http://3g.sina.com.cn/prog/wapsite/sso/login_submit.php?rand=619136017&backURL=http%3A%2F%2Fweibo.cn%2F%3Fs2w%3Dlogin&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt=4&revalid=2&ns=1',
		data = postdata
	)

	result = urllib2.urlopen(req).read()

	## it is a skip page
	soup = BeautifulSoup(result)
	a_skip = soup.findAll('a')[0]

	## get the url & content
	weibo_url = a_skip['href']
	weibo_req = urllib2.Request(
		url = weibo_url,
		headers = headers
	)

	weibo_content = urllib2.urlopen(weibo_req).read()
	weibo_soup = BeautifulSoup(weibo_content)
	weibo = weibo_soup.findAll('body')

	if (weibo_content):
		return 'successful'
	else:
		return 'failed'


## setp 2: use nickname to get uid	
def weibo_get_album_num():
	url_album = 'http://weibo.cn/album/albummblog/?fuid=' + self.uid
	# get the number of images
	req_album = urllib2.Request(
		url = url_album,
		headers = headers
	)
	weibo_album_content = urllib2.urlopen(req_album).read()
	weibo_album_soup = BeautifulSoup(weibo_album_content)
	weibo_album_info = weibo_album_soup.findAll('input', attrs={'name':'mp'})[0]
	weibo_album_num = weibo_album_info['value']
#	weibo_img_num = int(weibo_album_num)*12
	if (weibo_album_content):
		return weibo_album_num
	else:
		return 'empty'
"""
def weibo_get_img(uid, album_num, max):
	weibo_img_list = []
#	weibo_img_num = album_num * 2 > max ? max * 12 : album_num *12
	url_img_pre = 'http://weibo.cn/album/photo/photomblog?fuid='+ uid + '&page='
	for img in range(1 + (album_num-1) *24 , album_num * 24):
		url_img = url_img_pre + str(img)
		req_img = urllib2.Request(
			url = url_img,
			headers = headers
		)

		weibo_img_content = urllib2.urlopen(req_img).read()
		weibo_img_soup = BeautifulSoup(weibo_img_content)
		weibo_img_info = weibo_img_soup.findAll('img')[0]
		weibo_img_url = weibo_img_info['src'][26:]
		weibo_img_url = 'http://ww3.sinaimg.cn/large/'+weibo_img_url
		weibo_img_list.append(weibo_img_url)

	return weibo_img_list
"""
def weibo_set_page_num(num):
	page_num = num

def weibo_set_uid(iuid, samepage):
	global uid
	uid = iuid
	if (samepage == 1):
		global pagecount
		pagecount += 1
	else:
		global pagecount
		pagecount = 1
		del weibo_img_list[:]

def get_img(num):
	print num
	url_img_pre = 'http://weibo.cn/album/photo/photomblog?fuid='+ uid + '&page='
	url_img = url_img_pre + str(num)
	req_img = urllib2.Request(
		url = url_img,
		headers = headers
	)

	weibo_img_content = urllib2.urlopen(req_img).read()
	weibo_img_soup = BeautifulSoup(weibo_img_content)
	weibo_img_info = weibo_img_soup.findAll('img')[0]
	weibo_img_url = weibo_img_info['src'][26:]
	weibo_img_url = 'http://ww3.sinaimg.cn/large/'+weibo_img_url

	weibo_img_list.append(weibo_img_url)

## multi-thread
def working():
	while True:
		arguments = q.get()

		get_img(arguments)

		sleep(1)
		q.task_done()

def weibo_get_img():
	# fork NUM thread
	for i in range(1, NUM):
		t = Thread(target=working)
		t.setDaemon(True)
		t.start()

	# in que
	for i in range(1+(pagecount - 1)*JOBS, pagecount*JOBS):
		q.put(i)

	# wait for finish
	q.join() 

	return weibo_img_list
