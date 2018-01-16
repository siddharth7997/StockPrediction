#this is a python3 program which was made by my friend.
# to run it python3 list.py


from datetime import date
from datetime import timedelta

t = timedelta(days = 1)
month = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
print('Enter company name')
com = input()
f = open(com + '1.csv', 'r')
fo = open('semantic.csv', 'w')
l = []
d = []
fo.write("Date" + ', ' + "Semantic")
fo.write('\n')
for i in f:
	li, di = i.split(', ')
	da = list(map(int, di.split('.')))
	dat = date(da[2], da[1], da[0])
	l.append(float(li))
	d.append(dat)
lenlist = len(l)
for i in range(lenlist-1):
	for j in range(lenlist - i - 1):
		if(d[j] > d[j + 1]):
			c = d[j]
			d[j] = d[j + 1]
			d[j+1] = c
			m = l[j]
			l[j] = l[j + 1]
			l[j + 1] = m
for i in range(lenlist):
	print(l[i], d[i])


curdate = d[0]
lol1 = []
lol2 = []
sc = 2
i = 0
while(curdate <= d[lenlist - 1]):
	sc = 0
	dtt = (str(curdate)).split('-')
	c = 0
	for i in range(lenlist):
		if(curdate == d[i]):
			sc = sc + l[i]
			c = c + 1
	if(c == 0):
		fo.write(dtt[2] + '-' + month[int(dtt[1])] + '-' + dtt[0][2:] + ', 0.0')
		fo.write('\n')
	else:
		fo.write(dtt[2] + '-' + month[int(dtt[1])] + '-' + dtt[0][2:] + ', '+str(sc / c))
		fo.write('\n')
	curdate = curdate + t




