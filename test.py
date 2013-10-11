#!/usr/bin/python
import datetime
#print "Yes, this is it"
test = open('/Users/jzucker/Desktop/log.txt', 'a')
test.write('************')
test.write('we just ran')
test.write(str(datetime.datetime.now()) + '\n')
test.write('************')
test.close()
exit(0)
