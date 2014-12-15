#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# file: 'distance.py'
"""
Module: distance

Utilities for manipulation of feet, inches and fractions of an inch.

Provides a class Distance with the following:
Operators:
    +, -, *, /, **, as well as +=, -=, *= and /=.
        The second operand can be an instance of the class or a number.
Methods:
    def __init__(self, feet, inches, numerator=0, denominator=1):
    def value(self):
        Returns the distance in inches as a float.
    def show(self, inches_only = False, accuracy=16):
        Returns a formated string showing 
            [feet,] inches, numerator, denominator.
        If you want only inches (no feet) set inches_only to True.
        Accuracy to the nearest 1/16th is assumed but can be changed.
    def sqrt(self):
        Returns another instance that is its square root.
    def new(self):
        Returns another instance with the same value. 
        Use this rather than an assignment.

Also provides the following function:
def distances(distance, n_steps):
    Returns an array of distances (as floating point inches)
    marking off <distance> into <n_steps> equal length segments
    starting at 0 and going up to distance.
"""

import math

TOLLERANCE = 0.00001

class Distance(object):

    INCHES = 12  # Inches in a foot.

    def __init__(self, feet, inches, numerator=0, denominator=1):
        """Sets distance in decimal inches.

        Input as described.  If there is no fractional part, default positional
        arguments are provided (0 for numerator and 1 for denominator.)
        First two parameters may be any type that can be converted to
        float.  The default parameters, if provided, must be able to be
        converted to integer type.
        (DON'T ENTER 0 for last paramter- mustn't divide by 0!)
        """
        self.decimal_inches = (float(feet) * Distance.INCHES
                                + float(inches)
                                + int(numerator) / int(denominator))

    @property
    def value(self):
        return self.decimal_inches

    def new(self):
        return Distance(0, self.value)

    def __add__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        ret = Distance(0, 0)
        ret.decimal_inches = self.decimal_inches + other
        return ret

    def __iadd__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        self.decimal_inches += other
        return self

    def __sub__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        ret = Distance(0, 0)
        ret.decimal_inches = self.decimal_inches - other
        return ret

    def __isub__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        self.decimal_inches -= other
        return self

    def __mul__(self, other):
        if isinstance(other, Distance):
            other = other.inches
        ret = Distance(0, 0)
        ret.decimal_inches = self.decimal_inches * other
        return ret

    def __imul__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        self.decimal_inches *= other
        return self

    def __truediv__(self, other):
        if isinstance(other, Distance):
            other = other.decimal.inches
        return Distance(0, self.decimal_inches / other)
        ret = Distance(0, 0)

    def __itruediv__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        self.decimal_inches /= other
        return self

    def __pow__(self, other):
        if isinstance(other, Distance):
            other = other.decimal.inches
        return Distance(0, self.decimal_inches ** other)

    def __lt__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        return self.decimal_inches < other

    def __le__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        return self.decimal_inches <= other

    def __eq__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        if abs(self.decimal_inches - other) > TOLLERANCE:
            return False
        else:
            return True
        return self.decimal_inches == other

    def __ne__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        if abs(self.decimal_inches - other) <= TOLLERANCE:
            return False
        else:
            return True

    def __ge__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        return self.decimal_inches >= other

    def __gt__(self, other):
        if isinstance(other, Distance):
            other = other.decimal_inches
        return self.decimal_inches > other

    def sqrt(self):
        """Returns another instance that is its square root."""
        return Distance(0, math.sqrt(self.decimal_inches))

    def show(self, inches_only = False, accuracy=16):
        """Returns tuple of feet|none, inches, numerator, denominator.

        Assumes your want feet, inches, fractions of an inch.
        If you want only inches (no feet) set inches_only to True.
        Accuracy to the nearest 1/16th is assumed but can be changed.
        """
        inches, decimal = divmod(self.decimal_inches, 1)
        fraction, decimal = divmod(decimal * accuracy, 1)
        if decimal >= 0.5:
            fraction += 1
        while fraction % 2 == 0 and fraction > 0:
            fraction /= 2
            accuracy /= 2
        if inches_only or self.value < Distance.INCHES:
            args = int(inches), int(fraction), int(accuracy)
            if args[1]:
                return """{}"{}/{}""".format(*args)
            else:
                return '{}"'.format(args[0])
        else:
            feet, inches = divmod(inches, 12)
            args = int(feet), int(inches), int(fraction), int(accuracy)
            if args[2]:
                return """{}'{}"{}/{}""".format(*args)
            else:
                return "{}'{}\"".format(*args[:2])

    def __str__(self):
        return self.show()

