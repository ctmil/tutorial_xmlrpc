#!/usr/bin/python

import sys
import xmlrpclib
import ssl

import csv

username = '' #the user
pwd = '' #the user
dbname = ''    #the database

gcontext = ssl._create_unverified_context()

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http:///xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http:///xmlrpc/object',context=gcontext)

f = open('jujuy.csv','w')

fieldnames = ['name', 'customer', 'capital']
writer = csv.DictWriter(f, fieldnames=fieldnames)
writer.writeheader()

investment_ids = sock.execute(dbname,uid,pwd,'crm.investment','search',[('state','=','confirmed'),('pv','>',1000000)])
print "Cantidad de ON %s"%(len(investment_ids))
for investment_id in investment_ids:
	print investment_id
	investment_data = sock.execute(dbname,uid,pwd,'crm.investment','read',investment_id,['name','pv','partner_id'])
	print investment_data
	writer.writerow({'name': investment_data[0]['name'],'customer': investment_data[0]['partner_id'][1],'capital': investment_data[0]['pv']})
	partner_data = sock.execute(dbname,uid,pwd,'res.partner','read',investment_data[0]['partner_id'][0],['phone'])
	print partner_data

f.close()
