#! /usr/bin/env python
# -*- coding: utf-8 -*-
########################################################
# File Name: gdg.py
# Created By: Zhicong Chen -- chen.zhico@husky.neu.edu
# Creation Date: [2012-11-06 21:57]
# Last Modified: [2012-11-08 00:22]
# Licence: chenzc (c) 2012 | all rights reserved
# Description:  
########################################################

import web, gl
import weibohack
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

### Url mappings

urls = (
	'/', 'Index',
	'/search', 'Search',
	'/(\d+)', 'Show',
)

### Templates
t_globals = {

}

render = web.template.render('templates', base='base', globals=t_globals)

class Index:

	global connect	

	def GET(self):
		connect = web.cookies().get('connect')
		if(connect == '1'):
			raise web.seeother('/search')
		else:
			return render.index('输入帐号连接微博')

	def POST(self):
		username = web.input().username
		password = web.input().password
		content = weibohack.weibo_login(username, password)
		
		if (content == 'successful'):
			web.setcookie('connect','1',600)
			raise web.seeother('/search')
		else:
			return render.index('连接失败')
		
class Search:

	def GET(self):
			connect = web.cookies().get('connect')
			if (connect == '1'):
				return render.search('连接新浪微博成功！')
			else:
				raise web.seeother('/')

	def POST(self):
		uid = web.input().uid
		return web.seeother('/'+uid)

class Show:

	img_list = []
	def GET(self, id):
		samepage = web.cookies().get('samepage')
		weibohack.weibo_set_uid(id, samepage)
		        

		self.img_list = weibohack.weibo_get_img()
    
		return render.show(self.img_list, id)

	def POST(self, id):
		uid = web.input().uid
		if (uid == id or uid == '1'):
			weibohack.weibo_set_uid(id, 1)
			web.setcookie('samepage', '1', 600)
			self.img_list += weibohack.weibo_get_img()
			return render.show(self.img_list, id)
		else:
			web.setcookie('samepage', '0', 600)
			self.samepage = 0
	
		raise web.seeother('/'+uid)
		

app = web.application(urls, globals())

if __name__ == '__main__':
	app.run()
