#!/usr/bin/python

import sys
import xmlrpclib
import ssl
import csv

username = 'admin' #the user
pwd = 'demo_uy' #the user
dbname = 'demo_uy'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://capacitacion:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://capacitacion:8069/xmlrpc/object',context=gcontext)

f = open('jugadores.csv','rt')
reader = csv.DictReader(f,delimiter='|')

for row in reader:
	print row
	ref = row['ref']
	name = row['name']
	partner_id = sock.execute(dbname,uid,pwd,'res.partner','search',[('ref','=',ref)])
	if not partner_id:
		vals = {
			'ref': ref,
			'name': name,
			}	
		partner_id = sock.execute(dbname,uid,pwd,'res.partner','create',vals)
	else:
		uruguay_id = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Uruguay')])
		if uruguay_id:
			vals = {
				'country_id': uruguay_id[0]
				}
			return_id = sock.execute(dbname,uid,pwd,'res.partner','write',partner_id,vals)
			print return_id

