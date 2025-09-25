# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PriceCode(Document):
	def validate(self):
		default_exist = frappe.db.exists({"doctype": "Price Code", "is_default": 1})
		if default_exist:
			if self.is_default and default_exist != self.name:
				frappe.throw("Default Price Code is already exist")