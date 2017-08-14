#!/usr/bin/python
# -*- coding: gb2312 -*-


#########################################################################
#2015-12-11 09:47:46
#author: 358275018@qq.com

########################################################################


import urllib2, urllib, traceback, smtplib, datetime
import os, sys, time,zlib,json,ConfigParser,codecs
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage

import email.MIMEMultipart  
import email.MIMEText  
import email.MIMEBase  

from utility import getPyLogger,debug,info

#mail_host="smtp.qq.com"			#设置服务器
mail_host='smtp.qq.com'
mail_user="358275018@qq.com"		#用户名
mail_pass="xxxxxxxxx"				#口令, 请修改!!!

MORNING_START="08:30"				#上班, 截获从8:30到8:40的顺风单
MORNING_END="08:40"
AFTERNOON_START="18:05"				#下班, 截获从18:05到18:20的顺风单
AFTERNOON_END="18:20"
last_modify_time = 0

TOKEN='JPXq-mw6-YPhBnegPQ6pdbwJvXMOw5SnLfWW6-gl1pVUjDsOwkAMRO8ytQvb62wc34Y_FAiJFVW0d2faVCO9N3o7TihAcEZ5WqyLbov3toYKrmQuuKF2jPdAWfRwN9dNMD6_74VKp-B-VA8mrXkSZMvO-pNEuS8e5z8AAP__'

def loadTimeConfig():
	global last_modify_time,MORNING_START,MORNING_END,AFTERNOON_START,AFTERNOON_END
	file_name = r"C:\ddrive\mynutstore\ditime2.txt"
	if(not os.path.exists(file_name)):
		return
	statinfo=os.stat(file_name)
	if(statinfo.st_mtime>last_modify_time):
		last_modify_time = statinfo.st_mtime
		config = ConfigParser.ConfigParser()
		try:
			config.readfp(codecs.open(file_name, "r", "utf_16"))
		except Exception, e: 
			config.read(file_name)
		try:
			MORNING_START=config.get('TIME_INFO', 'MORNING_START').strip()
		except Exception, e: 
			pass
		try:
			MORNING_END=config.get('TIME_INFO', 'MORNING_END').strip()
			print 'MORNING_END=',MORNING_END
		except Exception, e: 
			pass
		try:
			AFTERNOON_START=config.get('TIME_INFO', 'AFTERNOON_START').strip()
		except Exception, e: 
			pass
		try:
			AFTERNOON_END=config.get('TIME_INFO', 'AFTERNOON_END').strip()
		except Exception, e: 
			pass
			
def getHtmlContent(respInfo):
	htmlContent = ''
	try:
		respHtml = respInfo.read()
		if( ("Content-Encoding" in respInfo.headers) and (respInfo.headers['Content-Encoding'] == "gzip")):
			htmlContent = zlib.decompress(respHtml, 16+zlib.MAX_WBITS);
		else:
			htmlContent = respHtml
	except BaseException, e:
		debug(logger, traceback.format_exc())
	return htmlContent
	
def send_mail(to_list,sub,content):  
    me="358275018@qq.com"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  
		 



headers = {
	'Host': 'api.didialift.com'
	,'Accept-Encoding': 'gzip'
	,'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI 4LTE MIUI/V7.2.11.0.MXDCNDB)'
}
common_headers = {
	'Host': 'common.diditaxi.com.cn'
	,'Accept-Encoding': 'gzip'
	,'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI 4LTE MIUI/V7.2.11.0.MXDCNDB)'
}
xiaojukeji_headers = {
	'Host': 'pay.xiaojukeji.com'
	,'Accept-Encoding': 'gzip, deflate'
	,'Accept': '*/*'
	,'Accept-Language': 'zh-Hans;q=1, en;q=0.9, fr;q=0.8, de;q=0.7, zh-Hant;q=0.6, ja;q=0.5'
	,'User-Agent': 'OneTravel/4.1.4.3 (iPhone; iOS 7.1.2; Scale/2.00)'
}


