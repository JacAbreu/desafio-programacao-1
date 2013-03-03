import os
from flask import Flask
import unittest
import tempfile
import little_store

class LittleStoreTestCase(unittest.TestCase):
	def setUp(self):
		self.db_fd, little_store.app.config['DATABASE'] = tempfile.mkstemp()
		little_store.app.config['TESTING'] = True
		self.app = little_store.app.test_client()
		little_store.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(little_store.app.config['DATABASE'])

	def test_raiz_application_rout(self):
		rv = self.app.get('/')
		self.assertIsNotNone(rv.data)
		
	def test_hello(self):
		result = self.app
		print result

if __name__ == '__main__':
    unittest.main()
