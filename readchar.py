#!/usr/bin/env python3
# file: 'readchar.py'
"""
Provides readchar()
Implementation of a way to get a single character of input
without waiting for the user to hit <Enter>.
(OS is Linux, Ubuntu 14.04)
"""

import tty, sys, termios

class ReadChar():
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

def readchar():
    with ReadChar() as rc:
        return rc

def testrc():
    print\
    ("Testing ReadChar: enter a character and we'll report what it is.")
    while True:
        char = readchar()
        if ord(char) <= 32:
            print("You entered character with ordinal {}, aka {}."\
                        .format(ord(char), repr(char)))
        else:
            print("You entered character '{}'."\
                        .format(char))
        if char in "":
            break

if __name__ == "__main__":
    testrc()

