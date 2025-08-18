# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class POSSetting(Document):
	def validate(self):
		if self.main_currency == self.second_currency:
			frappe.throw(_("Main and Second Currency cannot be the same"))