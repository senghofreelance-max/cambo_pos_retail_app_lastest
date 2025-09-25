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
		frappe.throw(_("Please select working date"),title="Invalid Data",exc=frappe.ValidationError)

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
def get_current_working_day(branch,pos_profile):
	current_shift_name = frappe.get_value("Cashier Shift",{'pos_profile':pos_profile,'branch':branch,'is_closed':0})
	working_day_name=frappe.db.get_value("Working Day",{'is_closed': 0,"branch":branch,"pos_profile":pos_profile})
	currenct_working_day = None
	current_shift=None
	if working_day_name:
		currenct_working_day = frappe.get_doc("Working Day",working_day_name)
		if current_shift_name:
			current_shift = frappe.get_doc("Cashier Shift",current_shift_name)
		
	return {"current_working_day":currenct_working_day,"current_cashier_shift":current_shift}
		
	frappe.throw("Working Day not found",exc=frappe.DoesNotExistError,title="Not Found")
	# working_day = frappe.get_doc("Working Day",{},)
	
	