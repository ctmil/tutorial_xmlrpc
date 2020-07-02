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

"""
for row in reader:
	print row
	state_id = sock.execute(dbname,uid,pwd,'res.country.state','search',[('name','=',row['state_id'])])
	if not state_id:
		print "No existe la provincia " + row['state_id']
	else:
		vals = {
			'ref': row['ref'],
			'name': row['name'],
			'state_id': state_id[0],
			'l10n_ar_afip_responsibility_type_id': 1,
			'l10n_latam_identification_type_id': 4,
			'vat': '20230080217'		
			}
		partner_id = sock.execute(dbname,uid,pwd,'res.partner','search',[('ref','=',row['ref'])])
		if partner_id:
			return_id = sock.execute(dbname,uid,pwd,'res.partner','write',partner_id,vals)
		else:
			return_id = sock.execute(dbname,uid,pwd,'res.partner','create',vals)
		print return_id
		vat = '20230080217'
		vals_write = {
			'vat': vat
			}
		return_id = sock.execute(dbname,uid,pwd,'res.partner','write',partner_id,vals_write)
		print return_id

f.close()
"""
