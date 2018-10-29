import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import datetime

URL = 'http://www.doutula.com/zz/list?page='
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
			imgg = item.img
			img_url = imgg['data-original']
			save(img_url)

def save(img_url):
	_name = img_url.split('/')
	name = _name.pop()
	path = os.path.join('images',name)
	urllib.request.urlretrieve(img_url,filename=path)

if __name__ == '__main__':
	num = input('请输入要下载的页数：')
	str_time = datetime.datetime.now()
	get_pic_url(int(num))
	end_time = datetime.datetime.now()
	print("下载用时：",(end_time-str_time).seconds,'s')
