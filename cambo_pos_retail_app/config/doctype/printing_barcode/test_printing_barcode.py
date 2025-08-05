# Copyright (c) 2025, Mr.Sengho and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestPrintingBarcode(UnitTestCase):
	"""
	Unit tests for PrintingBarcode.
	Use this class for testing individual functions and methods.
	"""

	pass


class IntegrationTestPrintingBarcode(IntegrationTestCase):
	"""
	Integration tests for PrintingBarcode.
	Use this class for testing interactions between multiple components.
	"""

	pass
