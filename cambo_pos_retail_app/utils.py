import json
import frappe
from frappe import whitelist,_
from frappe.auth import LoginManager

@whitelist(allow_guest=True)
def ping():
    frappe.local.response["message"] = {'text':_("server connected success"),'status':200}


    
@frappe.whitelist(allow_guest=True,methods="POST")
def pos_login(usr="", pwd="",pos_profile=""):
    response_employee = {}
    try:
        if usr != "cashier":
            pos_user = frappe.db.get_all("POS Profile User",{'username': usr,"parent":pos_profile,"allow_login_pos":1},['employee','name'])
            if len(pos_user) > 0:
                
                employee = frappe.get_doc("Employee",pos_user[0].get('employee'))
                pos_user_permission= frappe.get_doc("POS User Permission",employee.get("pos_role"))
                pos_permission_meta = frappe.get_meta('POS User Permission')
                _pos_permission = {}
                pos_permission_field = [ item.get("fieldname")  for item in pos_permission_meta.get("fields") if  item.get("fieldtype") == "Check"  ]
                for pos_permission_fieldname in pos_permission_field:
                    _pos_permission[pos_permission_fieldname] = pos_user_permission.get(pos_permission_fieldname)

                response_employee={
                    "name":employee.get("name"),
                    "employee_name":employee.get("employee_name"),
                    "employee_code":employee.get("employee_code"),
                    "photo":employee.get("photo"),
                    "pos_role":employee.get("pos_role"),
                    "pos_permission":_pos_permission
                }
                
            else:
                frappe.local.response["http_status_code"] = 401
                return {
                "message": "Login Invalid username or password",
                "error_type": "AuthenticationError"
            }
        else:
            pos_permission_meta = frappe.get_meta('POS User Permission')
            _pos_permission = {}
            pos_permission_field = [ item.get("fieldname")  for item in pos_permission_meta.get("fields") if  item.get("fieldtype") == "Check"  ]
            for pos_permission_fieldname in pos_permission_field:
                _pos_permission[pos_permission_fieldname] = 1
            response_employee = {
                "name": "cashier",
                "employee_name": "Cashier",
                "employee_code": "cashier",
                "pos_role": "Cashier",
                "user_permission": _pos_permission
            }

        login_manager = LoginManager()
        login_manager.authenticate(user=employee.get("username") if usr != "cashier" else "cashier", pwd=pwd)
        login_manager.post_login()
        
        return {
            "message": "Login successful",
            "user":response_employee
        }

    except frappe.exceptions.AuthenticationError as e:
        frappe.local.response["http_status_code"] = 401
        return {
            "message": f"Invalid login credentials {e}",
            "error_type": "AuthenticationError"
        }

    except Exception as e:
        frappe.local.response["http_status_code"] = 500
        frappe.log_error(message=f"Login failed: {e}", title="Custom Login Error")
        return {
            "message": f"An unexpected error occurred {e}",
            "error_type": "ServerError"
        }

def get_all_product_by_category(pos_profile,pos_profile_doc):
    product_categories = []
    if len(pos_profile_doc.get("product_categories")) > 0:
        sql = """
                WITH BaseCategories AS (
    
                    SELECT 
                        a.name,
                        a.category_name ,
                        a.parent_product_category,
                        b.idx AS sort_order,
                        a.background_color,
                        a.background_image,
                        a.text_color,
                        b.parent,
                        a.is_group,
                        a.show_in_shortcut_menu
                    FROM 
                        `tabPOS Profile Product Category` b 
                    INNER JOIN `tabProduct Category` a ON a.name = b.product_category
                    WHERE b.parent = 'Secondary_Outlet_Main_Branch' 
                )

                    
                    SELECT 
                            name,
                            category_name,
                            parent_product_category,
                            -1 AS sort_order,
                            background_color,
                            background_image,
                            text_color,
                            1 AS is_group,
                            1 AS show_in_shortcut_menu
                    FROM `tabProduct Category` 
                    WHERE name = 'All Categories'
                UNION 
                    SELECT
                        NAME,
                        category_name,
                        parent_product_category,
                        -1 AS sort_order,
                        background_color,
                        background_image,
                        text_color,
                        is_group,
                        show_in_shortcut_menu FROM BaseCategories
                    
                UNION 
                    SELECT 
                        name,
                        category_name,
                        parent_product_category,
                        -1 AS sort_order,
                        background_color,
                        background_image,
                        text_color,
                        is_group,
                        show_in_shortcut_menu
                FROM `tabProduct Category`
                WHERE parent_product_category IN (SELECT name FROM BaseCategories) 
                ORDER BY sort_order;
        """
        product_categories = frappe.db.sql(sql,{"pos_profile":pos_profile},as_dict=1)
    else:
        product_categories = frappe.db.get_list("Product Category",
                                                        ["name",
                                                         "parent_product_category",
                                                         "is_group",
                                                         "category_name",
                                                         "show_in_shortcut_menu",
                                                         "background_image",
                                                         "text_color",
                                                         "background_color",
                                                         "sort_order"],
                                                         order_by="sort_order asc")
    return product_categories



