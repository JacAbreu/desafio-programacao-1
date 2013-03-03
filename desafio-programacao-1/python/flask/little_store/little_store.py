# coding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask import render_template, request, session, g, redirect, url_for, abort, flash
from werkzeug import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from database import db_session

from database import init_db
from models_little_store import Client, Sale, Merchant, Product

app = Flask(__name__)

def import_file(file_source):
	
	if (file_source):
	
		filename = secure_filename(file_source.filename)

		for line in file_source:

			line = line.decode('utf-8')

			line_aux = line.split('\t')
			
			if(line_aux[0]!= "purchaser name"):
			
				client = Client.query.filter(Client.name == line_aux[0]).first()
								
				merchant = Merchant.query.filter(Client.name == line_aux[5]).first()
				
				product = Product.query.filter(Product.name == line_aux[1]).first()
				
				if(client is None):
					client = Client (line_aux[0])
					db_session.add(client)			
					db_session.commit()		
					client = Client.query.filter(Client.name == line_aux[0]).first()
					
				if (merchant is None):
					merchant = Merchant (line_aux[5], line_aux[4])
					db_session.add(merchant)
					db_session.commit()
					merchant = Merchant.query.filter(Merchant.name == line_aux[5]).first()
					
				if (product is None):
					product = Product (line_aux[1], line_aux[2], merchant)
					db_session.add(product)
					db_session.commit()
					product = product.query.filter(Product.name == line_aux[1]).first()
				
				sale = Sale (product, client,  product.value * int(line_aux[3]), line_aux[3])
				
				db_session.add(sale)
				
				db_session.commit()				
			
@app.route("/")
def hello():

	return render_template('layout_home.html', title = "Ola! Seja bem vindo a Lojinha")

@app.route("/sale_report", methods=['POST', 'GET'])
def sale_report():

	print request
	print request.files 	
	if(request.files): 
	
		import_file(request.files['source'])
		
	sales = Sale.query.all()

	return render_template('layout_report.html', title = "Relatorio de Vendas", sales = sales)


@app.route("/checkout", methods=['POST', 'GET'])
def checkout():
	data = request.form
	
	if(data):
		client = Client.query.filter(Client.name == data.getlist("client").pop(0)).first()
		
		product = Product.query.filter(Product.name == data.getlist("product").pop(0)).first()
				
		if (client != None and product != None):
			
			value = int(data.getlist("quantity").pop(0)) * product.value
			sale = Sale(product, client, value,  int(data.getlist("quantity").pop(0)))
			db_session.add(sale)			
			db_session.commit()			
		
	return render_template('layout_entity_inclusion.html', title = "Checkout", sale="true")

	
@app.route("/new_client", methods=['POST', 'GET'])
def new_client():
	data = request.form
	client = Client( data.getlist("username").pop(0),  data.getlist("name").pop(0),  data.getlist("address").pop(0),  data.getlist("email").pop(0))
	db_session.add(client)			
	db_session.commit()			
	return render_template('layout_entity_inclusion.html', title = "Novo Cliente", client="true")
	
@app.route("/informations_client", methods=['POST', 'GET'])
def informations_client():
	data = request.form
	
	client_searched = None
	
	sale_searched = None
		
	if(data):
	
		client_searched = Client.query.filter(Client.username == data.getlist("username").pop(0)).first()
		
		sale_searched = db_session.query(func.count(Sale.id)).filter(Sale.client_id == client_searched.id).first()
		
	clients = Client.query.all()
	return render_template('layout_entity_instance_informations_view.html', title = "Cliente", client="true",  entities = clients, client_searched = client_searched, sale_searched = sale_searched )

@app.route("/infomations_checkout")
def info_client(checkout_id):
	return "futuro informacoes do checkout"

if __name__ == "__main__":
	init_db()
	app.run(debug=True)
    
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
    

__name__ = "little_store"


