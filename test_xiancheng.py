#测试多线程
import time
import threading
import datetime

def main(i):
    print("hello world!-->%d"%i)
    time.sleep(2)


#单线程执行（线性执行）
def dan():
    for i in range(5):
        main(i)

def duo():
    for i in range(5):
        th = threading.Thread(target=main,args=[i])
        th.start()

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    dan()
    end_time = datetime.datetime.now()
    print("线性执行时间：", (end_time - start_time).seconds, 's')
    start_time = datetime.datetime.now()
    duo()
    end_time = datetime.datetime.now()
    print("多线程执行时间：", (end_time - start_time).seconds, 's')