@frappe.whitelist(allow_guest=True)
def get_pos_config_info(pos_profile,terminal):
    shifts = frappe.get_list("Shift")
    pos_profile_doc = frappe.get_doc("POS Profile",pos_profile)
    pos_profile_meta =frappe.get_meta('POS Profile')
    pos_config_doc = frappe.get_doc("POS Config",pos_profile_doc.get("pos_config"))
    branch = frappe.get_doc("Branch",pos_profile_doc.get("branch"))
    terminal_doc  =frappe.get_doc("Terminal",terminal)
    pos_setting= frappe.get_single("POS Setting")
    main_currency = frappe.db.get_value("Currency",pos_setting.get("main_currency"),["symbol","number_format","custom_locale","symbol_on_right"],as_dict=1)
    second_currency = frappe.db.get_value("Currency",pos_setting.get("second_currency"),["symbol","number_format","custom_locale","symbol_on_right"],as_dict=1)
    customer_groups = frappe.db.get_list("Customer Group",["name","color"])
    price_codes = frappe.db.get_list("Price Code",["is_default","price_code","name"])
    
    product_categories = []
    product_categories = get_all_product_by_category(pos_profile,pos_profile_doc)

    default_customer = frappe.db.get_value("Customer",branch.get("default_customer"),["phone","name","customer_name"],as_dict=1)
    if not default_customer:
        default_customer = frappe.db.get_value("Customer","General Customer",["phone","name","customer_name"],as_dict=1)


    pos_profile_response = {
                "name":pos_profile_doc.get("name"),
                "pos_profile_name":pos_profile_doc.get("pos_profile_name"),
                "pos_config":pos_profile_doc.get("pos_config"),
                
                "permission_config":[ {"label":item.get("label"),"fieldname":item.get("fieldname"),"value":pos_profile_doc.get(item.get("fieldname"))}  for item in pos_profile_meta.get("fields") if  item.get("fieldtype") == "Check"  ],
                "pos_config":{
                    "config_name":pos_config_doc.get("onfig_name"),
                    "login_background":pos_config_doc.get("login_background"),
                    "home_background":pos_config_doc.get("home_background"),
                    "pos_background":pos_config_doc.get("pos_background")
                },
                "payment_types":pos_profile_doc.get("payment_types")
            }
    currency_info = []
    currency_info.append({
                    "name":pos_setting.get("main_currency"),
                    "formatter":main_currency.get("number_format"),
                    "symbol":main_currency.get("symbol"),
                    "locale":main_currency.get("custom_locale"),
                    "symbol_on_right":main_currency.get("symbol_on_right"),
             }   )
    currency_info.append({
                "name":pos_setting.get("second_currency"),
                "formatter":second_currency.get("number_format"),
                "symbol":second_currency.get("symbol"),
                "locale":second_currency.get("custom_locale"),
                "symbol_on_right":second_currency.get("symbol_on_right"),
             }  )
    return {
            "branch_name":branch.get("branch_name"),
            "default_customer_obj":default_customer,
            "default_customer":default_customer.name,
            "address":branch.get("address"),
            "phone":branch.get("phone"),
            "contact_name":branch.get("contact_name"),
            "contact_phone":branch.get("contact_phone"),
            "pos_profile":pos_profile_response,
            "shifts":shifts,
            "customer_groups":customer_groups,
            "price_codes":price_codes,
            "terminal":{
                    "name":terminal_doc.get("name"),
                    "terminal_name":terminal_doc.get("terminal_name")
                },
            "currency_info":currency_info,
            "pos_setting":{
                "default_user_avatar":pos_setting.get("default_user_avatar"),
                "can_open_day_before":pos_setting.get("can_open_day_before"),
                "can_open_day_after":pos_setting.get("can_open_day_after"),
                "main_currency":pos_setting.get("main_currency"),
                "main_currency_formatter":main_currency.get("number_format"),
                "main_currency_symbol":main_currency.get("symbol"),
                "main_currency_locale":main_currency.get("custom_locale"),
                "second_currency":pos_setting.get("second_currency"),
                "second_currency_formatter":second_currency.get("number_format"),
                "second_currency_symbol":second_currency.get("symbol"),
                "second_currency_locale":second_currency.get("custom_locale"),
                "pos_date_format":pos_setting.get("pos_date_format"),
            },
            "product_categories":product_categories
    }




