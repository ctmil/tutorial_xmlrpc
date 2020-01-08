#!/usr/bin/python

import sys
import xmlrpclib
import ssl
import csv

username = 'admin' #the user
pwd = 'demowebinar' #the user
dbname = 'demowebinar'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://142.93.159.197:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://142.93.159.197:8069/xmlrpc/object',context=gcontext)

f = open('ejemplo_serial_number.csv','rt')
default_code = 'FURN_5555'
product_id = sock.execute(dbname,uid,pwd,'product.product','search',[('default_code','=',default_code)])
csv_reader = csv.reader(f, delimiter='|')
for i,line in enumerate(csv_reader):
	print i,line
	serial_number = line[1].zfill(8)
	vals = {
		'company_id': 1,
		'product_id': product_id[0],
		'name': serial_number,
		}
	return_id = sock.execute(dbname,uid,pwd,'stock.production.lot','create',vals)
	print return_id
f.close()
