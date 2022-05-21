#!/usr/bin/python3

# import xmlrpc and openpyxl modules
from xmlrpc import client
import openpyxl
from datetime import datetime

url = 'http://45.79.213.164:8069'
common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
res = common.version()

dbname = 'demo_contract_ar'
user = 'admin'
pwd = 'admin'
uid = common.authenticate(dbname, user, pwd, {})

# prints Odoo version and UID to make sure we are connected
print(res)
print(uid)

models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Busca el ID del journal MISC
journal_id = models.execute_kw(dbname,uid,pwd,'account.journal','search',[[['code','=','MISC']]])
# Busca cuenta ajuste de capital (codigo 3.1.1.01.020)
credit_account_id = models.execute_kw(dbname,uid,pwd,'account.account','search',[[['code','=','3.1.1.01.020'],['company_id','=',1]]])
# Busca cuenta deudores por venta (codigo 3.1.1.01.020)
debit_account_id = models.execute_kw(dbname,uid,pwd,'account.account','search',[[['code','=','1.1.3.01.010'],['company_id','=',1]]])

# Define la variable para leer el workbook
workbook = openpyxl.load_workbook("saldos_cuenta_corriente.xlsx")

# Define variable para la planilla activa
worksheet = workbook.active

# Itera las filas para leer los contenidos de cada celda
rows = worksheet.rows
for x,row in enumerate(rows):
    # Saltea la primer fila porque tiene el nombre de las columnas
    if x == 0:
        continue
    # Lee cada una de las celdas en la fila
    vals = {}
    partner_id = None
    amount = 0
    for i,cell in enumerate(row):
        print(i,cell.value)
        ref = ''
        if i == 0:
            # Busca el cliente por el codigo de referencia
            partner_id = models.execute_kw(dbname,uid,pwd,'res.partner','search',[[['ref','=',cell.value]]])
            if not partner_id:
                continue
        if i == 1:
            col = 'ref' 
            vals[col] = cell.value
        if i == 2:
            col = 'date'
            vals[col] = cell.value
            if type(vals[col]) == datetime:
                vals[col] = str(vals[col])
        if i == 3:
            amount = float(cell.value)

    vals['journal_id'] = journal_id[0]
    vals['name'] = vals.get('ref')
    vals['company_id'] = 1
    move_id = models.execute_kw(dbname,uid,pwd,'account.move','search',[[['ref','=',vals.get('ref')]]])
    if not move_id:
        move_id = models.execute_kw(dbname,uid,pwd,'account.move','create',[vals])
    else:
        # El asiento ya fue creado, se pasa a la siguiente fila
        continue
    print(move_id)
    vals_debit = {
            'company_id': 1,
            'move_id': move_id,
            'date': vals.get('date'),
            'journal_id': vals.get('journal_id'),
            'account_id': debit_account_id[0],
            'partner_id': partner_id[0],
            'name': vals.get('ref'),
            'debit': amount,
            'credit': 0,
            }
    debit_id = models.execute_kw(dbname,uid,pwd,'account.move.line','create',[vals_debit],{'context' :{'check_move_validity': False}})
    vals_credit = {
            'company_id': 1,
            'move_id': move_id,
            'date': vals.get('date'),
            'journal_id': vals.get('journal_id'),
            'account_id': credit_account_id[0],
            'partner_id': partner_id[0],
            'name': vals.get('ref'),
            'debit': 0,
            'credit': amount,
            }
    credit_id = models.execute_kw(dbname,uid,pwd,'account.move.line','create',[vals_credit],{'context' :{'check_move_validity': False}})
    post_id = models.execute_kw(dbname,uid,pwd,'account.move','action_post',[move_id])
    print(post_id)
