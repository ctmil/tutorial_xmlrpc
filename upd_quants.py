#!/usr/bin/python

import sys
import xmlrpclib
import ssl

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
product_id = sock.execute(dbname,uid,pwd,'product.product','search',[('default_code','=','PROD_STOCK')])

quant_id = sock.execute(dbname,uid,pwd,'stock.quant','search',[('product_id','=',product_id[0]),('location_id','=',location_id[0])])
if quant_id:
	quant_data = sock.execute(dbname,uid,pwd,'stock.quant','read',quant_id)
	print quant_data
	vals_update = {
		'quantity': 555
		}
	return_id = sock.execute(dbname,uid,pwd,'stock.quant','write',quant_id,vals_update)
	print return_id
