#encoding=utf-8

#利用生产者、消费者方法去下载斗图啦的图片
#这里把获取图片的url的函数get_img_url()作为生产者
#把利用图片url下载图片的函数download_img()作为消费者

import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import datetime
import threading


BASE_URL = 'http://www.doutula.com/photo/list/?page='
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

#页面的url列表
PAGE_URL = []
#图片的url列表
IMG_URL = []
#全局锁
gLock = threading.Lock()

for num in range(20):
    url = BASE_URL+str(num+1)
    PAGE_URL.append(url)

def get_img_url():
    global IMG_URL
    while PAGE_URL:
        gLock.acquire()#上锁
        page_url = PAGE_URL.pop()
        gLock.release()#解锁
        try:
            response = requests.get(page_url,headers=headers)
        except:
            pass
        con = response.text
        soup = BeautifulSoup(con, 'lxml')
        pic = soup.find('div', attrs={'class':'page-content'})
        imgs = pic.find_all('img', attrs={'class':'lazy'})
        for item in imgs:
            img_url = item['data-original']
            gLock.acquire()  # 上锁
            IMG_URL.append(img_url)
            gLock.release()  # 解锁

def download_img():
    global IMG_URL
    while True:
        if len(IMG_URL)==0:
            break
        else:
            gLock.acquire()#上锁
            img_url = IMG_URL.pop()
            gLock.release()#解锁
            _name = img_url.split('/')
            name = _name.pop()
            na = name.split('!')
            name = na[0]
            path = os.path.join('images', name)
            urllib.request.urlretrieve(img_url, filename=path)

def main():
    #给生产者三个线程，去获取图片的url
    for item in range(3):
        th = threading.Thread(target=get_img_url)
        th.start()
        th.join()
    # 给消费者五个线程，去下载图片
    for item in range(5):
        th = threading.Thread(target=download_img)
        th.start()
        th.join()


if __name__ == '__main__':
    str_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print("下载用时：", (end_time - str_time).seconds, 's')


