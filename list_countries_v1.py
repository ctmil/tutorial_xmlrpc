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

country_id = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Rodrigombia')])
if country_id:
	vals = {
		'l10n_ar_afip_code': '1266'
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','write',country_id,vals)
	print return_id
	country_data = sock.execute(dbname,uid,pwd,'res.country','read',country_id)
	print country_data
else:
	vals = {
		'name': 'Rodrigombia'
		}
	country_id = sock.execute(dbname,uid,pwd,'res.country','create',vals)
	print "Creo ", country_id


