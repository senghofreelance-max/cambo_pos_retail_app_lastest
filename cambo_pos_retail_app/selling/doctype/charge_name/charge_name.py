# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ChargeName(Document):
	def validate(self):
		if frappe.db.exists({"doctype": "Charge Name", "charge_name": self.charge_name}):
			frappe.throw(_("Charge name is already exist."))