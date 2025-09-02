frappe.listview_settings['Cashier Shift'] = {
    // Add all fields you need to access in the formatters.
    add_fields: ['is_closed', 'docstatus', 'working_date', 'working_day'],
    has_indicator_for_draft: true,
    get_indicator(doc) {
        console.log(doc.docstatus)
        if (doc.is_closed === 1) {
            return [__("Closed"), "red", "is_closed,=,1"];
        } else {
            return [__("Opening"), "blue", "is_closed,=,0"];
        }
    },
    formatters: {
        // docstatus: function (val, doc) {
        //     console.log(val)
        //     if (doc.is_closed === 1) {
        //         return '<span class="indicator-pill closed blue">' + 'Closed' + '</span>';
        //     } else {
        //         return '<span class="indicator-pill opening red">' + 'Opening' + '</span>';
        //     }


        //     return frappe.get_listview_docstatus_indicator(val);
        // },
        working_day: function (val, doc) {
            if (doc.working_day && doc.working_date) {
                return `${doc.working_day}<br>${frappe.datetime.str_to_user(doc.working_date)}`;
            }
            return val || '';
        }
    },
    column_order: ['docstatus', 'pos_profile', 'posting_date', 'terminal', 'working_day']
};