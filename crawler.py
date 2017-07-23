#!/usr/bin/python
# coding: utf-8

import sys, os
import socket, socks
###################################################################
# Uncomment this 2 lines to do the requests under TOR network.    #
#                                                                 #
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)#
#socket.socket = socks.socksocket                                 #
#                                                                 #
# Warning, with the option --dir the requests are (very long)     #
# Do not use that to dir-brute a website                          #
###################################################################
import random
import requests
from urllib2 import *
from optparse import *
import re
import time

# --> colors
R = "\033[91m"
O = "\033[0m"
G = "\033[32m"
Y = "\033[93m"
B = "\033[94m"
BOLD = "\033[1m"
ERROR = R + "[-] " + O
PASS = G + "[+] " + O
INFO = B + "[!] " + O
MED = Y + "[~] " + O

def help():
	print '''\033[1;94mSimple web crawler in python written by OnixIs.\033[0m
\033[1mOptions:\033[0m
    [-u] www.google.com -- Specify URL.
    [--crawl] -- Enable crawling mode.
    [--dir] -- Enable dirbruter mode.
    [--all] -- Launch crawling and brute force modes.
    [--random-agent] -- Use random user agents.
\033[1mUsage:\033[0m
    ./crawler.py [-u] www.google.com
    ./crawler.py [-u] www.google.com [--crawl]
    ./crawler.py [-u] www.apple.com [--dir]
    ./crawler.py [-u] www.microsoft.com [--all]
    ./crawler.py [-u] www.microsoft.com [--dir] [--random-agent]
\033[1mVersion: 1.0\033[0m'''

def randomagent():
	global usera
	usera = []
	usera.append("Opera/8.51 (Windows NT 5.0; U; en)")
	usera.append("Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0")
	usera.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27")
	usera.append("Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8) Gecko/20060118 Firefox/1.5")
	usera.append("Opera/9.63 (Macintosh; Intel Mac OS X; U; en) Presto/2.1.1")
	return usera

def hostinfos(URL):
	IP = socket.gethostbyname(URL)
	print INFO + "URL to scan : "+ URL
	print INFO + "Server IP : "+ IP + "\n"

def dirbrute(URL, agent, https):
	print PASS + "Starting brute mode."
	print PASS + "The URL is under scan."
	print INFO + "The scan can take several minutes."
	t = 6768
	if agent == True:
		print INFO + "Requests under random User-agent.\n"
	else:
		print INFO + "Base User-Agent -- {'User-Agent': 'OnixIs/:)'}\n"

	wordlist = "/usr/share/webkit/wordlist"
	with open(wordlist, "r") as checks:
		for i in checks.readlines():
			DIR = i.strip("\n")
			try:
				link = "http://" + URL+"/"+DIR
				if https == True:
					link = "https://" + URL + "/" + DIR

				if agent == True:
					req = Request(link, headers={'User-Agent': random.choice(usera)})
				else:
					req = Request(link, headers={'User-Agent': 'OnixIs/:)'})
				urlopen(req)
				print G + "[+]"+ O +" Directory found "+URL+"/"+DIR
				t = t - 1
			except HTTPError:
				t = t - 1
				pass
			sys.stdout.write(INFO + str(t) +" remaining tests\r")
			sys.stdout.flush()
			#sys.stdout.write(INFO + "Elapsed time "+time.strftime("%M:%S")+"\r")
			#sys.stdout.flush()

	if https == True:
		r = requests.get("https://" + URL+ "/robots.txt")
	else:
		r = requests.get("http://" + URL + "/robots.txt")

	if r.status_code == 200:
		print PASS + "Display robots.txt content."
		re = urlopen("https://" + URL + "/robots.txt")
		t = re.read()
		print t

