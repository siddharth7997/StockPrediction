# this is a python3 program which was made by my friend Vishal Anand Chenna.
# to run it python3 parse.py



import time
import feedparser
import sys
import codecs

company = input('Please enter company: ')
market = input('Please enter market: ')
d = feedparser.parse('https://finance.google.com/finance/company_news?q='+market+'%3A'+company+'&'+'&ei=579dWvmiEYavuAS3x7rIAg&output=rss&num=1000')






#https://finance.google.com/finance/company_news?q=NASDAQ%3AGOOGL&ei=579dWvmiEYavuAS3x7rIAg&output=rss&num=500







file = open(company+'.csv','wb')
for i in d.entries:
	date_p = i.published_parsed
	date = time.strftime("%d.%m.%Y", date_p)
	line = i.title+', '+date
	file.write((line).encode('utf=8'))
	file.write('\n'.encode("utf-8"))
file.close()		
