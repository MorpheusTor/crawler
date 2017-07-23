# coding: utf-8

import os

def unistall():
	print "let's unistall the program...."

	os.system("sudo rm -rf /usr/share/webkit")
	print "'/usr/share/webkit' removed."
	os.system("sudo rm /usr/bin/crawler")
	print "'/usr/bin/crawler' removed."
	print "All the program are unistalled."

if __name__ == '__main__':
	unistall()