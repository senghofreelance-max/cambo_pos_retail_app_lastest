# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname
import itertools
import operator
import json


class Product(Document):
	def validate(self):
		product_code_prefix = frappe.db.get_value("Product Category",self.product_category,"product_code_prefix")
		if not product_code_prefix:
			frappe.throw(_("Please enter product code."))

		if self.has_value_changed("product_category"):
			if self.product_code and frappe.db.exists({"doctype": "Product", "product_code": self.product_code}):
				frappe.db.sql("""
						UPDATE `tabProduct` a
						INNER JOIN `tabProduct Category` c ON a.product_category = c.category_name
						SET a.product_group = c.parent_product_category WHERE a.name = %(name)s;
					""",{"name":self.name})
		if not self.price  and len(self.product_prices) > 0:
			default_price= [row.get("price") for row in self.get("product_prices") if row.price_code == "Default Price"]
			self.price = default_price[0] or 0
		get_default_price_code = [row.get("price_code") for row in self.get("product_prices") if row.price_code == "Default Price"]
		if len(self.get("product_prices")) > 0 and not get_default_price_code:
			frappe.throw(_("Please set product price for Default Price"), title=_("Price Required"),exc=frappe.MandatoryError)
		if not self.price and len(self.product_prices) <= 0:
			frappe.throw(_("Please set product price."), title=_("Price Required"),exc=frappe.MandatoryError)
		
		self.check_duplicate_product_prices()

	def check_duplicate_product_prices(self):

		seen = set()
		for row in self.get("product_prices"):  # child table fieldname
			key = (row.branch, row.price_code, row.uom)

			if key in seen:
				frappe.throw(
					f"Duplicate entry found in Product Prices. (Row {row.idx} Barcode {row.barcode}), "
				)
			seen.add(key)

		
	def before_save(self):
		if self.photo:
			self.display_photo = self.photo
		if not self.product_name_kh:
			self.product_name_kh = self.product_name
	
		if self.auto_generate_barcode:
			for price in self.product_prices:
				if not price.barcode:
					price.barcode =  f'{self.name}-{price.idx:02d}'
		else:
			for price in self.product_prices:
				if not price.barcode:
					frappe.throw(_("Please enter barcode for price list row {0}").format(price.idx))
		product_group = frappe.db.get_value("Product Category",self.product_category,"parent_product_category")
		self.product_group = product_group

	def on_update(self):
		delete_pos_product_sql = """
									delete from 
										`tabPOS Product` 
									where product_code = %(product_code)s
								"""
		frappe.db.sql(delete_pos_product_sql,{"product_code":self.product_code} )
		frappe.db.commit()
		pos_profile = frappe.db.get_value('Product Category', self.product_category, 'pos_profile')
		if len(self.product_prices) > 0:
			if self.disabled == 0:
				sorted_data = sorted(json.loads(frappe.as_json(self.product_prices)) , key=operator.itemgetter("branch"))
			for key, group in itertools.groupby(sorted_data, key=operator.itemgetter("branch")):
				doc = frappe.get_doc({'doctype': 'POS Product',
					'product_code': self.product_code,
					'product_name_en': self.product_name,
					'product_name_kh': self.product_name_kh,
					'product_group': self.product_group,
					'product_category': self.product_category,
					'unit': self.unit,
					'price': self.price,
					'inventory_product': self.inventory_product,
					'cost': self.cost,
					'photo': self.photo,
					'pos_profile':pos_profile,
					'display_photo': self.display_photo,
					'prices':frappe.as_json(list(group)),
					'product_data':frappe.as_json(self),
					'branch': key})
				doc.save()
		else:

			if self.disabled == 0:
				doc = frappe.get_doc({'doctype': 'POS Product',
					'product_code': self.product_code,
					'product_name_en': self.product_name,
					'product_name_kh': self.product_name_kh,
					'product_group': self.product_group,
					'product_category': self.product_category,
					'unit': self.unit,
					'price': self.price,
					'inventory_product': self.inventory_product,
					'cost': self.cost,
					'photo': self.photo,
					'pos_profile':pos_profile,
					'display_photo': self.display_photo,
					'product_data':frappe.as_json(self)
					})
				doc.save()
			
			
	def autoname(self):
		if self.auto_generate_code:
			product_code_prefix = frappe.db.get_value("Product Category",self.product_category,"product_code_prefix")
			if product_code_prefix:
				self.name = make_autoname(product_code_prefix)
			else:
				if self.product_code and not frappe.db.exists({"doctype": "Product", "product_code": self.product_code}):
					self.name = self.product_code
				else:
					frappe.throw(_("Please enter product code."))

			for price in self.product_prices:
				if not price.barcode:
					price.barcode =  f'{self.name}-{price.idx:02d}'
		else:
			for price in self.product_prices:
				if not price.barcode:
					frappe.throw(_("Please enter barcode for price list row {0}").format(price.idx))

