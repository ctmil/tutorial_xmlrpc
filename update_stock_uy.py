#!/usr/bin/python

import sys
import xmlrpclib
import ssl
import csv

username = 'admin' #the user
pwd = 'demo_uy' #the user
dbname = 'demo_uy'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://capacitacion:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://capacitacion:8069/xmlrpc/object',context=gcontext)

f = open('ejemplo_sibra.csv','rt')
reader = csv.DictReader(f,delimiter='|')

vals_inv_header = {
	'company_id': 1,
	'name': 'Ejemplo 1 - version 3',
	'prefill_counted_quantity': 'counted',
	}
inv_header = sock.execute(dbname,uid,pwd,'stock.inventory','create',vals_inv_header)
print inv_header
action_id = sock.execute(dbname,uid,pwd,'stock.inventory','action_start',[inv_header])
print action_id

for row in reader:
	print row
	default_code = row['default_code']
	name = row['name']
	category = row['category']
	stock = int(row['inventario'])
	product_id = sock.execute(dbname,uid,pwd,'product.product','search',[('default_code','=',default_code)])
	if product_id:
		vals_line = {
			'inventory_id': inv_header,
			'location_id': 18,
			'product_id': product_id[0],
			'product_qty': stock
		}
		line_id = sock.execute(dbname,uid,pwd,'stock.inventory.line','create',vals_line)
		
