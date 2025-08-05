// Copyright (c) 2025, Mr.Sengho and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sale", {
    refresh(frm) {

    },
    customer(frm) {
        frappe.db.get_value('Customer', frm.doc.customer, 'default_price_code')
            .then(r => {
                frm.doc.price_code = r.message.default_price_code
                frm.refresh()
            })
    }
});

frappe.ui.form.on('Sale Product', {

    product(frm, cdt, cdn) {
        const row = frappe.get_doc(cdt, cdn);
        frm.call('get_product_price_by_price_code', {
            product: row.product
        })
            .then(r => {
                if (r.message) {
                    console.log(r.message);
                    // do something with linked_doc
                }
            }).catch((err) => {
                console.log(frm.get_field('products').grid.grid_rows_by_docname[cdn])
                frm.get_field('products').grid.grid_rows_by_docname[cdn].remove();
                // console.log(JSON.parse(err.responseText)['exception'])
            })
    },

})

frappe.ui.form.on('Additional Charge', {

    amount(frm, cdt, cdn) {

        calculateTotalShippingAndCharge(frm, cdt, cdn)
    },

    shipping_and_charge_remove(frm, cdt, cdn) {
        calculateAdditionalChargeTotal(frm)

    }
})
function calculateTotalShippingAndCharge(frm, cdt, cdn) {
    const row = frappe.get_doc(cdt, cdn);
    if (row.type == 'Actual') {
        row.charged_amount = row.amount

        if (frm.doc.shipping_and_charge.length > 1) {
            frm.doc.shipping_and_charge.forEach((element, idx) => {
                if (idx == frm.doc.shipping_and_charge.length - 1) {
                    row.total = frm.doc.shipping_and_charge[idx - 1].total + element.amount
                    frm.doc.grand_total = frm.doc.shipping_and_charge[idx - 1].total + element.amount
                } else {
                    row.total = frm.doc.shipping_and_charge[idx].total + element.amount
                    frm.doc.grand_total = frm.doc.shipping_and_charge[idx].total + element.amount
                }
                frm.doc.additional_charge = frm.doc.additional_charge + element.amount
            });

        } else {
            row.total = frm.doc.sub_total + row.amount
            frm.doc.additional_charge = row.amount
        }

        frm.refresh()
    }
}

function calculateAdditionalChargeTotal(frm) {
    let total = 0;
    
    let row = locals[cdt][cdn];
    row.total = flt(row.amount) + flt(row.charge_amount);
    frappe.model.set_value(cdt, cdn, 'total', row.total);

    frm.doc.shipping_and_charge.forEach(row => {
        total += flt(row.amount);
    });

    

    // If Grand Total is calculated using Additional Charge + something else, update it here
    let grand_total = total + flt(frm.doc.total_item_discount || 0); // Adjust based on your formula
    frm.set_value('grand_total', grand_total);
    frm.refresh_field('grand_total');
}
