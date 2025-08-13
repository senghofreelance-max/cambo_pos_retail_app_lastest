// Copyright (c) 2025, Mr.Sengho and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cashier Shift", {
    refresh(frm) {
        frm.set_query('working_day', () => {
            return {
                filters: {
                    is_closed: 0
                }
            }
        })
    },
});
