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
# file: 'tabulate.py'
"""
This module provides the function tabulate().
def tabulate(data,
            max_width = 75,
            max_columns = 0,
            separator = ' ',
            display = None,
            down = False,
            force =0):
    Its single positional argument is an iterable.
    If <display> is provided it must be a function or method used to
    provide a string representation of the elements in the iterable.
    If not provide, elements are assumed to be printable.
    <down> can be set to True if you want the elements to be ordered
    down the columns rather than across each line.
    If max_columns is changed, it will be used as the upper limit of 
    columns used.
    <force> can be used force groupings. In the simplest case,
    use 1 or 2 if you want an odd or even number of elements in each
    row (column if down=True.)  Use 3 if you want them in groups of 3,
    etc. 
"""

import functools

def longest(x, y):
    if len(x) > len(y):
        return x
    else:
        return y

def tabulate(data,
            display = None,
            alignment = '>',
            down = False,
            max_width = 75,
            max_columns = 0,
            separator = ' ',
            force =0,
            usage=False,
            stats=False):
    """Usage: tabulate( data, 
                        display = None,
                        alignment = '>',
                        down = False,
                        max_width = 75,
                        max_columns = 0,
                        separator = ' ',
                        force =0,
                        usage=False,
                        stats=False)

    The single positional argument (<data>) must be an iterable, a
    representation of which will be returned as a string formated
    into tabular form suitable for printing.
    If <display> is provided it must be a function that, when
    provided with a returned element of data, returns a string
    representation.  If not provided, elements are assumed to have
    their own __repr__ and/or __str__ method(s).
    Possible values for <alignment> are '<', '^', and '>'
    for left, center, and right.
    <down> can be set to True if you want the elements to be listed
    down the columns rather than across each line.
    If <max_columns> is changed, it will be used as the upper limit
    of columns used. It is only effective if you specify fewer
    columns than would fit into <max_width> and any <force> 
    specifiction will take precedence. (See next item.)
    <force> can be used to force groupings. If used, an attempt is 
    made to keep items in groups of <force>, either vertically (if
    <down>) or horizontally (if not.)
    If both are specified, and if <force> is possible, <force> takes
    precedence over <max_columns>, otherwise <force> is ignored.
    If <usage> is set to True, the <data> parmeter is ignored and
    this document string is returned.
    If <stats>is set to True, output will show table layout but no table.
    """
    orig_max_col = max_columns
    if usage:
        return tabulate.__doc__
    # Assign <display>:
    if not alignment in ('<', '^', '>'):
        return "Alignmemt specifier not valid: choose from '<', '^', '>'" 
    if not display:
        display = str
    # Map to a representable format:
    data = [display(x) for x in data]
    # Establish length of longest element:
    max_len = len(functools.reduce(lambda x, y: 
                            x if len(x)>len(y) else y, data))
    # Establish how many can fit on a line:
    n_per_line = (
            (max_width + len(separator)) // (max_len + len(separator)))
    # Adjust for max_n_columns if necessary:
    # If <down> then <force> becomes irrelevant but otherwise,
    # force takes precedence over max_columns but within limits
    # of n_per_line.
#   print("max_columns ({}) < n_per_line ({})?"
#           .format(max_columns, n_per_line))
    if down:             # In down mode:
        if (max_columns > 0   # <force> is irelevant to n_per_line.
          and max_columns < n_per_line):
            n_per_line = max_columns
#           print("1. n_per_line is {}.".format(n_per_line))
    else:
        if max_columns < force and force <= n_per_line:
            max_columns = 0
        if force > 1 and n_per_line > force:
            _, remainder = divmod(n_per_line, force)
            n_per_line -= remainder
            forced = True
#           print("2. n_per_line is {}.".format(n_per_line))
        else:
            forced = False
        if max_columns > 0 and n_per_line > max_columns: 
            if forced:
                temp_n = n_per_line
                while temp_n > max_columns:
                    temp_n -= force
                if temp_n > 0:
                    n_per_line = temp_n
            else:
                n_per_line = max_columns
#               print("3. n_per_line is {}.".format(n_per_line))
    if down:  # Tabulating downwards.
        column_data = []
        n_per_column, remainder = divmod(len(data),n_per_line)
        if remainder:
            n_per_column += 1
        if force > 1:
            _, remainder = divmod(n_per_column, force)
            if remainder:
                n_per_column += force -remainder
        for j in range(n_per_column):
            for i in range(0, len(data), n_per_column):
                try:
                    appendee = data[i+j]
                except IndexError:
                    appendee = ''
                column_data.append(appendee)
        data = column_data
    else:  # Tabulating accross so skip the above:
        pass
    if stats:
        return("Alignment={}, down={}, force={}, maxCol={}, n={}"
            .format(alignment, down, force, orig_max_col, n_per_line))

    new_data = []
    row = []
    for i in range(len(data)):
        if not (i % n_per_line):
            new_data.append(separator.join(row))
            row = []
        try:
            appendee = ('{:{}{}}'
                .format(data[i], alignment, max_len))
        except IndexError:
            appendee = ('{:{}{}}'
                .format('', alignment, max_len))
        row.append(appendee)
    if row:
            new_data.append(separator.join(row))
    return '\n'.join(new_data)

def test_tabulate(stats_only):
    print("Running Python3 script: 'tabulate.py'.......")
    words = __doc__.split()
    for alignment_var in ('<', '^', '>'): 
      for down_var in (True, False):
        for force_var in range(7):
          for max_columns_var in range(7):
            table = tabulate(words, down = down_var,
                                    alignment = alignment_var,
                                    force = force_var,
                                    max_columns = max_columns_var,
                                    stats = stats_only)
            if not stats_only:
              print("*** Table is as follows: ***")
              print(
              "v alignment={}, down={}, force={} and max_columns={}. v"
                  .format(alignment_var, down_var,
                          force_var, max_columns_var))
              print(table)
              input(
              "^ alignment={}, down={}, force={} and max_columns={}. ^"
                  .format(alignment_var, down_var,
                          force_var, max_columns_var))
            else:
                input(table)
if __name__ == "__main__":
    test_tabulate(stats_only = True)


