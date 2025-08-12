# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.password import update_password as _update_password


class Employee(Document):
	def validate(self):
		if self.password and len(self.password) < 6:
			frappe.throw(_("Password must be at least 6 characters long."))
		if self.has_value_changed("disabled"):
			frappe.db.set_value("User", self.user, "enabled", not self.disabled)

	def autoname(self):
		if self.employee_code:
			self.name = self.employee_code
		if not self.employee_code:
			self.employee_code = self.name
		
	def after_insert(self):
		if not self.employee_code:
			self.employee_code = self.name
		
		if self.allow_login_pos:
			self.create_new_user_with_password()

		# self.password=""
		# self.save()


	def create_new_user_with_password(self):
		if not self.role_profile:
			frappe.throw("Please select role profile.")
		user = frappe.get_doc({
			"doctype": "User",
			"email": self.email or  f"{self.employee_name}@mail.com",
			"full_name": self.employee_name,
			"first_name": self.employee_name,
			"new_password": self.password,
			"user_type":"System User",
			"send_welcome_email": 0
		})
		
		user.insert()
		if self.role_profile:
			user.append("role_profiles", {"role_profile": self.role_profile})
		if self.module_profile:
			user.module_profile = self.module_profile
		
		user.save()
		frappe.db.set_value("Employee",self.name,'user',user.name)
		# _update_password(self.user, self.password)
		

@frappe.whitelist()
def update_password(name,new_password):
	if not new_password:
		frappe.throw(_("Password is required for the employee."))
	if len(new_password) < 6:
		frappe.throw(_("Password must be at least 6 characters long."))
	try:
		user = frappe.db.get_value("Employee", name, "user")
		if user:
			_update_password(user, new_password)
	except Exception as e:
		frappe.throw(f"Error updating password: {e}")