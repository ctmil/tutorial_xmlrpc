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

currency_id = sock.execute(dbname,uid,pwd,'res.currency','search',[('name','=','USD')])
if not currency_id:
	print("No existe el USD")
	exit(4)

country_ids = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Rodrigombia')])
#country_ids = sock.execute(dbname,uid,pwd,'res.country','search',['|',('name','=','Rodrigombia'),('currency_id.name','=','USD')])
#country_ids = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Rodrigombia'),('currency_id','=',currency_id[0])])
#country_ids = sock.execute(dbname,uid,pwd,'res.country','search',['!',('currency_id','=',currency_id[0])])

if not country_ids:
	vals = {
		'name': 'Rodrigombia'
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','create',vals)
	print return_id
else:
	vals = {
		'currency_id': currency_id[0]
		}
	return_id = sock.execute(dbname,uid,pwd,'res.country','write',country_ids,vals)
	print return_id

