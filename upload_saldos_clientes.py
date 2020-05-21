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
		'date': '2020-05-20',
		'partner_id': partner_id,
		'journal_id': 28,
		'company_id': 4,
		'ref': 'SAN RAFAEL v2 - SALDO INICIAL CLIENTE ' + str(row['COD']),
		'type': 'entry'
		}
	amount = float(row['SALDO'].replace(',',''))
	if row['MONEDA'] == 'ARS':
		currency_id = 'ARS'
	if row['MONEDA'] == 'U$S':
		currency_id = 'USD'
	if row['MONEDA'] == 'EUR':
		currency_id = 'EUR'
	currency_id = models.execute_kw(db,uid,pwd,'res.currency','search',[[('name','=',currency_id)]])
	account_move_id = models.execute_kw(db, uid, pwd, 'account.move', 'create', [vals], {'context' :{'check_move_validity': False}})
	print account_move_id

	amount = abs(int(row['SALDO']))
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
	if row['MONEDA'] == 'U$S':
		vals_debit['amount_currency'] = amount
              	vals_debit['debit'] = amount * 63
              	vals_debit['currency_id'] = currency_id[0]
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
	if row['MONEDA'] == 'U$S':
                vals_credit['amount_currency'] = amount * (-1)
                vals_credit['credit'] = abs(amount) * 63
              	vals_credit['currency_id'] = currency_id[0]
        credit_id = models.execute_kw(db, uid, pwd, 'account.move.line', 'create', [vals_credit], {'context' :{'check_move_validity': False}})
        print credit_id
	#try:
	#return_id = models.execute_kw(db, uid, pwd, 'account.move','action_post',[account_move_id],{})
	#print return_id
	#except:
	#	pass
	print "*"*20
