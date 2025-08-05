// Copyright (c) 2025, Mr.Sengho and contributors
// For license information, please see license.txt

frappe.ui.form.on("Product", {
    refresh(frm) {

    },
    product_category(frm, cdt, cdn) {
        frappe.db.get_value(
            "Product Category",
            frm.doc.product_category,
            "product_code_prefix",
            (val) => {
                if (val && val.product_code_prefix) {
                    frm.set_value("naming_series", val.product_code_prefix);
                } else {
                    frm.set_value("naming_series", "");
                }
            }
        );

    }
});
