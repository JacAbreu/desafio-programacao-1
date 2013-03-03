# coding: utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func

from database import init_db
from models_little_store import Client, Sale, Merchant, Product

def import_sale_file(file_source):

	for line in file_source:

		line = line.decode('utf-8')

		print "line ->"
		print line

		line_aux = line.split('\t')

		if(line_aux[0]!= "purchaser name"):
			

			client = Client.query.filter(Client.name == line_aux[0]).first()
					
			merchant = Merchant.query.filter(Merchant.name == line_aux[5]).first()
	
			product = Product.query.filter(Product.name == line_aux[1]).first()
	
			if(client is None):
				print line_aux[0]
				#client = Client (str(line_aux[0]).decode('utf-8'))
				client = Client (line_aux[0])
				db_session.add(client)			
				db_session.commit()		
				client = Client.query.filter(Client.name == line_aux[0]).first()
		
			if (merchant is None):
				merchant = Merchant (line_aux[5], line_aux[4])
				print merchant
				db_session.add(merchant)
				db_session.commit()
				merchant = Merchant.query.filter(Merchant.name == line_aux[5]).first()
		
			if (product is None):
				product = Product (line_aux[1], line_aux[2], merchant)
				print product
				db_session.add(product)
				db_session.commit()
				product = product.query.filter(Product.name == line_aux[1]).first()
	
			sale = Sale (product, client,  product.value * int(line_aux[3]), line_aux[3])
	
			db_session.add(sale)
	
			db_session.commit()				


