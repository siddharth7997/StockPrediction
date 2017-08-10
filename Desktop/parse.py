import time
import feedparser
import sys
import codecs

company = input('Please enter company: ')
d = feedparser.parse('https://www.google.com/finance/company_news?q=NASDAQ:'+company+'&ei=oaGGWeCyONbGugSh66CoDg&output=rss&num=500')

file = open(company+'.csv','wb')
for i in d.entries:
	date_p = i.published_parsed
	date = time.strftime("%d.%m.%Y", date_p)
	line = i.title+', '+date
	file.write((line).encode('utf=8'))
	file.write('\n'.encode("utf-8"))
file.close()		
