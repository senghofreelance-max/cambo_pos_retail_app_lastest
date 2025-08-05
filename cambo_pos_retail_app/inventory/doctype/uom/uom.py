# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class UOM(Document):
	def after_insert(self):
		doc = frappe.get_doc({
			'doctype': 'UOM Conversion',
			'from': self.name,
			'to': self.name,
			'value':1
		})
		doc.insert()
