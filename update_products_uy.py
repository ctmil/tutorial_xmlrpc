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

for row in reader:
	print row
	default_code = row['default_code']
	name = row['name']
	category = row['category']
	category_id = sock.execute(dbname,uid,pwd,'product.category','search',[('name','=',category)])
	if not category_id:
		vals ={
			'name': category,
			'parent_id': 1
			}
		category_id = sock.execute(dbname,uid,pwd,'product.category','create',vals)
		print category_id
	if type(category_id) == list:
		category_id = category_id[0]
	product_id = sock.execute(dbname,uid,pwd,'product.product','search',[('default_code','=',default_code)])
	if not product_id:
		vals = {
			'default_code': default_code,
			'name': name,
			'categ_id': category_id,
			}
		product_id = sock.execute(dbname,uid,pwd,'product.product','create',vals)
		print product_id
		
