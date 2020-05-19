#!/usr/bin/python

import sys
import xmlrpclib
import ssl
import csv

username = 'admin' #the user
pwd = 'demo_ar' #the user
dbname = 'demo_ar'    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://capacitacion:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://capacitacion:8069/xmlrpc/object',context=gcontext)

f = open('paises.csv','rt')
reader = csv.DictReader(f)

categories = ['Consulting Services','Services']
categ_ids = []
for category in categories:
	categ_id = sock.execute(dbname,uid,pwd,'res.partner.category','search',[('name','=',category)])
	if categ_id:
		categ_ids.append(categ_id[0])

for i,row in enumerate(reader):
	print i,row
	ref = row['ref']
	name = row['name']
	provincia = row['state_id']
	state_id = sock.execute(dbname,uid,pwd,'res.country.state','search',[('name','=',provincia)])
	partner_id = sock.execute(dbname,uid,pwd,'res.partner','search',[('ref','=',ref)])
	vals = {
		'ref': ref,
		'name': name,
		'state_id': state_id[0],
		'category_id': [(6,0,categ_ids)],
		}
	l10n_latam_identification_type_id = None
	if row.get('l10n_latam_identification_type_id',None):
		l10n_latam_identification_type_id = sock.execute(dbname,uid,pwd,'l10n_latam.identification.type','search',[('name','=',row.get('l10n_latam_identification_type_id',None))])
		if l10n_latam_identification_type_id:
			vals['l10n_latam_identification_type_id'] = l10n_latam_identification_type_id[0]
	if not partner_id:
		return_id = sock.execute(dbname,uid,pwd,'res.partner','create',vals)
		print return_id
	else:
		return_id = sock.execute(dbname,uid,pwd,'res.partner','write',partner_id,vals)
		print return_id
		if l10n_latam_identification_type_id:
			vat = row['vat']
			vat = vat.replace('-','')
			vat = vat.replace('.','')
			vals['vat'] = vat
			return_id = sock.execute(dbname,uid,pwd,'res.partner','write',partner_id,vals)
			print return_id

			
