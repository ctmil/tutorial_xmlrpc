#!/usr/bin/python

import sys
import xmlrpclib
import ssl

username = 'admin' #the user
pwd = 'demowebinar' #the user
dbname = 'demowebinar'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://142.93.159.197:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://142.93.159.197:8069/xmlrpc/object',context=gcontext)

# 1 - Ejemplo de busqueda
partner_ids = sock.execute(dbname,uid,pwd,'res.partner','search',[('customer_rank','>',0)])
for partner_id in partner_ids:
	print partner_id
	# Ejemplo de lectura
	partner_data = sock.execute(dbname,uid,pwd,'res.partner','read',partner_id,['name','city','email'])
	print partner_data
