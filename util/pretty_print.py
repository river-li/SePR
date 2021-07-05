#!/usr/bin/env python

def log(content, color):
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    PURPLE = "\x1b[35m"
    CYAN = "\x1b[36m"
    NORMAL = "\x1b[0m"

    print(eval(color) + content + NORMAL)


def error(content):
    log('[-] ' + content, 'RED')


def success(content):
    log('[+] ' + content, 'GREEN')
