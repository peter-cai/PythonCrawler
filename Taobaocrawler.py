import os
import threading
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import socket
from multiprocessing import Pool 
# 由于urllib在获取网络信息经常出现timeout错误，下两行是网友推荐方法，但效果貌似不明显
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

# phantomjs浏览器的位置，需要提前安装好，并将路径添加到环境变量
browserPath = 'D:\\desktop\\python\\phantomjs-2.1.1-windows\\bin\\phantomjs'
# 爬虫主页面
homePage = 'https://mm.taobao.com/search_tstar_model.htm?'
outputDir = 'photo/'
# 网页解析器，之前是'html5lib'会出错，改成'lxml'就没事了
parser = 'lxml'

def main():
    driver = webdriver.PhantomJS(executable_path=browserPath)  #浏览器的地址
    driver.get(homePage)  #访问目标网页地址
    bsObj = BeautifulSoup(driver.page_source, parser)  #解析目标网页的 Html 源码
    print("[*]OK GET Page")
    girlsList = driver.find_element_by_id('J_GirlsList').text.split(
        '\n')  #获得主页上所有妹子的姓名、所在城市、身高、体重等信息
    imagesUrl = re.findall('\/\/gtd\.alicdn\.com\/sns_logo.*\.jpg',
                           driver.page_source)  #获取所有妹子的封面图片
    girlsUrl = bsObj.find_all(
        "a",
        {"href": re.compile("\/\/.*\.htm\?(userId=)\d*")})  #解析出妹子的个人主页地址等信息
    # 所有妹子的名字地点
    girlsNL = girlsList[::3]
    # 所有妹子的身高体重
    girlsHW = girlsList[1::3]
    # 所有妹子的个人主页地址
    girlsHURL = [('http:' + i['href']) for i in girlsUrl]
    # 所有妹子的封面图片地址
    girlsPhotoURL = [('https:' + i) for i in imagesUrl]
    # zip函数接受0个或多个序列作为参数，返回一个tuple列表，第n次从各个序列分别取第n个作为tuple
    girlsInfo = zip(girlsNL, girlsHW, girlsHURL, girlsPhotoURL)
    gitlsDeff = []  
    for item in girlsInfo:
        gitlsDeff.append(item) 
    # pool函数来实现多线程，线程数看计算机性能，多线程效率大大提升
    pool = Pool()
    pool.map(downloadimages, gitlsDeff)
    pool.close()
    pool.join()
    driver.close()

def downloadimages(item):
    girlNL = item[0]    #  姓名地址    
    girlHW = item[1]    #  身高体重 
    girlHURL = item[2]  #  个人主页地址 
    girlCover = item[3] #  封面图片   
    print("[*]Girl :", girlNL, girlHW)
    # 为妹子建立文件夹
    mkdir(outputDir + girlNL)
    print("    [*]saving...")
    # 获取妹子封面图片
    data = urlopen(girlCover).read()
    with open(outputDir + girlNL + '/0_cover.jpg', 'wb') as f:
        f.write(data)
    print("    [+]Loading Cover... ")
    # 获取妹子个人主页中的图片
    getImgs(girlHURL, outputDir + girlNL)


def mkdir(path):
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print("    [*]新建了文件夹", path)
        # 创建目录操作函数
        os.makedirs(path)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print('    [+]文件夹', path, '已创建')


def getImgs(url, path):    
    driver = webdriver.PhantomJS(executable_path=browserPath)    
    # 设置读取时间，防止程序卡住
    socket.setdefaulttimeout(15)
    try:
         driver.get(url)
    except socket.timeout:
        pass
        #send ESCAPE key to browser
    print("    [*]Opening...")
    bsObj = BeautifulSoup(driver.page_source, parser)
    #获得模特个人页面上的艺术照地址
    imgs = bsObj.find_all("img", {"src": re.compile(".*\.jpg")})
    for i, img in enumerate(imgs[1:]):  #不包含与封面图片一样的头像
        try:
            html = urlopen('https:' + img['src'])
            data = html.read()
            fileName = "{}/{}.jpg".format(path, i + 1)
            print("    [+]Loading...", fileName)
            socket.setdefaulttimeout(15)
            try:
                with open(fileName, 'wb') as f:
                    f.write(data)
            except socket.timeout:
                pass
        except Exception:
            print("    [!]Address Error!")
    driver.close()


if __name__ == '__main__':
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    main()
