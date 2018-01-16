# this is a python3 program which was made by my friend Vishal Anand Chenna.
# to run it python3 test1.py





from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
print('Enter company name')
com = input()
f = open(com + '.csv', 'r')   #Opening the company file with news titles
fp = open(com + '1.csv', 'w')
for line in f:  #Calculating sentiment score for each title in the file
	d=','
	l = line.split(d)   #Splitting each line from the file with comma as delimiter
	s = ""
	for i in range (len(l)-1):  #Joining the title back without the date
		s = s+l[i]+d
	vs = analyzer.polarity_scores(s[:len(s)-1]) #Calculating the sentiment
	#print(s[:len(s)-1])
	dic = dict(vs)  #Converting the sentiment results into dictionary
	dic.pop('compound') #Removing compund key from the dictionary
	tup = dic.items()  #Creating a tuple from the dictionary items
	m = ('lel', 0)  
	for i in tup:   #Finding the tuple with maximum value on sentiment
		if(i[1] == 1 and i[0] == 'neu'):
			m = i
		if(i[1] > m[1] and i[0] != 'neu'):
			m = i		
	#Adding one or two to the max sentiment for easy normalisation depending on the emotion
	n = ['mew', 0]
	if m[0] == 'pos':   
		n[1] = m[1]
		n[0] = m[0]
	elif m[0] == 'neu':
		n[1] = m[1] - 1 
		n[0] = m[0] 
	else:
		n[1] = -m[1]
		n[0] = m[0]
	fp.write(str(n[1]) + ', ' + l[len(l) - 1])
	
