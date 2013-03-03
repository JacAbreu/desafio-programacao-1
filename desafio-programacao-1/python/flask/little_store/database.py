import sqlite3
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///little_store.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	import models_little_store
	Base.metadata.create_all(bind=engine)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////flask/little_store.db'
#db = SQLAlchemy(app)


