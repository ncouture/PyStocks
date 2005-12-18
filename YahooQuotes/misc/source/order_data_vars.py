#!/usr/bin/python
# $Id:$

import cPickle
yhoo = {}

# more or less manually formatted version of
# http://edit.my.yahoo.com/config/edit_pfview?.vk=v1
#
# my yahoo lin: atestok xssord: tmp123
#
f = open('datavarlist.txt', 'r')
while True:
    line = f.readline()
    if line and line != '\n':
        key = line.split()[:1][0]
        descr = line.split()[1:]
        yhoo[key] = " ".join(descr)
    else:
        break

for key in yhoo:
    print key + ": " + yhoo[key]

f = open('YahooFinanceDataVariables.dict', 'w')
cPickle.dump(yhoo, f)#, protocol=-1)
f.close()