ROUTE_ID_MORNING1='12132747'		#家->办公室
ROUTE_ID_AFTERNOON1='109950277'		#办公室->家
one_way_map = {	
	'android_id':'2227d1a93826902'
	,'appversion':'4.4.10'
	,'at_mb_cid':'19771395'
	,'at_mb_lac':'16836'
	,'at_mb_mcc':'460'
	,'at_mb_mnc':'01'
	,'at_net_st':'1'
	,'at_wf_bssid':'8c:be:be:16:b5:74'
	,'at_wf_ssid':'"zzzzzz"'
	,'channel':'0'
	,'city_id':'14'
	,'cpu':'Processor	: ARMv8 Processor rev 1 (v8l)'
	,'datatype':'1'
	,'date_id':'1477584000'
	,'dviceid':'bf39e245983e7ce8b96ec5cb468f4b9e'
	,'filter':'0'
	,'imei':'8659310207085419EFC357283F3AFD66688CC444C08403A' ################
	,'lat':'38.844252869870736'
	,'lng':'121.51104529558397'
	,'locatePerm':'1'
	,'locateTime':'1462240824'
	,'mac':'74:51:ba:55:a6:8f'
	,'maptype':'soso'
	,'model':'MI 4LTE'
	,'networkType':'WIFI'
	,'os':'6.0.1'
	,'route_id':'12132747'
	#,'sig':'2cdde9c6ac1b653c19a31a535b1959acf0c61156'
	,'suuid':'F759479A0C2CCDE83BE5EA8D5F6EC05E_15'
	,'token':TOKEN
	,'uuid':'D85C052433285BB365875F9F3AA28EFE'###############
	,'vcode':'162'
	,'wsgsig':'sign error'
}

#抢单参数
strive_para_map = {
	'android_id':'2227d1a93826902'  #'_t':'1449818404'
	,'appversion':'4.4.10'
	,'at_mb_cid':'18589187'
	,'at_mb_lac':'16838'
	,'at_mb_mcc':'460'
	,'at_mb_mnc':'01'
	,'at_net_st':'1'
	,'at_wf_bssid':'8c:be:be:16:b5:74'
	,'at_wf_ssid':'zzzzzz'
	,'channel':'0'
	,'city_id':'14'
	,'cpu':'Processor	: ARMv8 Processor rev 1 (v8l)'
	,'datatype':'1'
	,'dviceid':'bf39e245983e7ce8b96ec5cb468f4b9e'
	,'imei':'8659310207085419EFC357283F3AFD66688CC444C08403A'
	,'lat':'38.849033'
	,'lng':'121.518660'
	,'locatePerm':'1'
	,'locateTime':'1449818399'
	,'mac':'74:51:ba:55:a6:8f'
	,'maptype':'soso'
	,'model':'MI 4LTE'
	,'networkType':'WIFI'
	,'order_id':'3635506508184237070'
	,'order_level':'1'
	,'os':'6.0.1'
	,'route_id':'4338899913'
	,'serial':'1462283172995'
	#,'sig':'82d12c28338ca223876af1242cf341e6a334cc50'
	,'source':'0'
	,'suuid':'F759479A0C2CCDE83BE5EA8D5F6EC05E_15'
	,'token':TOKEN
	,'uuid':'D85C052433285BB365875F9F3AA28EFE'
	,'vcode':'162'
	,'view_sort':'0c'
}

def getSig(map):
	from operator import itemgetter
	params = sorted(map.iteritems(), key=itemgetter(0), reverse=False)
	newList = []
	PREFIX = "didiwuxiankejiyouxian2013"
	newList.append(PREFIX)
	for parm in params:
		newList.append(parm[0]+parm[1])
	newList.append(PREFIX)
	data = ''.join(newList)
	import hashlib
	sig = hashlib.sha1(data).hexdigest();
	return sig

POINT_HOME = set([u'万科溪之谷',u'依云溪谷'])
POINT_OFFICE = set([u'大连软件园腾飞',u'腾飞软件园',u'谷歌里',u'东软软件园B区'])

