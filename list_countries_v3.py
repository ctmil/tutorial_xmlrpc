#!/usr/bin/python

import xmlrpclib

username = 'admin' #the user
pwd = 'demo_ar'      #the password of the user
dbname = 'demo_ar'    #the database

## Get the uid
sock_common = xmlrpclib.ServerProxy ('http://capacitacion:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
#
##replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://capacitacion:8069/xmlrpc/object')
"""
country_ids = sock.execute(dbname,uid,pwd,'res.country','search',[])
for country_id in country_ids:
	country_data = sock.execute(dbname,uid,pwd,'res.country','read',country_id)
	print country_data[0]['name'],country_data[0]['code']
"""
country_id = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Rodrigombia')])
if not country_id:
	vals = {
		'name': 'Rodrigombia'
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','create',vals)
	print return_id
else:
	currency_id = sock.execute(dbname,uid,pwd,'res.currency','search',[('name','=','USD')])
	vals = {
		'code': 'RG',
		'currency_id': currency_id[0],
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','write',country_id,vals)
	print "Actualizo ",return_id
