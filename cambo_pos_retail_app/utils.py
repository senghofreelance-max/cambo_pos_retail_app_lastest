import frappe
from frappe import whitelist,_
from frappe.auth import LoginManager

# @whitelist(allow_guest=True)
# def get_product_for_home_page():
#     response_data = {}
#     arrival_list = frappe.db.get_list("Product",filters={
#         'disabled':0,
#         'new_arrival':1
#     },fields=['title','price','name','description','display_photo'])
#     response_data['new_arrival'] = {'title':_("New Arrival"),"data":arrival_list}
#     response_data['slideshow'] = slideshow
    
#     return response_data


@whitelist(allow_guest=True)
def ping():
    frappe.local.response["message"] = {'text':_("server connected success"),'status':200}


    
@frappe.whitelist(allow_guest=True,methods="POST")
def pos_login(usr="", pwd="",pos_profile=""):
        
    try:
        pos_user = frappe.db.get_all("POS Profile User",{'username': usr,"parent":pos_profile,"allow_login_pos":1},['employee','name'])
        if len(pos_user) > 0:
            response_employee = {}
            employee = frappe.get_doc("Employee",pos_user[0].get('employee'))
            pos_user_permission= frappe.get_doc("POS User Permission",employee.get("pos_role"))
            pos_permission_meta = frappe.get_meta('POS User Permission')
            _pos_permission = {}
            pos_permission_field = [ item.get("fieldname")  for item in pos_permission_meta.get("fields") if  item.get("fieldname") not in ["section","column_break_hpah"]  ]
            for pos_permission_fieldname in pos_permission_field:
                _pos_permission[pos_permission_fieldname] = pos_user_permission.get(pos_permission_fieldname)

            response_employee={
                "name":employee.get("name"),
                "employee_name":employee.get("employee_name"),
                "employee_code":employee.get("employee_code"),
                "pos_role":employee.get("pos_role"),
                "user_permission":_pos_permission
            }
        else:
            return {
            "message": "Can not login current POS",
            "error_type": "AuthenticationError"
        }
        login_manager = LoginManager()

        login_manager.authenticate(user=employee.get("username"), pwd=pwd)
        login_manager.post_login()
        
        return {
            "message": "Login successful",
            "user":response_employee
        }

    except frappe.exceptions.AuthenticationError:
        # Handle authentication failure
        frappe.local.response["http_status_code"] = 401
        return {
            "message": "Invalid login credentials",
            "error_type": "AuthenticationError"
        }

    except Exception as e:
        # Handle any other exceptions
        frappe.local.response["http_status_code"] = 500
        frappe.log_error(message=f"Login failed: {e}", title="Custom Login Error")
        return {
            "message": f"An unexpected error occurred {e}",
            "error_type": "ServerError"
        }

@frappe.whitelist(allow_guest=True)
def get_pos_config_info(pos_profile,terminal):
    pos_profile_doc = frappe.get_doc("POS Profile",pos_profile)
    pos_profile_meta =frappe.get_meta('POS Profile')
    pos_config_doc = frappe.get_doc("POS Config",pos_profile_doc.get("pos_config"))
    branch = frappe.get_doc("Branch",pos_profile_doc.get("branch"))
    terminal_doc  =frappe.get_doc("Terminal",terminal)
    pos_profile_response = {
                "pos_profile_name":pos_profile_doc.get("pos_profile_name"),
                "pos_config":pos_profile_doc.get("pos_config"),
                "permission_config":[ {"label":item.get("label"),"fieldname":item.get("fieldname"),"value":pos_profile_doc.get(item.get("fieldname"))}  for item in pos_profile_meta.get("fields") if  item.get("fieldtype") == "Check"  ],
                "pos_config":{
                    "config_name":pos_config_doc.get("onfig_name"),
                    "login_background":pos_config_doc.get("login_background"),
                    "home_background":pos_config_doc.get("home_background")
                }
            }
    return {
            "branch_name":branch.get("branch_name"),
            "address":branch.get("address"),
            "phone":branch.get("phone"),
            "contact_name":branch.get("contact_name"),
            "contact_phone":branch.get("contact_phone"),
            "pos_profile":pos_profile_response
            
    }