def filter(order):
	departure_time = order["trip_info"]['text_setup_time']
	#route_id = order['route_id']
	order_id = order["order_info"]['order_id']
	from_name = order["trip_info"]['from_name']
	from_address = order["trip_info"]['from_address']
	to_name = order["trip_info"]['to_name']
	to_address = order["trip_info"]['to_address']
	price = order["trip_info"]['price']
	
	global MORNING_START,MORNING_END,AFTERNOON_START,AFTERNOON_END
	#上班
	if(departure_time[-5:]>=MORNING_START and departure_time[-5:]<=MORNING_END):
		#测试起点
		start = False;
		for oneArea in POINT_HOME:
			if from_name.find(oneArea)>-1:
				start = True;
				break;
		if(start == False):
			return False;        
		
		#测试终点
		end = False;
		for oneArea in POINT_OFFICE:
			if to_name.find(oneArea)>-1:
				end = True;
				break;
		return end;
	
	#下班
	if(departure_time[-5:]>=AFTERNOON_START and departure_time[-5:]<=AFTERNOON_END):
		#测试起点
		start = False;
		for oneArea in POINT_OFFICE:
			if from_name.find(oneArea)>-1:
				start = True;
				break;
		if(start == False):
			return False;        
		
		#测试终点
		end = False;
		for oneArea in POINT_HOME:
			if to_name.find(oneArea)>-1:
				end = True;
				break;
		return end;
		
	return False; #其它一律视为不符合条件
	
HOME_at_wf_bssid = 'ec:88:8f:2b:a1:84'
HOME_at_wf_ssid = '"MERCURY_2BA184"'
HOME_lat='38.814874403212'
HOME_lng='121.577924262153'
HOME_at_mb_cid='68630454'
HOME_at_mb_lac='49441'
#
OFFICE_at_wf_bssid = '8c:be:be:16:b5:74'
OFFICE_at_wf_ssid = '"zzzzzz"'
OFFICE_lat='38.949033203125'
OFFICE_lng='121.418660753038'
OFFICE_at_mb_cid='18538497'
OFFICE_at_mb_lac='16836'

#修改参数
def updateParmsMap(map):
	localtime = time.localtime(time.time())
	hour = str(localtime.tm_hour)
	min = str(localtime.tm_min)
	if(len(hour)==1): hour='0'+hour
	if(len(min)==1): min='0'+min
	hm = hour+':'+min
	if( hm>'09:00' and hm<'18:30'):#OFFICE
		if(map.has_key('at_wf_bssid')): map['at_wf_bssid']=OFFICE_at_wf_bssid
		if(map.has_key('at_wf_ssid')): map['at_wf_ssid']=OFFICE_at_wf_ssid
		if(map.has_key('lat')): map['lat']=OFFICE_lat
		if(map.has_key('lng')): map['lng']=OFFICE_lng
		if(map.has_key('at_mb_cid')): map['at_mb_cid']=OFFICE_at_mb_cid
		if(map.has_key('at_mb_lac')): map['at_mb_lac']=OFFICE_at_mb_lac
	else:#HOME
		if(map.has_key('at_wf_bssid')): map['at_wf_bssid']=HOME_at_wf_bssid
		if(map.has_key('at_wf_ssid')): map['at_wf_ssid']=HOME_at_wf_ssid
		if(map.has_key('lat')): map['lat']=HOME_lat
		if(map.has_key('lng')): map['lng']=HOME_lng
		if(map.has_key('at_mb_cid')): map['at_mb_cid']=HOME_at_mb_cid
		if(map.has_key('at_mb_lac')): map['at_mb_lac']=HOME_at_mb_lac
	now = int(time.time())
	#map['_t']=str(now)
	map['locateTime']=str(now+10)
	if(map.has_key('app_time')): map['app_time']=str(now+10)
	date_id = int(time.mktime(datetime.date.today().timetuple()))
	map['date_id']=str(date_id)
	sig = getSig(map)
	map['sig']=sig
		
