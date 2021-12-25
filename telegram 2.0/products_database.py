import sqlite3 as sql
from config import track_product_database

class product_database:

	def __init__(self, track_database):
		self.connection = sql.connect(track_database)
		self.cursor = self.connection.cursor()

	def select_all(self, name_table):
		with self.connection:
			try:
				table_name = str(name_table)
				return self.cursor.execute('SELECT * FROM ' + table_name).fetchall()
			except:
				return None

	def len_rows(self, name_table):
		''' the method returns the number of rows in the table '''
		try:
			table_name = str(name_table)
			arr = self.cursor.execute('SELECT * FROM ' + table_name).fetchall()
			return len(arr)
		except:
			return None


	def product_availability(self, name_category):
		try:
			with self.connection:
				return self.cursor.execute('''SELECT ab_level_three.name_product, ab_level_three.name_subcategory, 
				ab_level_three.price_product, ab_level_three.quantity_product, ab_level_one.name_category
				FROM ab_level_one INNER JOIN
				ab_level_three ON ab_level_one.name_category = ab_level_three.name_category
				WHERE ab_level_one.name_category = "''' + name_category + '";').fetchall()
		except:
			return None

	def select_level_two_item(self, name_category):
		try:
			with self.connection:
				return self.cursor.execute('''SELECT ab_level_two.id, ab_level_one.name_category, ab_level_two.name_subcategory 
				FROM ab_level_one INNER JOIN
				ab_level_two ON ab_level_one.name_category = ab_level_two.name_category
				WHERE ab_level_one.name_category = "''' + name_category + '";').fetchall()
		except:
			return None


	def select_lever_four_items(self, name_subcategory):
		try:
			with self.connection:
				return self.cursor.execute(f'SELECT * FROM ab_level_four WHERE name_subcategory = "{name_subcategory}"').fetchall()
		except:
			return None

	def select_level_four(self, name_product):
		try:
			with self.connection:
				return self.cursor.execute(f'SELECT * FROM ab_level_four WHERE name_product = "{name_product}"').fetchall()
		except:
			return None

	def delete_product_level_four(self, id_product):
		''' Delete product from ab_level_four table
			id_product: id table product
		'''
		with self.connection:
			id_product = int(id_product)
			item = self.cursor.execute(f'SELECT * FROM ab_level_four WHERE id = {id_product}').fetchall()
			self.cursor.execute(f'DELETE FROM ab_level_four WHERE id = {id_product}')
			return item

	def insert_into_level_four(self, product, name_product, name_subcategory, name_category):
		with self.connection:
			param = (
				product,
				name_product,
				name_subcategory,
				name_category,
			);
			self.cursor.execute('INSERT INTO ab_level_four(product, name_product, name_subcategory, name_category) VALUES (?,?,?,?)', param)


	def level_three_change_quantity_products(self, quantity_product, name_product):
		with self.connection:
			quantity_product = int(quantity_product)
			name_product = str(name_product)
			self.cursor.execute(f'update ab_level_three set quantity_product = {quantity_product} where name_product = "{name_product}"')

	def insert_purchased_product(self, id_user: str, product, way_product, timep):
		with self.connection:
			param = (
				id_user,
				product,
				way_product,
				timep,
			);
			self.cursor.execute(
				'INSERT INTO purchased_product(id_user, product, way_product, time) VALUES (?,?,?,?)', param,
			);
	def select_purchased_product_user(self, id_user: str):
		with self.connection:
			data_purchased_product = self.cursor.execute(f'SELECT * FROM purchased_product WHERE id_user = "{id_user}"').fetchall();
			len_data = len(data_purchased_product)
			return len_data

		

	def close(self):
		self.connection.close()


if __name__ == "__main__":
    pass