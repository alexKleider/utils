#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8 :
# Copyright 2014 Alex Kleider
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#   Look for file named COPYING.
#
# file: 'sort_file.py'
"""
sort_file.py sorts file content.
It expects one or two parameters.
The first is the name of the file, who's contents are to be sorted.
The second which defaults to 'sorted', is the name of the output.
All words in the source file will appear sorted in the output file
one word per line.
In the end of an error condition, a string describing the error is
returned.

Usage:
  sort.py INFILE [OUTFILE]

Options:
  OUTFILE  [default: sorted]
"""

import docopt

DEFAULT_OUTFILE = 'sorted'

args = docopt.docopt(__doc__)

if not args['OUTFILE']:
    args['OUTFILE'] = DEFAULT_OUTFILE

# print(args)

def sort_file(fileID, sorted_file_ID = DEFAULT_OUTFILE):
    try:
        with open(fileID) as f:
            words = f.read().split()
            words.sort()
    except FileNotFoundError:
        return "Input file not found."
    try:
        with open(sorted_file_ID, 'w') as out_file:
            out_file.write('\n'.join(words))
    except PermissionError:
        return "Lack permission to open output file."
    except FileNotFoundError:
        return "Can not open output. Probably no such directory."


if __name__ == "__main__":
    if args:
        sort_file(args['INFILE'], args['OUTFILE'])
    else:
        print("No argument(s) provided.")

