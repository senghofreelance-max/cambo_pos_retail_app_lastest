# Copyright (c) 2025, Mr.Sengho and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestSale(UnitTestCase):
	"""
	Unit tests for Sale.
	Use this class for testing individual functions and methods.
	"""

	def test_register_unregister(self):
		doc = frappe.get_doc({
			'doctype': 'Sale',
			'customer': 'CRM-0001',
			'price_code': 'Retail Price',
			'posting_date': '2025-05-07',
			'sale_date': '2025-05-07',
			'additional_charge': 1.5,
			'discount': 5,
			'discount_type':'Percentage',
			'additional_charge': 1.5,
			'sale_products':[{
				'product':'P-0001',
				'quantity':2,
				'selling_price':12.5,
				'discount':0
			},{
				'product':'RB-0002',
				'quantity':5,
				'selling_price':6.00,
				'discount_type':'Percentage',
				'discount':10
			}
			],
		})
		doc.insert()
		self.assertEqual(doc.items_count, 2)
		self.assertEqual(doc.gross_sale, 55.00,'Gross Sale')
		self.assertEqual(doc.discountable_amount,25.00,'Discountable Amount')
		self.assertEqual(doc.total_discount_amount,4.25,'Total Discount Amount')
		self.assertEqual(doc.sub_total,50.75 ,'Sub total')
		
		self.assertEqual(doc.net_sale, 52.25,'Net Sale')
		self.assertEqual(doc.grand_total, 52.25,'Grand Total')
		
		self.assertEqual(doc.discountable_amount, 25.00,'Discountable Amount')


class IntegrationTestSale(IntegrationTestCase):
	"""
	Integration tests for Sale.
	Use this class for testing interactions between multiple components.
	"""

	pass
