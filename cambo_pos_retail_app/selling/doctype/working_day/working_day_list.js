frappe.listview_settings['Working Day'] = {
    add_fields: ['is_closed',],
    get_indicator(doc) {
        // customize indicator color
        if (doc.is_closed) {
            return [__("Closed"), "red", "is_closed,=,1"];
        } else {
            return [__("Opening"), "green", "is_closed,=,0"];
        }
    },
}