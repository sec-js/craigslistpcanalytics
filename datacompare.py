import time

#deletes specific outliers that are listed
def outlierdelete(dict):
	updatedict = {}
	voidlist = ["&amp", "XBOX", "&#39", "Blaster", "quot", "Dance", "Mortal", "140+", "Xbox", "Ornata", "WW2", "Boost", "Flight", "Shifter", "Ematic", "Battlefield", "Game walk", "Cabinet"]
	check = 1
	for key in dict.keys():
		for word in voidlist:
			if word in dict.get(key)[0]:
				check = 0
		if check == 1:
			updatedict[key] = dict.get(key)
		check = 1
	
	return updatedict
	
#if entry in main but not new, sold. if entry in new but not main, new item. if in both, still for sale.
def compare(maindict, newdict, soldlist, currentdate):
	maindict, lst = findsold(maindict, newdict, soldlist, currentdate)
	maindict = addnew(maindict, newdict)
	
	return maindict, lst
	
#finds sold items and puts them into a list. Removes the sold items from the main dictionary
def findsold(maindict, newdict, lst, currentdate):
	check = 1
	for main in maindict.keys():
		if newdict.get(main) is None:
			tmp = maindict.get(main)
			lst.append((tmp[0], int(tmp[1]), tmp[2], int(tmp[3]), currentdate))
			maindict.pop(main)
			
	return maindict, lst
	
#adds new entries to the main dictionary
def addnew(maindict, newdict):
	for new in newdict.keys():
		if maindict.get(new) is None:
			maindict[new] = newdict.get(new)
	
	return maindict
