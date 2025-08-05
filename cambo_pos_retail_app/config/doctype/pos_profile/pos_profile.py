# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class POSProfile(Document):
	def autoname(self):
		self.uniqe_name =  f"{self.pos_profile_name}_{self.branch}".replace(" ","_")
