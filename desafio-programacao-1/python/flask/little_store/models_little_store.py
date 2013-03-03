# coding: utf-8

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from database import Base

class Client(Base):
	__tablename__ = 'client'
	id = Column(Integer, primary_key=True)
	username = Column(String(30), unique=True)
	name = Column(String(80))
	address = Column(String(100))
	email = Column(String(120), unique=True)

	def __init__(self, name, username = None, address = None, email = None):
		self.username = username
		self.name = name
		self.address = address
		self.email = email
		
	def __repr__(self):
		return '<Client %r>' % self.id + self.name.encode('utf-8')
        
class Sale (Base):
	__tablename__ = 'sale'
	id = Column(Integer, primary_key=True)
	produt_id = Column(Integer, ForeignKey('product.id'))
	product = relationship("Product")
	value = Column(Float)
	quantity = Column(Integer)
	client_id = Column(Integer, ForeignKey('client.id'))
	client = relationship("Client")

	def __init__(self, product, client, value, quantity):
		self.product = product
		self.client = client
		self.value = value
		self.quantity = quantity
		
	def __repr__(self):
		#return '<Sale %r>' % self.id + str(self.client_id)
		return '<Sale %r>' % self.id + str(self.value)
		
class Product (Base):
	__tablename__ = 'product'
	id = Column(Integer, primary_key=True)
	name = Column(String(80))
	value = Column(Float)
	
	def __init__(self, name, value, merchant):
		self.name = name
		self.value = value
		merchant_id = Column(Integer, ForeignKey('merchant.id'))
		merchant = relationship("Merchant")
		
	def __repr__(self):
		return '<Product %r>' % self.id + self.name.encode('utf-8')
		
class Merchant(Base):
	__tablename__ = 'merchant'
	id = Column(Integer, primary_key=True)
	username = Column(String(30), unique=True)
	name = Column(String(80))
	address = Column(String(100))
	email = Column(String(120), unique=True)
	
	def __init__(self, name, address, username=None, email = None):
		self.name = name
		self.adress = address
		self.username = username
		self.email = email
		
	def __repr__(self):
		return '<Merchant %r>' % self.id + self.name.encode('utf-8')
		

