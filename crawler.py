#!/usr/bin/env python


'''
--------------------------------------------------
--------------------------------------------------
 Name:   GeeksForGeeks Article Extractor
 Purpose: To download and save articles filed under each and every tag mentioned in www.geeksforgeeks.org 
 Author: Debapriya Das
 Dept of CSE, NIT Durgapur
 V1.0 - 06.02.2015 - basic implementation

--------------------------------------------------
--------------------------------------------------
'''




import urllib2
import os
import pdfkit
from bs4 import BeautifulSoup



#AllTags = ['payu']

#path = "/home/yodebu/Desktop/GeeksForGeeks_article_extractor/"      # Specify your path here



def ExtractMainLinks(AllTags,path):
	for i in AllTags:
		newpath = path + i 
		if not os.path.exists(newpath):
		  os.mkdir(newpath)
		url = "http://www.geeksforgeeks.org/tag/" + i +"/"
		data = urllib2.urlopen(url).read()
		soup = BeautifulSoup(data)
		allLinks = soup.findAll("h2",class_="post-title")
		listofLinks = []
		for link in allLinks:
			mainLink = str(link.findAll("a")[0]).split("<a href=")[1].split('rel="bookmark"')[0].strip('"').split('"')[0]
			listofLinks.append(mainLink)
		Extract_And_Save_Page_Data(listofLinks,newpath,i)
		


def Extract_And_Save_Page_Data(listofLinks,newpath,i):
	No = 0
	for item in listofLinks:
		pageData = urllib2.urlopen(item).read()
		filePath = newpath +"//" +str(i)+" "+str(No+1)+".html"
		pdfPath = newpath +"//" +str(i)+" "+str(No+1)+".pdf"
		No = No +1
		with open(filePath,"wb") as f:
			f.write(str(pageData))
			



#ExtractMainLinks(AllTags,path)
