from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
def getTitle(url):
	try:
		html = urlopen(url)
	except HTTPError as e:
		return None
	try:
		bsObj = BeautifulSoup(html.read(), "lxml")#读取网页，不加"lxml"会有警告
		title = bsObj.body.h1#根据需要选择网页标签内的内容
	except AttributeError as e:
		return None
	return title
title = getTitle("http://www.pythonscraping.com/pages/page1.html")
if title == None:
	print("Title could not be found")
else:
	print(title)