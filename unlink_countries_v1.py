#!/usr/bin/python

import sys
import xmlrpclib
import ssl

username = 'admin' #the user
pwd = 'demo_uy' #the user
dbname = 'demo_uy'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://capacitacion:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://capacitacion:8069/xmlrpc/object',context=gcontext)

country_id = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Rodrigombia')])
if not country_id:
	print "No es necesario borrar"
else:
	return_id = sock.execute(dbname,uid,pwd,'res.country','unlink',country_id)
	print return_id
	

"""
for country_id in country_ids:
	country_data = sock.execute(dbname,uid,pwd,'res.country','read',country_id,['name','code'])
	print country_data
"""
