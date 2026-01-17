// Copyright (c) 2025, Mr.Sengho and contributors
// For license information, please see license.txt

frappe.ui.form.on("Product", {
     onload: function(frm) {
        frm.set_query("product_category", function() {
            return {
                "filters": {
                    "is_group": 0
                }
            };
        });
    },
    refresh(frm) {

    },
    product_category(frm, cdt, cdn) {
        console.log(frm)
        frappe.db.get_value(
            "Product Category",
            frm.doc.product_category,
            ["product_code_prefix","parent_product_category"],
            (val) => {
                if (val && val.product_code_prefix) {
                    frm.set_value("naming_series", val.product_code_prefix);
                    frm.set_value("product_group",val.parent_product_category)
                } else {
                    frm.set_value("naming_series", "");
                }
            }
        );
        
    }
});
