#!/usr/bin/python

import sys
import xmlrpclib
import ssl

username = 'admin' #the user
pwd = 'demo_ar' #the user
dbname = 'demo_ar'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://capacitacion:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://capacitacion:8069/xmlrpc/object',context=gcontext)

country_ids = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Rodrigombia')])

"""
if not country_ids:
	vals = {
		'name': 'Rodrigombia'
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','create',vals)
	print return_id
else:
	currency_id = sock.execute(dbname,uid,pwd,'res.currency','search',[('name','=','USD')])
	if currency_id:
		vals = {
			'currency_id': currency_id[0]
			}
		return_id = sock.execute(dbname,uid,pwd,'res.country','write',country_ids,vals)
		print return_id
"""

if country_ids:
	print "Borrando"
	return_id = sock.execute(dbname,uid,pwd,'res.country','unlink',country_ids)
	print return_id

