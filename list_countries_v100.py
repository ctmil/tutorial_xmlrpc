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

if country_ids:
	print "Borrando Rodrigombia"
	return_id = sock.execute(dbname,uid,pwd,'res.country','unlink',country_ids)
	print return_id


"""
if not country_ids:
	vals = {
		'name': 'Rodrigombia'
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','create',vals)
	print return_id 
else:
	usd_id = sock.execute(dbname,uid,pwd,'res.currency','search',[('name','=','USD')])
	vals = {
		'currency_id': usd_id[0]
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','write',country_ids,vals)
	print return_id

for country_id in country_ids:
	country_data = sock.execute(dbname,uid,pwd,'res.country','read',country_id,['name','currency_id'])
	country_data = country_data[0]
	print country_id,country_data
"""
