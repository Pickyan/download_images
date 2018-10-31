#encoding=utf-8

import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import datetime
import threading

URL = 'http://www.doutula.com/photo/list/?page='
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

def get_pic_url(PAGE_NUM):
	for page_num in range(1,PAGE_NUM+1):
		url = URL+str(page_num)
		try:
			response = requests.get(url,headers=headers)
		except:
			print("重新获取url")
			continue
		page = response.content
		soup = BeautifulSoup(page,'lxml')
		pic = soup.find('div',attrs={'class':'page-content'})
		aa = pic.find_all('a')
		for item in aa:
			imgg = item.find('img',attrs={'class':'lazy'})
			img_url = imgg['data-original']
			th = threading.Thread(target=save, args=[img_url])#10个页面680个图片，用时3秒
			th.start()


def save(img_url):
	_name = img_url.split('/')
	name = _name.pop()
	na = name.split('!')
	name = na[0]
	path = os.path.join('images',name)
	urllib.request.urlretrieve(img_url,filename=path)




if __name__ == '__main__':
	num = input('请输入要下载的页数：')
	str_time = datetime.datetime.now()

	#多线程执行
	# th = threading.Thread(target=get_pic_url,args=[int(num)])
	# th.start()
	# th.join()
	get_pic_url(int(num))#测试1：线性执行程序下载10页用时58秒，多线程下载10页用了55(结果：与想象不符)
			     #测试2：调用save()也加上了多线程，下载10页用时3秒
			     #测试3：调用get_pic_url()使用线程执行，save()执行多线程下载10页用时3秒

	end_time = datetime.datetime.now()
	print("下载用时：",(end_time-str_time).seconds,'s')
