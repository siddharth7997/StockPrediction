import time
import feedparser
import sys
import codecs

company = input('Please enter company: ')
market = input('Please enter market: ')
d = feedparser.parse('https://www.google.com/finance/company_news?q='+market+':'+company+'&daterange:'+'2014-09-09'+'..'+'2017-09-09'+'&ei=oaGGWeCyONbGugSh66CoDg&output=rss&num=500')

file = open(company+'.csv','wb')
for i in d.entries:
	date_p = i.published_parsed
	date = time.strftime("%d.%m.%Y", date_p)
	line = i.title+', '+date
	file.write((line).encode('utf=8'))
	file.write('\n'.encode("utf-8"))
file.close()		
