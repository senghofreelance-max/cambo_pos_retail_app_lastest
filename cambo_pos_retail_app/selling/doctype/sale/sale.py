# Copyright (c) 2025, Mr.Sengho and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Sale(Document):
	def before_validate(self):
		for p in self.sale_products:
			# frappe.db.get_all('Product Price') 
			p.base_selling_price = frappe.db.get_value("Product",p.product,'price')
			if (p.discount or 0 ) > 0:
				if p.discount_type == 'Amount':
					p.sub_total = p.selling_price * float(p.quantity or 1)
					p.total_discount = p.discount
					p.gross_sale = p.quantity * p.selling_price
				elif p.discount_type == 'Percentage':
					p.total_discount = (p.discount or 0)/100 * (p.selling_price * float(p.quantity or 1))
					p.sub_total = p.selling_price * float(p.quantity or 1) - (p.total_discount or 0)
					p.gross_sale = p.quantity * p.selling_price

		self.items_count = len(self.sale_products)
		self.total_item_discount = sum([r.total_discount for r in self.sale_products])
		self.gross_sale = sum([r.quantity * r.selling_price for r in self.sale_products])
		self.discountable_amount = sum([r.quantity * r.selling_price for r in self.sale_products if r.discount == 0])
		self.total_discount_amount = self.total_item_discount + (self.discount if self.discount_type == "Amount" else (self.discount / 100) * self.discountable_amount)
		self.sub_total = sum([(r.quantity * r.selling_price) for r in self.sale_products]) - self.total_discount_amount
		
		self.additional_charge = sum([r.amount for r in self.shipping_and_charge]) or 0
		self.net_sale = sum([r.quantity * r.selling_price for r in self.sale_products]) - self.total_discount_amount + self.additional_charge
		self.grand_total = self.sub_total + self.additional_charge

	def validate(self):
		self.additional_charge = sum([r.amount for r in self.shipping_and_charge])

	@frappe.whitelist()
	def get_product_price_by_price_code(self,product):
		if not self.customer:
			frappe.throw(title='Customer Missing',msg=_("Please select a customer."))
		if not self.price_code:
			frappe.throw(title='Price Code Missing',msg=_("Please select a price code."))
		data = frappe.db.sql('SELECT * FROM `tabProduct Price` where parent = %(product)s and price_code = %(price_code)s',{'product':product,'price_code':self.price_code})
		return data

