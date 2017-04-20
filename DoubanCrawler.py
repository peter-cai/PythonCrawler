#coding=utf-8
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import pdb
import csv

num = 0  #用来计数，计算爬取的书一共有多少本
start_time = time.time()  #计算爬虫爬取过程时间

#第一页网页网址https://read.douban.com/columns/category/all?sort=hot&start=0
#第二页网页网址https://read.douban.com/columns/category/all?sort=hot&start=10
#第三页网页网址https://read.douban.com/columns/category/all?sort=hot&start=20
#以此类推，0，10，20，30，40，……
url = 'https://read.douban.com/columns/category/all?sort=hot&start='  
csvFile = open("./bookCollect.csv", 'wt', newline="", encoding='utf-8')
writer = csv.writer(csvFile)
writer.writerow(['序号','书名','作者','类型'])
i = 0
#for i in range(0,1000,10):  #这里的  range（初始，结束，间隔）
judgement = 'n'
while(judgement == 'n'):    
    #urllib.request库用来向该网服务器发送请求，请求打开该网址链接
    try:
        html = urlopen('https://read.douban.com/columns/category/all?sort=hot&start=%d' % i)    
    #BeautifulSoup库解析获得的网页，第二个参数一定记住要写上‘lxml’，记住就行
        bsObj = BeautifulSoup(html,'lxml') 
        print('==============' + '第%d页'%(i/10 + 1) + '==============')        
        print('序号','    ','书名/作者/类型')
        contentList = bsObj.findAll('h4')#获取h4标签内的a标签，但这里返回是只含1个元素的list
        contentList = bsObj.find("div",{'class':'bd'}).contents[0]
        for item in contentList:
            num = num + 1
            #pdb.set_trace()
            bookName = item.h4.contents[0].contents[0] #contents将子节点列表输出
            author = item.find("div",{"class","author"}).contents[1].contents[0]
            bookCategory = item.find("div",{"class","category"}).contents[1].replace('\n','')
            try:
                print('%04d'%num, bookName, '/', author, '/', bookCategory)
                writer.writerow(['%04d'%num, bookName, author, bookCategory])
            except Exception as e:
                print('%04d'%num, "book's name not be found")
                writer.writerow(['%04d'%num, "book's name not be found"])
            
    except HTTPError as e:
	    writer.writerow(['The page can not be opened'])
    #设置抓数据停顿时间为1秒，防止过于频繁访问该网站，被封
    
    print("--")
    print("Whether to continue? ['n': next page, 's': stoping the program]")
    keyInput = input("Please enter your input (default: 'n'):")
    if keyInput == '' or keyInput == 'n':
        judgement = 'n'
    else:
        judgement = 's'
    i = i + 10
    time.sleep(0.5) 
csvFile.close()
end_time = time.time()
duration_time = end_time - start_time
print('运行时间共：%.2f'  % duration_time + '秒')
print('共抓到%d本书名'%num, '详细内容见 bookCollect.csv')