def getOrdersViaUrl(url):
	req = urllib2.Request(url,headers=headers)
	respInfo = urllib2.urlopen(req,timeout=15)
	html = getHtmlContent(respInfo)
	#debug(logger,html)
	
	json_data = json.loads(html)
	orders=[]
	section_list = []
	if(json_data.has_key('section_list')):
		section_list=json_data['section_list']
	for section in section_list:
		type = section["type"]
		if(type=="byway_order_info"):
			orders = section["list"]
			break
	return orders
	
def getOrders_432():
	localtime = time.localtime(time.time())
	hour = localtime.tm_hour
	if(hour>=10 and hour<=19):
		one_way_map['route_id']=ROUTE_ID_AFTERNOON1
		updateParmsMap(one_way_map)
		paraStr = urllib.urlencode(one_way_map)
		url = "http://api.didialift.com/beatles/api/route/driver/info?"+paraStr
		orders = getOrdersViaUrl(url)
		return orders
	else:
		one_way_map['route_id']=ROUTE_ID_MORNING1
		updateParmsMap(one_way_map)
		paraStr = urllib.urlencode(one_way_map)
		url = "http://api.didialift.com/beatles/api/route/driver/info?"+paraStr
		orders = getOrdersViaUrl(url)
		return orders
			
def striveOrder(order):
	route_id = order['route_id']
	order_id = order['order_id']
	
	# put time and sig params
	updateParmsMap(strive_para_map)
	strive_para_map['route_id']=route_id
	strive_para_map['order_id']=order_id
	sig = getSig(strive_para_map)
	strive_para_map['sig']=sig

	paraStr = urllib.urlencode(strive_para_map)
	url = "http://api.didialift.com/beatles/api/driver/order/strive?"+paraStr
	req = urllib2.Request(url,headers=headers)
	respInfo = urllib2.urlopen(req,timeout=15)
	html = getHtmlContent(respInfo)
	#debug(logger,html)
	map = json.loads(html)
	return map['errno']=='0' and map['errmsg']=='OK'
	

if __name__ == '__main__':
	try:
		send_mail(['358275018@qq.com'],'didi catcher starts','didi catcher starts')
	except Exception,e:
		pass
	
	log_path = os.path.dirname(os.path.realpath(__file__))
	if not os.path.exists(log_path):
		os.makedirs(log_path)
	logger = getPyLogger('didi','debug',os.path.join(log_path,os.path.basename(__file__)+'.log'),'d',1,99999)
	
	debug(logger,'start to work...')
	while(1):
		try:
			#从坚果云中LOAD最新的参数
			loadTimeConfig()

			debug(logger,'FLOW: get my orders')
			orders = getOrders_432()
			debug(logger,'FLOW: GOT ================='+str(len(orders))+' ==================orders')
			for order in orders:
				departure_time = order["trip_info"]['text_setup_time']
				#route_id = order['route_id']
				order_id = order["order_info"]['order_id']
				from_name = order["trip_info"]['from_name']
				from_address = order["trip_info"]['from_address']
				to_name = order["trip_info"]['to_name']
				to_address = order["trip_info"]['to_address']
				price = order["trip_info"]['price']
				passenger_id = order['user_info']['user_id']
				nick_name = order['user_info']['nick_name']
				
				debug(logger,'FLOW: filter orders')
				debug_content = '%s (%s->%s) price=%s'%(departure_time,from_name,to_name,price) #nick_name
				debug(logger,debug_content)
					
				if(filter(order)):
					debug(logger,'FLOW: strive order')
					striveOrder(order)
					#print 'FOUND **************************************** FOUND'
					content = departure_time.encode('utf8')+' '+from_name.encode('utf8')+' '+to_name.encode('utf8')
					send_mail(['358275018@qq.com'],content,content)
					break;
			time.sleep(10)
		except Exception,e:
			debug(logger,str(e))
			time.sleep(10)
	send_mail(['358275018@qq.com'],'didi chatcher exits','didi chatcher exits')
