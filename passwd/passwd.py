#!/usr/bin/python
###################################################################################################################################
## Author             : whf307
## Created            : 2018-01-09
## Mail               : whf307@gmail.com
## Website            : https://whf307.github.io
## Platform           : Linux
## Python             : 2.7\3.6
## How to use         : chmod +x passwd.py   &&  ./passwd.py 
## About the scripts  : To generate a strong password with 2 digital , 2 capital letters ,2 small letters and 2 special character
###################################################################################################################################

#difine the base char to use
dig=['0','1','2','3','4','5','6','7','8','9']
char1=['~','!','#','$','^','&','*','(',')','_','+']
char2=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
char3=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

import sys
import random

#genereate digital for each position
d1=random.randint(0,9)
d2=random.randint(0,9)
d3=random.randint(0,10)
d4=random.randint(0,10)
d5=random.randint(0,25)
d6=random.randint(0,25)
d7=random.randint(0,25)
d8=random.randint(0,25)

passwd1=[]
passwd1.append(dig[d1])
passwd1.append(dig[d2])
passwd1.append(char1[d3])
passwd1.append(char1[d4])
passwd1.append(char2[d5])
passwd1.append(char2[d6])
passwd1.append(char3[d7])
passwd1.append(char3[d8])

#shuffle the items
items = [0,1,2,3,4,5,6,7]
random.shuffle(items)

#combine again
passwd=''.join(passwd1[items[0]])+''.join(passwd1[items[1]])+''.join(passwd1[items[2]])+''.join(passwd1[items[3]])+''.join(passwd1[items[4]])+''.join(passwd1[items[5]])+''.join(passwd1[items[6]])+''.join(passwd1[items[7]])

#print the final password
if sys.version[0:1] >= "3":
	eval('print (passwd)')
else:
	eval('print passwd')


