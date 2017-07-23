# coding: utf-8

import os

# --> colors
O = "\033[0m"
G = "\033[32m"
Y = "\033[93m"
B = "\033[94m"
PASS = G + "[+] " + O
INFO = B + "[!] " + O


def setup():
	print PASS + "Let's install the tool :)"
	try:
		import socks
	except ImportError:
		print ERROR + "Module socks not installed."
		print INFO + "Installing socks module....."
		os.system("sudo apt update && sudo apt install python-socks")

	print PASS + "Module socks installed."

	print INFO + "Installing TOR....."
	os.system("sudo apt install tor && sudo service tor restart")
	print PASS + "TOR setting up."

	print INFO + "Copying program to '/usr/bin/crawler'"
	os.system("sudo cp crawler.py /usr/bin/crawler && sudo chmod 0755 /usr/bin/crawler")

	print INFO + "Make directory at '/usr/share/webkit/' & copying the wordlist."
	os.system("sudo mkdir /usr/share/webkit && sudo cp wordlist /usr/share/webkit/wordlist")
	print INFO + "Files are stocked at '/usr/share/webkit/'"
	print INFO + "Please type 'crawler -h' to see how to use it :)"

if __name__ == '__main__':
	try:
		setup()
	except KeyboardInterrupt:
		sys.exit(ERROR + "KeyboardInterrupt")