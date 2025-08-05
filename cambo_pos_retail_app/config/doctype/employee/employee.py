# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.password import update_password as _update_password


class Employee(Document):

	def autoname(self):
		if self.employee_code:
			self.name = self.employee_code
		
	def after_save(self):
		if not self.employee_code :
			self.employee_code = self.name
		if not self.user and self.allow_login_pos and self.is_new():
			self.create_new_user_with_password()
		if not self.is_new() and self.password:
			_update_password(user=self.user, pwd=self.password)

	def create_new_user_with_password(self):
		try:
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
			frappe.db.commit()
			frappe.db.set_value("Employee",self.name,'user',user.name)
				
		except Exception as e:
			frappe.db.rollback()
			frappe.throw(f"Error creating user: {e}")