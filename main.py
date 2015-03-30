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
from optparse import OptionParser

import crawler
from crawler import *



def parse_options():
  usage = "usage: prog [options] (arg1, arg2, ... argn)"
  parser = OptionParser(usage=usage)
  
  parser.add_option("-t", "--tag1", \
		      type="string", \
		      action="store", \
		      dest="inp_tag1", \
		      default = "", \
		      help="input tags for downloading from the website")


  parser.add_option("-u", "--tag2", \
		      type="string", \
		      action="store", \
		      dest="inp_tag2", \
		      default = "", \
		      help="input tags for downloading from the website")

  parser.add_option("-v", "--tag3", \
		      type="string", \
		      action="store", \
		      dest="inp_tag3", \
		      default = "", \
		      help="input tags for downloading from the website")
		      
  parser.add_option("-l", "--location", \
		      type="string", \
		      action="store", \
		      dest="inp_location", \
		      default = "/home/yodebu/Desktop/GeeksForGeeks_article_extractor/", \
		      help="location where downloaded files willl be stored")
		      		      	      
  opts, args = parser.parse_args()
  return opts, args



##-----------------------------------------------------

# main function

def main():  
  # parse the input parameters
  opts, args = parse_options()
  AllTags = [opts.inp_tag1, opts.inp_tag2, opts.inp_tag3]
  path = opts.inp_location    
  ExtractMainLinks(AllTags,path)


if __name__ == "__main__": main()
