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
country_id = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Rodrigombia')])
if not country_id:
	vals = {
		'name': 'Rodrigombia'
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','create',vals)
	print return_id
else:
	currency_id = sock.execute(dbname,uid,pwd,'res.currency','search',[('name','=','USD')])
	if currency_id:
		vals = {
			'currency_id': currency_id[0],
			}
		return_id = sock.execute(dbname,uid,pwd,'res.country','write',country_id,vals)
		print return_id
"""
country_id = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Estados Unidos')])
if country_id:
	country_data = sock.execute(dbname,uid,pwd,'res.country','read',country_id)
	country_data = country_data[0]
	print country_data['currency_id'],country_data['state_ids']
	for state_id in country_data['state_ids']:
		state_data = sock.execute(dbname,uid,pwd,'res.country.state','read',state_id,['name'])
		state_data = state_data[0]
		print state_data
"""	
