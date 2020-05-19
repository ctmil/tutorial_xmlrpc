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
sock_common = xmlrpclib.ServerProxy ('http://capacitacion:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://capacitacion:8069/xmlrpc/object',context=gcontext)

f = open('paises.csv','rt')
reader = csv.DictReader(f)

for i,row in enumerate(reader):
	print i,row
	ref = row['ref']
	name = row['name']
	partner_id = sock.execute(dbname,uid,pwd,'res.partner','search',[('ref','=',ref)])
	vals = {
		'ref': ref,
		'name': name,
		}
	if not partner_id:
		return_id = sock.execute(dbname,uid,pwd,'res.partner','create',vals)
		print return_id
	else:
		return_id = sock.execute(dbname,uid,pwd,'res.partner','write',partner_id,vals)
		print return_id
