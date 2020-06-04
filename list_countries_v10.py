#!/usr/bin/python

import sys
import xmlrpclib
import ssl

username = 'admin' #the user
pwd = 'demo_ar' #the user
dbname = 'demo_ar'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://grupomaca:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://grupomaca:8069/xmlrpc/object',context=gcontext)

country_id = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Rodrigombia')])
if not country_id:
	vals = {
		'name': 'Rodrigombia'
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','create',vals)
	print return_id
else:
	vals = {
		'code': 'R0'
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','write', country_id,vals)
	print return_id
"""
country_data = sock.execute(dbname,uid,pwd,'res.country','read',country_ids)
for idx in range(len(country_data)):
	print country_data[idx]['name']
"""
