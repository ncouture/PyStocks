#!/usr/bin/python
#

__revision__ = "$Id:$"

def format_number(n):
    """
    Convert a number to a string by adding a coma every 3 characters
    """
    if int(n) < 0:
        raise ValueError("positive integer expected")
    n = str(n)
    return ','.join([n[::-1][x:x+3]
              for x in range(0,len(n),3)])[::-1]
