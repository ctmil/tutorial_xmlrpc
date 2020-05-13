#!/usr/bin/python

import sys
import xmlrpclib
import ssl

username = 'admin' #the user
pwd = 'demo_ar' #the user
dbname = 'demo_ar'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://capacitacion:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://capacitacion:8069/xmlrpc/object',context=gcontext)
"""
product_ids = sock.execute(dbname,uid,pwd,'product.product','search',[])
for product_id in product_ids:
	product_data = sock.execute(dbname,uid,pwd,'product.product','read',product_id)
	product_data = product_data[0]
	print product_data['name'],product_data['categ_id']
	if product_data['categ_id'][1] == 'All':
		vals = {
			'categ_id': 8
			}
		return_id = sock.execute(dbname,uid,pwd,'product.product','write',product_id,vals)
		print return_id
"""
country_ids = sock.execute(dbname,uid,pwd,'res.country','search',[('state_ids','!=',False)])
for country_id in country_ids:
	print country_id
	country_data = sock.execute(dbname,uid,pwd,'res.country','read',country_id)
	country_data = country_data[0]
	print country_data['state_ids']
	for state_id in country_data['state_ids']:
		state_data = sock.execute(dbname,uid,pwd,'res.country.state','read',state_id)
		print state_data[0]['name']