def distances(distance, n_steps):
    """ Returns an array of distances (as floating point inches)
    marking off <distance> into <n_steps> equal length segments
    starting at 0 and going up to distance.
    """
    ret = []
    for i in range(n_steps + 1):
        ret.append(distance * i / n_steps)
    return ret

def lay_out(span, gauge, n_spaces):
    """The first two parameters can be either instances of the Distance
    class or tuples suitable for turning into instances there of.
    The third is an integer.
    Assume we have a 'span' length opening that we want to divide into
    'n_spaces' spaces using dividers that are themselves 'gauge' wide.
    Returned is an array of instances of the Distance class.
    The array values begin with 0 and end with span.
    Intervening pairs are points marking the location of each side of each
    divider.  The second item in the array provides the gap.
    """
    if type(span) == tuple:
        span = Distance(*span)
    if type(gauge) == tuple:
        gauge = Distance(*gauge)
    gap =  (span - gauge * (n_spaces -1)) / n
    ret = []
    ret.append(Distance(0, 0))
    running_total = gap.new()
    ret.append(running_total.new())
    while running_total < span:
        running_total += gauge
        ret.append(running_total.new())
        running_total += gap
        ret.append(running_total.new())
    assert(running_total == span)
    return ret


def test():
    while True:
        tup = input(
            "Provide feet, inches, fraction, denominator: ")
        tup = tup.split()
        di = Distance(*tup)
        print("{} is represented internally as {}.".format(tup, di.value))
        di1 = Distance(*[int(val) for val in tup])
        print('Represents {}"'.format(di1.show()))
        print('And converts back to {} or {}.'
                                .format(di.show(),
                                        di.show(inches_only = True)))

def receiver_platform():
    opening = (0, 43)
    gauge = (0, 0, 1, 8)
    ret = []
    for n in range(5, 11):
        gap = (span - thickness * n) / (n + 1)
        ret.append("With {} cross members, gaps will be {}."
                .format(n, gap.show()))
    return ret

def show(inches):
    for inch in inches:
        print("{:6.2f} inches => {}."
                .format(inch, Distance(0, inch).show()))

if __name__ == "__main__":
    print("Running Python3 script: 'british.py'.......")
    my_dimensions = (
                7,
                7.25,
                9,
                10.5,
                10.75,
                12,
                16,
                17,
                20.5,
                29,
                30,
                32,
                36,
                36 + 1/8,
                43,
                46,
                54,
                55,
                57,
                61,
                67,
                77.5,
                89,
                90,
                102,
                )

    #   test()
    #   show(my_dimensions)
    bad_code = """
    array = platform()
    for line in array:
        print(line)

    array = distances(43, 8)
    for item in array:
        d = Distance(0, item)
        print('{}, '.format(d.show()), end='')
    print()
    """

    begin = 5
    end = 12
    opening = (0, 43)
    gauge = (0, 0, 1, 8)
    print("Number of openings     Size of gap")
    data = []
    for n in range(5, end + 1):
        l = lay_out(opening, gauge, n)
        data.append(l)
    for n, item in enumerate(data, begin):
        print("{:^19}     {:^11}".format(n, item[1].show()))

    which = int(input("Pick one to get a lay out: "))
    print("For span of {}, using {} dividers ({} openings) of gauge {}:"
            .format(Distance(*opening).show(inches_only=True),
                    which-1,
                    which,
                    Distance(*gauge).show(inches_only=True)))
    print("The layout will be:")
    for d in data[which-begin]:
        print('{}, '.format(d.show(inches_only=True)), end='')
    print()
    later = """
    print("We are working with a {} opening and {} cross members."
                                .format(Distance(*opening)))
"""
