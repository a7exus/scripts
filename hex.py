#!/usr/bin/python

f=open("1",'rb')
n=0
while True:
	b=f.read(1)
	if not b: break
	print '%2.2X'%ord(b),
	n+=1
	if n>15:
		print 
		n=0