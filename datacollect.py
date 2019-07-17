import sys
import time
from datacompare import *

def createdict(filename, currenttime):
	dict = {} 
	holdname, holddate, holdprice, holdline = "", "", "", ""
	pid, check = 0, 0
	
	#reading the file
	file = open(filename, "r")
	for line in file:
		if "ban nearby" in line:
			break
			
		if "data-id" in line and "data-ids" not in line: #gets data id and name
			pid = getpid(line)
			holdname = cut(line)
			check += 1
			
		if "<time class=\"result-date\"" in line:  #gets post date
			holddate = cut(line)
			check += 1
			
		if "result-price" in line and line not in holdline: #gets price
			holdprice = cut(line)
			holdprice = holdprice[1:]
			
			check += 1
			holdline = line
		
		if check == 3:
			if dict.get(pid) is None:
				dict[pid] = (holdname,int(holdprice),holddate,0)
			check = 0
			
			
	#method calls
	countdays(dict, currenttime)
	dict = outlierdelete(dict)
	file.close()
	return dict
		
			
def countdays(dict, currenttime):
	for key in dict.keys():
		daysrun = 0
		if "Apr" in dict.get(key)[2]:
			truetime = dict.get(key)[2].replace("Apr ", "4")
		elif "May" in dict.get(key)[2]:
			truetime = dict.get(key)[2].replace("May ", "5")
		elif "Jun" in dict.get(key)[2]:
			truetime = dict.get(key)[2].replace("Jun ", "6")
			
		truetime = truetime.replace(" ", "")
		
		if truetime[0] == currenttime[0]:
			daysrun = int(currenttime[2:]) - int(truetime[1:])
		else:
			if truetime[0] == "4" and currenttime[0] == "5":
				daysrun = int(currenttime[2:]) - int(truetime[1:]) + 30
			elif truetime[0] == "4" and currenttime[0] == "6":
				daysrun = int(currenttime[2:]) - int(truetime[1:]) + 61
			elif truetime[0] == "5" and currenttime[0] == "6":
				daysrun =  int(currenttime[2:]) - int(truetime[1:]) + 31
				
		tmp = (dict.get(key)[0], dict.get(key)[1], dict.get(key)[2], daysrun)
		dict[key] = tmp
		
def getpid(line):
	index = line.find("data-id")
	return int(line[index+9:index+19])

def cut(line):
	index = line.find(">")
	temp1 = line[index+1:]
	index2 = temp1.find("<")
	return temp1[:index2]
		