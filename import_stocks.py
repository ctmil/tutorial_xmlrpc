#!/usr/bin/python3

# import xmlrpc and openpyxl modules
from xmlrpc import client
import openpyxl
from datetime import datetime

url = 'http://45.79.213.164:8069'
common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
res = common.version()

dbname = 'demo_ecommerce'
user = 'admin'
pwd = 'admin'
uid = common.authenticate(dbname, user, pwd, {})

# prints Odoo version and UID to make sure we are connected
print(res)
print(uid)

models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))
# Define la variable para leer el workbook
workbook = openpyxl.load_workbook("stocks.xlsx")

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
        res = None
        if i == 0:
            col = 'location_dest_id'
            # Buscamos por complete_name ya que dicho campo provee toda la estructura de la ubicacion
            res = models.execute_kw(dbname,uid,pwd,'stock.location','search',[[['complete_name','=',cell.value]]])
            location_id = res
        if i == 1:
            col = 'product_id'
            res = models.execute_kw(dbname,uid,pwd,'product.product','search',[[['default_code','=',cell.value]]])
            product_id = res
        if i == 2:
            col = 'product_uom_qty' 
        vals[col] = res and res[0] or cell.value
    if not location_id or not product_id:
        continue
    # Lee unidad de medida
    product_data = models.execute_kw(dbname,uid,pwd,'product.product','read',[product_id])
    vals['product_uom'] = product_data[0].get('uom_id')[0]
    vals['name'] = 'Actualizacion inventario %s' % product_data[0].get('name')
    vals['company_id'] = 1
    vals['state'] = 'draft'
    vals['is_inventory'] = True
    # busca la ubicacion virtual de ajustes de inventario
    location_id = models.execute_kw(dbname,uid,pwd,'stock.location','search',[[['complete_name','=','Virtual Locations/Inventory adjustment'],['company_id','=',1]]])
    if not location_id:
        continue
    vals['location_id'] = location_id[0]
    move_id = models.execute_kw(dbname,uid,pwd,'stock.move','create',[vals])
    print(move_id)
    # Agrega al diccionario el move_id y crea la línea de mov de stock
    vals['move_id'] = move_id
    # asigna la unidad de medida a product_uom_id y borra product_uom
    vals['product_uom_id'] = vals.get('product_uom')
    vals['qty_done'] = vals.get('product_uom_qty')
    del vals['product_uom']
    # borra name
    del vals['name']
    move_line_id = models.execute_kw(dbname,uid,pwd,'stock.move.line','create',[vals])
    print(move_line_id)
    return_id = models.execute(dbname,uid,pwd,'stock.move','action_done',[move_id])
    print(return_id)

"""
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
"""
