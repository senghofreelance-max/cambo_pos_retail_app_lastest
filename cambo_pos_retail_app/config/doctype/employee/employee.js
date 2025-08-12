// Copyright (c) 2025, Mr.Sengho and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
    refresh(frm) {
        if (frm.doc.allow_login_pos && frm.doc.user) {
            frm.add_custom_button('Update Password', () => {
                let d = new frappe.ui.Dialog({
                    title: 'Update Password',
                    fields: [
                        {
                            label: 'New Passwrod',
                            fieldname: 'new_password',
                            fieldtype: 'Data'
                        },

                    ],
                    size: 'small', // small, large, extra-large 
                    primary_action_label: 'Update',
                    primary_action(values) {
                        if (!values.new_password || values.new_password.length < 6) {
                            frappe.throw("Password must be at least 6 characters long.");
                        }
                        frappe.call({
                            method: "cambo_pos_retail_app.config.doctype.employee.employee.update_password",
                            args: { name: frm.doc.name, new_password: values.new_password },
                            btn: frm.page.btn_primary,
                        }).then((r) => {
                            frappe.show_alert({
                                message: __('Password updated successfully.'),
                                indicator: 'green'
                            }, 3);

                        }).cache(() => {
                            frappe.show_alert({
                                message: __('Failed to update password. Please try again.'),
                                indicator: 'red'
                            }, 3);
                        });

                        d.hide();
                    }
                });

                d.show();
            })
        }
    },
});
