import feedparser

d = feedparser.parse('https://www.google.com/finance/company_news?q=NASDAQ:MSFT&ei=CLh5WfiQF4KKuwTa47i4CQ&output=rss&num=100')

for i in range(100):
	print i,d['entries'][i]['title']