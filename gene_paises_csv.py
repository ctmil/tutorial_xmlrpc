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

for row in reader:
	print row
	country_id = sock.execute(dbname,uid,pwd,'res.country','search',[('code','=',row['Code'])])
	if country_id:
		print "Encontro %s"%(row['Name'])
