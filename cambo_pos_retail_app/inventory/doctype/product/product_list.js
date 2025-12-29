frappe.listview_settings['Product'] = {
    add_fields: ['display_photo'],
    formatters: {
        display_photo(value) {

            return `<div style="border-radius:12px,height:35px;margin-right:10px;margin-left:5px'"><img src='${value || "/assets/cambo_pos_retail_app/assets/photo/Placeholder.svg"}' style="height:35px;"/></div>`;
        },

    }
}