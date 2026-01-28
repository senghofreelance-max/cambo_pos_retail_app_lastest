frappe.pages['testpage'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Testing',
		single_column: true
	});
	
if (window.initVueApp) {
        window.initVueApp('#vue-pos-root');
    } else {
        console.error("Vue bundle not loaded yet");
    }
}