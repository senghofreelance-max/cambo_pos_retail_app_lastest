// Copyright (c) 2025, Mr.Sengho and contributors
// For license information, please see license.txt

frappe.ui.form.on("POS Profile", {
    refresh(frm) {

    },
    setup: function (frm) {
        frm.set_query("product_category", "product_categories", function (doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return {
                filters: [
                    ["Product Category", "is_group", "=", 1],
                    ["Product Category", "category_name", "!=", "All Categories"],
                ],
            };
        });
    }
});
