from datacollect import *
from datacompare import *
from analysis import *
import sys
import argparse

def main():
	maindict = {} #{pid: (name, price, post date, days run), ...}
	soldlist = [] #[(name, price, post date, days run, sell date), ...]
	
	parser = argparse.ArgumentParser()
	parser.add_argument("filename", help="Give the filename")
	parser.add_argument("currentdate", help="Give the current date. (May 7 = 5/7, June 27 = 6/27)")
	parser.add_argument("-d", "--dictionary", action="store", dest="dictionary", default="", help="Get existing dict file for reading")
	parser.add_argument("-s", "--sold", action="store", dest="soldlist", default="", help="Get existing list file for reading")

	args = parser.parse_args()
	if args.dictionary != "" and args.soldlist != "":
		maindict = rdictionary(args.dictionary)
		soldlist = rslist(args.soldlist)
		newdict = createdict(args.filename, args.currentdate)
		maindict, soldlist = compare(maindict, newdict, soldlist, args.currentdate)
		
		exportdict(maindict) #save dictionary state
		exportsoldlist(soldlist) #save sold list state
	else:	
		maindict = createdict(args.filename, args.currentdate)
		exportdict(maindict)
		
	#output
	qualoutput(maindict)
	qualoutputlist(soldlist)
	
	
def rdictionary(filename): #read existing dictionary
	dict = {}
	file = open(filename, "r")
	for line in file:
		tmparr = line.split("|")
		dict[int(tmparr[0])] = (tmparr[1], int(tmparr[2]), tmparr[3], int(tmparr[4]))
		
	file.close()
	return dict
	
def rslist(filename): #read existing sold list
	slist = []
	file = open(filename, "r")
	for line in file:
		tmp = line.split("|")
		slist.append((tmp[0], int(tmp[1]), tmp[2], int(tmp[3]), tmp[4]))
	file.close()
	return slist
	
def exportdict(dict):
	f = open("d.txt", "w")
	for key, value in dict.items():
		line = "%d|%s|%d|%s|%d\n" % (key, value[0], value[1], value[2], value[3])
		f.write(line)
	f.close()
	
def exportsoldlist(soldlist):
	f = open("soldlist.txt", "w")
	for entry in soldlist: #each entry will be a 5-tuple containing important information
		line = "%s|%d|%s|%d|%s" % (entry[0], entry[1], entry[2], entry[3], entry[4])
		f.write(line)
	f.close()

def qualoutput(dict):
	ctr = 1
	for value in dict.values():
		print "--- Dictionary Entry " + str(ctr) + " ---"
		print "Name: " + value[0]
		print "Price: $" + str(value[1])
		print "Date Posted: " + value[2]
		print "Days since Posted: " + str(value[3])
		print ""
		ctr += 1
		
def qualoutputlist(list):
	ctr = 1
	print "-------------------------------------------\n"
	for entry in list:
		print "--- Sell List Entry " + str(ctr) + " ---"
		print "Name: " + entry[0]
		print "Price: $" + str(entry[1])
		print "Date Posted: " + entry[2]
		print "Days since Posted: " + str(entry[3])
		print "Day Sold: " + entry[4]
		print ''
		ctr += 1
		
main()
