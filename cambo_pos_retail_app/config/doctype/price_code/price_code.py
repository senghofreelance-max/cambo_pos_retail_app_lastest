# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PriceCode(Document):
	def before_rename(self, old, new,merge=False):
		if self.built_in == 1:
			frappe.throw(
			_("Price code **{0}** is not allowed rename.").format(frappe.bold(old)),
			title=_("Operation Not Allowed")
		)
	# def validate(self):
	# 	default_exist = frappe.db.exists({"doctype": "Price Code", "is_default": 1})
	# 	if default_exist:
	# 		if self.is_default and default_exist != self.name:
	# 			frappe.throw("Default Price Code is already exist")