def crawl(URL, agent, https):
	opener = build_opener()
	if agent == True:
		print INFO + "Requests under random User-agent.\n"
		opener.addheaders = [('User-agent', random.choice(usera))]
	else:
		print INFO + "Base User-Agent -- {'User-Agent': 'OnixIs/:)'}\n"
		opener.addheaders = [('User-agent', 'OnixIs/:)')]

	link = "http://" + URL
	if https == True:
		link = "https://" + URL ## Simple security.

	out = opener.open(link)

	## Reading html code to find URLs. ##

	read = str(out.read())
	extln = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', read)
	out = list(set(extln))
	num = len(out)
	num = str(num)
        OUTPUT = "/usr/share/webkit/report.txt"
	w = open(OUTPUT, "a")
	w.write("\n\n\nReport crawler "+time.strftime("%A %d %B %Y %H:%M:%S")+" :\n")
	w.write("\n")

	for i in out:
		print PASS + "Found URL : "+i
		w.write("\nFound URL : "+i)


	## Searching .css or .js files and images ##

	css = re.findall('href="?\'?([^"\'>]*)', read)
	out2 = list(set(css))
	for i in out2:
		if str('.css') in i:
			print PASS + "Found CSS code : "+i
			w.write("\nFound CSS code : "+i)

	js_img = re.findall('src="?\'?([^"\'>]*)', read)
	out3 = list(set(js_img))
	
	for i in out3:
		if str('.js') in i:
			if "https://" in i:
				print PASS + "Found external JS link : "+i
				w.write("\n\nFound external JS link : "+i)
			elif "http://" in i:
				print PASS + "Found external JS link : "+i
				w.write("\nFound external JS link : "+i)
			else:
				print PASS + "Found internal JS code : "+i
				w.write("\nFound internal JS code : "+i)


	for i in out3:
		if str('.gif') in i:
			print PASS + "Found image : "+i
			w.write("\n\nFound image : "+i)
		elif str('.jpg') in i:
			print PASS + "Found image : "+i
			w.write("\nFound image : "+i)
		elif str('.jpeg') in i:
			print PASS + "Found image : "+i
			w.write("\nFound image : "+i)
		elif str('.png') in i:
			print PASS + "Found image : "+i
			w.write("\nFound image : "+i)


	print MED + "Found "+num+" true URLs."
	w.write("\n\nFound "+num+" true URLs.\n\n")

	print INFO + "Report save on this directory as 'report.txt'."
	print PASS + "Scan finished at "+time.strftime("%H:%M:%S")

# def htmlcopy(URL):

def main():
	parser = OptionParser(add_help_option=False)
	parser.add_option("-h", dest="help", action="store_true", help="help option.")
	parser.add_option("-u", dest="url", help="Specify your url.")
	parser.add_option("--crawl", action="store_true")
	parser.add_option("--dir", action="store_true")
	parser.add_option("--all", action="store_true")
	parser.add_option("--random-agent", dest="useragent", action="store_true")

	(options, args) = parser.parse_args()

	URL = options.url

	if not (options.help or options.url):
		print ERROR + "Not enough options."
		print ERROR + "Type './crawler -h' to see available options."

	elif options.help:
		help()

	elif options.url:
	    ## URL settings // Your http or https url is not compatible with urllib2
		## when you complete the request, so i will solve that for you :)
		https = False
		if "http://" in URL:
			print ERROR + "Invalid URL."
			print MED + "Replacing URL to avoid URLError. [-http]\n"
			URL = URL.replace("http://", "")
		elif "https://" in URL:
			https = True
			print ERROR + "Invalid URL."
			URL = URL.replace("https://", "")
			print MED + "Replacing URL to avoid URLError. [-https]\n"
		
		## www.test.com/ -- '/' is not compatible too so i solve that :)
		if "/" in URL:
			URL = URL.replace("/", "")
		## END ##
		
		## Display server IP
		hostinfos(URL)

		if options.crawl:
			if options.useragent:
				randomagent()
				agent = True
				crawl(URL, agent, https)
				sys.exit()
			
			agent = False
			crawl(URL, agent, https)
			sys.exit()

		elif options.dir:
			if options.useragent:
				randomagent()
				agent = True
				dirbrute(URL, agent, https)
				sys.exit()
			
			agent = False
			dirbrute(URL, agent, https)
			sys.exit()
			
		elif options.all:
			if options.useragent:
				agent = True
				randomagent()
				dirbrute(URL, agent, https)
				print INFO + "Starting crawl mode !"
				time.sleep(1.5)
				crawl(URL, agent, https)
				sys.exit()
			
			agent = False
			randomagent()
			dirbrute(URL, agent, https)
			print INFO + "Starting crawl mode !"
			time.sleep(1.5)
			crawl(URL, agent, https)
			sys.exit()
        
        #print ERROR + "Not enough options!"
        #sys.exit()

if __name__ == '__main__':
	if os.geteuid() != 0:
		print ERROR + "You need to run the program with root privileges."
		sys.exit()
	else:
		try:
			main()
		except KeyboardInterrupt:
			sys.exit(ERROR + "KeyboardInterrupt")

