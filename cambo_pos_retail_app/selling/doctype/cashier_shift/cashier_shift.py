# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

from cambo_pos_retail_app.selling.doctype.working_day.working_day import get_current_working_day
import frappe
from frappe.model.document import Document


class CashierShift(Document):
	def validate(self):
		if not self.working:
			frappe.throw('Working Day is required')
		
		if self.get('shift_detail'):
			for cashfloat in self.get('shift_detail'):
				cashfloat.total_open_amount = cashfloat.input_open_amount * cashfloat.exchange_rate
			self.total_opening_amount = sum(d.total_open_amount for d in self.get('shift_detail')) 

@frappe.whitelist()
def open_cashier_shift(cashier_shift):
	
	if cashier_shift.get("details"):
		total_opening_amount = sum(d['total_open_amount'] for d in cashier_shift.get("details")) 
		
	doc = frappe.get_doc({
	'doctype': cashier_shift.get("doctype"),
	"branch":  cashier_shift.get("branch") ,
	"pos_profile": cashier_shift.get("pos_profile"),
	"opened_terminal": cashier_shift.get("opened_terminal"),
	"opened_date": cashier_shift.get("opened_date"),
	"working_date": cashier_shift.get("working_date"),
	"working_day": cashier_shift.get("working_day"),
	"opened_by": cashier_shift.get("opened_by"),
	"posting_date": frappe.utils.today(),
	"shift_detail": cashier_shift.get("details") if cashier_shift.get("details") else [],
	"note": cashier_shift.get("note"),
	"total_opening_amount":total_opening_amount or 0.00
	})
	doc.insert()
	frappe.db.commit()
	return doc