@frappe.whitelist(allow_guest=1)
def get_pos_translate():
    data = frappe.db.get_all("POS Translate",['name','language_code','translate_text'])
    response = {}
    for language in data:
        response[language['language_code']] = json.loads(language.translate_text)
    return response

# @frappe.whitelist(allow_guest=1)
# def get_product_for_pos(pos_profile=None):
#     pos_profile_doc = frappe.get_doc("POS Profile",pos_profile)
#     product_categories = []
#     if len(pos_profile_doc.get("product_categories")) > 0:
#         sql = """
#                 SELECT 
#                     a.NAME product_category
#                 FROM
#                     `tabPOS Profile Product Category` b INNER JOIN `tabProduct Category` a
#                 ON a.name = b.product_category
#                 WHERE b.parent = %(pos_profile)s
#                 UNION 
#                 SELECT 
#                     NAME

#                 FROM `tabProduct Category` WHERE NAME  = 'All Categories'
#         """
#         product_categories = frappe.db.sql(sql,{"pos_profile":pos_profile},as_dict=1)

#     else:
#         product_categories = frappe.db.get_list("Product Category",filters=[['is_group',"=",0]])
#     product_data = []
#     for pc in product_categories:
#         product_list = frappe.get_list("POS Product",[
#                                                         'name',
#                                                         'product_code',
#                                                         'product_name_en',
#                                                         'product_name_kh',
#                                                         'branch','pos_profile',
#                                                         'product_data as product',
#                                                         'price',
#                                                         'prices',
#                                                         'product_group',
#                                                         'product_category'
#                                                     ],filters={"product_category":pc.get("product_category")},page_length=100)
#         product_data.append({'product_category':pc.get('product_category'),'product':product_list})
#     return product_data



@frappe.whitelist(allow_guest=1)
def get_product_for_pos(pos_profile=None):

    from itertools import chain

    pos_profile_doc = frappe.get_doc("POS Profile",pos_profile)
    product_categories = []
    product_meta = frappe.get_meta("POS Product")
    price_meta = frappe.get_meta("Product Price")

    product_field = product_meta.get_fieldnames_with_value()
    price_field = price_meta.get_fieldnames_with_value()
    product_field.insert(0,'name')
    price_field.insert(0,'name')

    if len(pos_profile_doc.get("product_categories")) > 0:
        sql = """
            WITH BaseCategories AS (
                    SELECT
                        a.NAME product_category
                    FROM
                        `tabPOS Profile Product Category` b INNER JOIN `tabProduct Category` a
                    ON a.name = b.product_category
                    WHERE b.parent = %(pos_profile)s 
                )
            SELECT category_name FROM `tabProduct Category` pc WHERE parent_product_category IN ( SELECT product_category FROM BaseCategories);


        """
        product_categories = frappe.db.sql(sql,{"pos_profile":pos_profile})

    else:
        product_categories = frappe.db.get_list("Product Category", filters=[['is_group',"=",0]],as_list=True)
    
    product_list=[]
    product_categories = list(chain.from_iterable(product_categories)) # Merge nest array into single array
    # return product_categories

    for c in product_categories:
        product_by_category = frappe.get_list(
                                "POS Product",product_field,
                                filters={"product_category":c},
                                page_length=25,
                                order_by='product_code',
                                as_list=1)
        if len(product_by_category) > 0:
            product_list.append({"category":c,"products":product_by_category})
    return {"product_field":product_field,"category_products":product_list,"price_field":price_field}


@frappe.whitelist()
def get_customer_list_for_pos(keyword=None,page_length=25,start=1):
    filters = {'keyword': ['like', f'%{keyword}%']}
    customer_list = frappe.db.get_list('Customer',
    filters=filters,
    fields=['name', 'customer_name','phone','customer_group','default_price_code'],
    order_by='customer_name asc',
    page_length=page_length,
    start=start
)
    print(f"{keyword}")
    return customer_list

@frappe.whitelist()
def get_customer_by_code():
    pass


@frappe.whitelist()
def get_customer_by_keyword(keyword=None):
    if keyword:
        filters = {'keyword': ['like', f'%{keyword}%']}
        customer_list = frappe.db.get_list('Customer',
        filters=filters,
        fields=['name', 'customer_name','phone','customer_group','default_price_code'],
        order_by='customer_name asc',

    )
    print(f"{keyword}")
    return customer_list



