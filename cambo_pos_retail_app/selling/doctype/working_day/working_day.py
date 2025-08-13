# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class WorkingDay(Document):

	def validate(self):
		last_doc = frappe.db.get_value(self.doctype, filters={"branch": self.branch,"pos_profile": self.pos_profile,"working_date": self.working_date,"is_closed":0})
		if last_doc:
			frappe.throw(_("Working day is already open"),title="Invalid Data",exc=frappe.ValidationError)
		

@frappe.whitelist()
def open_working_day(working_day):
	
	# doc = frappe.get_doc("Working Day")
	if not working_day.get("working_date"):
		frappe.throw(_("Please select opened date",title="Invalid Data",exc=frappe.ValidationError))

	doc = frappe.get_doc({
    'doctype': working_day.get("doctype"),
	"branch":  working_day.get("branch") ,
	"pos_profile": working_day.get("pos_profile"),
	"terminal": working_day.get("terminal"),
	"opened_date": working_day.get("opened_date"),
	"working_date": working_day.get("working_date"),
	"open_by": working_day.get("open_by"),
	"posting_date": frappe.utils.today(),
	"note": working_day.get("note")
})
	
	doc.insert()
	frappe.db.commit()
	return doc


@frappe.whitelist()
def get_current_shift(branch,pos_profile):
	cashier_shift = frappe.get_doc("Cashier Shift",{'is_closed': 0,"branch":branch,"pos_profile":pos_profile})
	working_day = frappe.get_doc("Working Day",cashier_shift.get("working_day"))
	
	return {
		"cashier_shift":cashier_shift,
		"working_day":working_day
	}