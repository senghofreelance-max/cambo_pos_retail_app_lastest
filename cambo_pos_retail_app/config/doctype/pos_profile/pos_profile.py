# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class POSProfile(Document):
	def autoname(self):
		self.uniqe_name =  f"{self.pos_profile_name}_{self.branch}".replace(" ","_")

	def validate(self):
		self.remove_duplicate_payment_types()
		self.remove_duplicate_payment_product_categories()
		exchange_rate = frappe.db.sql("SELECT rate FROM `tabExchange Rate` WHERE branch = %(branch)s AND docstatus = 1 ORDER BY DATE DESC  limit 1 ",{"branch":self.branch},as_dict=1)
		if exchange_rate:
			main_currency = frappe.get_single_value("POS Setting",'main_currency')
			second_currency = frappe.get_single_value("POS Setting",'second_currency')
			main_currency_rate = 1
			second_currency_rate = 1 / exchange_rate[0].get("rate")
			for payment_type in self.payment_types:
				if payment_type.currency == main_currency:
					payment_type.exchange_rate_value = main_currency_rate
				else:
					payment_type.exchange_rate_value = second_currency_rate
		product_categories_changed = self.has_value_changed("product_categories")
		if product_categories_changed:
			pass
			
	def remove_duplicate_payment_types(self):
		seen_items = set()
		unique_rows = []

		for row in self.payment_types:
			link_field_value = row.payment_type
			
			if link_field_value not in seen_items and row.payment_type:
				seen_items.add(link_field_value)
				unique_rows.append(row)

		self.payment_types = unique_rows

	def remove_duplicate_payment_product_categories(self):
		seen_items = set()
		unique_rows = []

		for row in self.product_categories:
			link_field_value = row.product_category
			
			if link_field_value not in seen_items and row.product_category:
				seen_items.add(link_field_value)
				unique_rows.append(row)

		self.product_categories = unique_rows