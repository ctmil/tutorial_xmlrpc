#!/usr/bin/python

import sys
import xmlrpclib
import ssl
import csv

username = 'admin' #the user
pwd = 'demo_ar' #the user
dbname = 'demo_ar'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://grupomaca:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://grupomaca:8069/xmlrpc/object',context=gcontext)

f = open('clientes.csv','rt')
csv_reader = csv.reader(f, delimiter='|')
for row in csv_reader:
	print row
	ref = row[0]
	name = row[1] + ',' + row[2]
	city = row[3]
	state = row[4]
	partner_id = sock.execute(dbname,uid,pwd,'res.partner','search',[('ref','=',ref)])
	if not partner_id:
		vals = {
			'ref': ref,
			'name': name,
			'city': city,
			}
		return_id = sock.execute(dbname,uid,pwd,'res.partner','create',vals)
		print return_id
	else:
		state_id = sock.execute(dbname,uid,pwd,'res.country.state','search',[('name','=',state)])
		if state_id:
			vals = {
				'state_id': state_id[0]
				}
			return_id = sock.execute(dbname,uid,pwd,'res.partner','write',partner_id,vals)
			print return_id

f.close()
