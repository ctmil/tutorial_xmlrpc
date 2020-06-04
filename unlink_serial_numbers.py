#!/usr/bin/python

import sys
import xmlrpclib
import ssl

username = 'admin' #the user
pwd = 'demowebinar' #the user
dbname = 'demowebinar'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://142.93.159.197:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://142.93.159.197:8069/xmlrpc/object',context=gcontext)

serial_ids = sock.execute(dbname,uid,pwd,'stock.production.lot','search',[])

for i,serial_id in enumerate(serial_ids):
	print i
	return_id = sock.execute(dbname,uid,pwd,'stock.production.lot','unlink',serial_id)
	print return_id
