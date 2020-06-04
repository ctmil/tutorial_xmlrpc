#!/usr/bin/python

import xmlrpclib
import csv

username = 'admin' #the user
pwd = 'demo_ar'      #the password of the user
db = 'demo_ar'    #the database


# Get the destination uid
#sock_common = xmlrpclib.ServerProxy ('https://prod.renodirector.com//xmlrpc/common')
#uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
#sock = xmlrpclib.ServerProxy('https://prod.renodirector.com/xmlrpc/object')
#fields = ['company_id','company_type','phone','email','name','customer','supplier','follower','street','street2','city','zip','country_id','state_id','property_product_pricelist','lang','main_id_number','gross_income_number','afip_responsability_type_id','sale_user_group_id','opt_out','team_id']

url = 'http://capacitacion:8069'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, pwd, {})

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

f = open('saldos_cliente.csv','rt')
csv_reader = csv.DictReader(f, delimiter='|')
products = []
partners = []
order_id = None
for i,row in enumerate(csv_reader):
	print i,row

        partner_id = models.execute_kw(db,uid,pwd,'res.partner','search',[[('ref','=',row['COD'])]])
	if not partner_id:
		import pdb;pdb.set_trace()

	if type(partner_id) == list:
		partner_id = partner_id[0]
	vals = {
		'date': '2020-06-04',
		'partner_id': partner_id,
		'journal_id': 28,
		'company_id': 4,
		'ref': 'COLOMBIA - SALDO INICIAL CLIENTE ' + str(row['COD']),
		'type': 'entry'
		}
	amount = float(row['SALDO'].replace(',',''))
	account_move_id = models.execute_kw(db, uid, pwd, 'account.move', 'create', [vals], {'context' :{'check_move_validity': False}})
	print account_move_id

	amount = abs(int(row['SALDO']))
	# '-302'
	# int('-302') = -302
	# abs(-302) = 302
	vals_debit = {
		# deudores por venta
		'account_id': 307,
		'partner_id': partner_id,
		'name': 'SAN RAFAEL - SALDO INICIAL DEBITO ARS',
		'debit': abs(amount),
		'credit': 0,
		'move_id': account_move_id,
		#'currency_id': currency_id[0],
		'company_id': 4,
	}
        debit_id = models.execute_kw(db, uid, pwd, 'account.move.line', 'create', [vals_debit], {'context' :{'check_move_validity': False}})
        print debit_id
        vals_credit = {
                # ajuste de saldos
               	'account_id': 382,
                'partner_id': partner_id,
                'name': 'SALDO INICIAL CREDIT',
                'credit': abs(amount),
                'move_id': account_move_id,
		#'currency_id': currency_id[0],
		'company_id': 4
                }
        credit_id = models.execute_kw(db, uid, pwd, 'account.move.line', 'create', [vals_credit], {'context' :{'check_move_validity': False}})
        print credit_id
	#try:
	#return_id = models.execute_kw(db, uid, pwd, 'account.move','action_post',[account_move_id],{})
	#print return_id
	#except:
	#	pass
	print "*"*20
