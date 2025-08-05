frappe.listview_settings['Product'] = {
    add_fields: ['display_photo'],
    formatters: {
        display_photo(value) {

            return `<img src='${value || "/assets/estc_app/images/avatar-2.png"}' style='border-radius: 50%;height:35px; margin-right:10px;margin-left:5px'/>`;
        },

    }
}