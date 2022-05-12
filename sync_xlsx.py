#!/usr/bin/python3

# import xmlrpc and openpyxl modules
from xmlrpc import client
import openpyxl


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
workbook = openpyxl.load_workbook("demo_products.xlsx")

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
        if i == 0:
            col = 'name' 
        if i == 1:
            col = 'default_code' 
        if i == 2:
            col = 'list_price' 
        vals[col] = cell.value
        print(i,cell.value)
    product_tmpl_id = models.execute_kw(dbname,uid,pwd,'product.template','search',[[['default_code','=',vals.get('default_code')]]])
    if not product_tmpl_id:
        return_id = models.execute_kw(dbname,uid,pwd,'product.template','create',[vals])
    else:
        return_id = models.execute_kw(dbname,uid,pwd,'product.template','write',[product_tmpl_id,vals])
    print(return_id)

