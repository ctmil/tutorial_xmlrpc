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
if country_id:
	return_id = sock.execute(dbname,uid,pwd,'res.country','unlink',country_id)
	print return_id
