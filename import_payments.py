#!/usr/bin/python3

# import xmlrpc and openpyxl modules
from xmlrpc import client
import openpyxl
from datetime import datetime

url = 'http://localhost:8069'
common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
res = common.version()

dbname = 'mrputilsv1'
user = 'admin'
pwd = 'admin'
uid = common.authenticate(dbname, user, pwd, {})

# prints Odoo version and UID to make sure we are connected
print(res)
print(uid)

models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))
# Define la variable para leer el workbook
workbook = openpyxl.load_workbook("demo_payments.xlsx")

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
    for i,cell in enumerate(row):
        print(i,cell.value)
        ref = ''
        if i == 0:
            col = 'payment_type' 
        if i == 1:
            col = 'partner_id' 
        if i == 2:
            col = 'amount' 
        if i == 3:
            col = 'date' 
        if i == 4:
            col = 'ref'
            ref = cell.value
        if i == 5:
            col = 'journal_id'
        if i not in [1,5]:
            vals[col] = cell.value
            if type(vals[col]) == datetime:
                vals[col] = str(vals[col])
        else:
            if i == 1:
                many2one_model = 'res.partner'
            else:
                many2one_model = 'account.journal'
            # saltea registros con valores many2one vacios
            if cell.value == None:
                continue
            res_id = models.execute_kw(dbname,uid,pwd,many2one_model,'search',[[['name','=',cell.value]]])
            # Si no encontramos el registro, pasamos al siguiente
            if not res_id:
                continue
            vals[col] = res_id[0]
    # saltea lineas en blanco
    if vals.get('ref') == None:
        continue
    payment_id = models.execute_kw(dbname,uid,pwd,'account.payment','search',[[['ref','=',vals.get('ref')]]])
    if not payment_id:
        payment_id = models.execute_kw(dbname,uid,pwd,'account.payment','create',[vals])
        return_id = payment_id
    else:
        return_id = models.execute_kw(dbname,uid,pwd,'account.payment','write',[payment_id,vals])
    print(return_id)
    try:
        post_id = models.execute_kw(dbname,uid,pwd,'account.payment','action_post',[payment_id])
        print(post_id)
    except:
        pass
