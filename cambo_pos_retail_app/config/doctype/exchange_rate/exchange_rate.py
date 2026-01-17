# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExchangeRate(Document):
	def on_submit(self):
		main_currency = frappe.get_single_value("POS Setting",'main_currency')
		second_currency = frappe.get_single_value("POS Setting",'second_currency')

		main_currency_rate = 1
		second_currency_rate = 1 / self.rate
		
		self.exchange_value = second_currency_rate

		sql = "Update `tabPOS Profile Payment Type` set exchange_rate_value = CASE WHEN currency = %(main_currency)s then %(main_currency_rate)s ELSE %(second_currency_rate)s END"
		frappe.db.sql(sql,{"exchange_rate_value":self.rate,"main_currency":main_currency,"main_currency_rate":main_currency_rate,"second_currency_rate":second_currency_rate})

		frappe.db.commit()
		