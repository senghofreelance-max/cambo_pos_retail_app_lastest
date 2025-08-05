# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class Product(Document):
	def validate(self):
		product_code_prefix = frappe.db.get_value("Product Category",self.product_category,"product_code_prefix")
		if not product_code_prefix:
			frappe.throw(_("Please enter product code."))
	def before_save(self):
		if self.photo:
			self.display_photo = self.photo

	def autoname(self):
		if self.auto_generate_code:
			product_code_prefix = frappe.db.get_value("Product Category",self.product_category,"product_code_prefix")
			if product_code_prefix:
				self.name = make_autoname(product_code_prefix)
			else:
				if self.product_code and frappe.db.exist:
					self.name = self.product_code
				else:
					frappe.throw(_("Please enter product code."))