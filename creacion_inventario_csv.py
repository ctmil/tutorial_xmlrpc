#!/usr/bin/python

import sys
import xmlrpclib
import ssl
import csv

username = 'admin' #the user
pwd = 'demo_stock' #the user
dbname = 'demo_stock'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://demo_server:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://demo_server:8069/xmlrpc/object',context=gcontext)

location_id = sock.execute(dbname,uid,pwd,'stock.location','search',[('usage','=','internal')])

vals_inv_header = {
	'name': 'Test inventario CSV #1',
	#'location_ids': location_id[0],
	'prefill_counted_quantity': 'counted'
	}
inv_header = sock.execute(dbname,uid,pwd,'stock.inventory','create',vals_inv_header)
print inv_header
action_id = sock.execute(dbname,uid,pwd,'stock.inventory','action_start',[inv_header])
print action_id

f = open('ejemplo_inventario_serie.csv','rt')
csv_reader = csv.DictReader(f,delimiter=',')
for line in csv_reader:
	print line
	product_id = sock.execute(dbname,uid,pwd,'product.product','search',[('default_code','=',line['producto'])])
	if not product_id:
		print('Error no existe el producto %s'%(line['producto']))
		continue
	lot_id = sock.execute(dbname,uid,pwd,'stock.production.lot','search',[('product_id','=',product_id[0]),('name','=',line['nro_serie'])])
	if not lot_id:
		vals = {
			'name': line['nro_serie'],
			'ref': line['nro_serie'],
			'product_id': product_id[0],
			'company_id': 1,
			}
		lot_id = sock.execute(dbname,uid,pwd,'stock.production.lot','create',vals)
	if type(lot_id) == list:
		lot_id = lot_id[0]
	
	vals_line = {
		'inventory_id': inv_header,
		'location_id': location_id[0],
		'product_id': product_id[0],
		'prod_lot_id': lot_id,
		'product_qty': 1,
		}
	line_id = sock.execute(dbname,uid,pwd,'stock.inventory.line','create',vals_line)
	print line_id

action_id = sock.execute(dbname,uid,pwd,'stock.inventory','action_validate',[inv_header])
print action_id
