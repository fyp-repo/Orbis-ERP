import frappe
import frappe.permissions

COMPANY = 'Orbis Car Manufacturing (Pvt.) Ltd.'
ABBR = 'OCM'
CURRENCY = 'PKR'

def run():
    frappe.set_user('Administrator')
    print('====================================================================')
    print('   STEP 5: CONFIGURE USERS, ROLES, PERMISSIONS, WORKSPACES & DATA    ')
    print('====================================================================\n')

    # -------------------------------------------------------------------------
    # 1. CONFIGURE EXISTING USERS & ROLE ASSIGNMENTS
    # -------------------------------------------------------------------------
    print('--- 1. Configuring Existing Users & Role Assignments ---')
    user_roles_map = {
        'forw8007+salesmanager@gmail.com': {
            'name': 'Ali Khan',
            'department': 'Sales',
            'roles': ['Sales Manager', 'Desk User', 'Employee']
        },
        'forw8007+purchasemanager@gmail.com': {
            'name': 'Ahmed Raza',
            'department': 'Purchasing',
            'roles': ['Purchase Manager', 'Desk User', 'Employee']
        },
        'forw8007+stockmanager@gmail.com': {
            'name': 'Usman Ali',
            'department': 'Inventory / Stock',
            'roles': ['Stock Manager', 'Desk User', 'Employee']
        },
        'forw8007+manufacturingmanager@gmail.com': {
            'name': 'Hassan Malik',
            'department': 'Manufacturing / Production',
            'roles': ['Manufacturing Manager', 'Desk User', 'Employee']
        },
        'forw8007+flooruser1@gmail.com': {
            'name': 'Hamza Ahmed',
            'department': 'Shop Floor / Production Operations',
            'roles': ['Shop Floor User', 'Desk User', 'Employee']
        },
        'forw8007+flooruser2@gmail.com': {
            'name': 'Bilal Khan',
            'department': 'Shop Floor / Production Operations',
            'roles': ['Shop Floor User', 'Desk User', 'Employee']
        },
        'forw8007+qualitymanager@gmail.com': {
            'name': 'Sara Ahmed',
            'department': 'Quality Control',
            'roles': ['Quality Manager', 'Desk User', 'Employee']
        },
        'forw8007+deliverymanager@gmail.com': {
            'name': 'Usman Shah',
            'department': 'Delivery / Logistics',
            'roles': ['Delivery Manager', 'Desk User', 'Employee']
        },
        'forw8007+accountsmanager@gmail.com': {
            'name': 'Ayesha Khan',
            'department': 'Accounts / Finance',
            'roles': ['Accounts Manager', 'Desk User', 'Employee']
        },
        'forw8007+hrmanager@gmail.com': {
            'name': 'Fatima Ali',
            'department': 'Human Resources',
            'roles': ['HR Manager', 'Desk User', 'Employee']
        }
    }

    # Ensure roles exist in Frappe
    all_needed_roles = [
        'Sales Manager', 'Purchase Manager', 'Stock Manager', 'Manufacturing Manager',
        'Shop Floor User', 'Quality Manager', 'Delivery Manager', 'Accounts Manager',
        'HR Manager', 'Desk User', 'Employee'
    ]
    for r in all_needed_roles:
        if not frappe.db.exists('Role', r):
            role_doc = frappe.new_doc('Role')
            role_doc.role_name = r
            role_doc.desk_access = 1
            role_doc.insert(ignore_permissions=True)
            print(f'Created Role: {r}')

    for email, uinfo in user_roles_map.items():
        if frappe.db.exists('User', email):
            u = frappe.get_doc('User', email)
            # Remove all roles and set exact roles
            u.set('roles', [])
            for r in uinfo['roles']:
                u.append('roles', {'role': r})
            u.save(ignore_permissions=True)
            print(f'Updated user roles for {uinfo["name"]} ({email}): {uinfo["roles"]}')
        else:
            print(f'WARNING: User {email} not found!')

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 2. CONFIGURE GRANULAR DOCTYPE PERMISSIONS (CUSTOM DOCPERM)
    # -------------------------------------------------------------------------
    print('\n--- 2. Configuring Custom DocPerm Permissions ---')

    def set_custom_perm(doctype, role, perm_dict):
        """Sets exact permissions for role on doctype using Custom DocPerm."""
        if not frappe.db.exists('DocType', doctype):
            return
        # Ensure custom perms are initialized for this DocType
        if doctype not in frappe.permissions.get_doctypes_with_custom_docperms():
            frappe.permissions.setup_custom_perms(doctype)

        # Check existing Custom DocPerm for this role
        existing = frappe.db.get_value('Custom DocPerm', {'parent': doctype, 'role': role, 'permlevel': 0}, 'name')
        if not existing:
            cdp = frappe.new_doc('Custom DocPerm')
            cdp.parent = doctype
            cdp.parenttype = 'DocType'
            cdp.parentfield = 'permissions'
            cdp.role = role
            cdp.permlevel = 0
        else:
            cdp = frappe.get_doc('Custom DocPerm', existing)

        # Set all properties
        for prop in ['read', 'write', 'create', 'submit', 'cancel', 'delete', 'amend', 'report', 'export', 'print', 'email']:
            val = perm_dict.get(prop, 0)
            setattr(cdp, prop, 1 if val else 0)

        cdp.save(ignore_permissions=True)

    def remove_custom_perm(doctype, role):
        """Removes permission for role on doctype if exists in Custom DocPerm."""
        if not frappe.db.exists('DocType', doctype):
            return
        if doctype not in frappe.permissions.get_doctypes_with_custom_docperms():
            frappe.permissions.setup_custom_perms(doctype)
        frappe.db.delete('Custom DocPerm', {'parent': doctype, 'role': role})

    # Perm configurations according to sections 4-12
    # 1. Sales Manager (Section 4)
    set_custom_perm('Customer', 'Sales Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Lead', 'Sales Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Opportunity', 'Sales Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Quotation', 'Sales Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Sales Order', 'Sales Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Sales Invoice', 'Sales Manager', {'read': 1, 'write': 0, 'create': 0, 'submit': 0, 'report': 1, 'print': 1})
    set_custom_perm('Delivery Note', 'Sales Manager', {'read': 1, 'write': 0, 'create': 0, 'submit': 0, 'report': 1, 'print': 1})
    set_custom_perm('Item', 'Sales Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1, 'print': 1})
    set_custom_perm('BOM', 'Sales Manager', {'read': 1, 'write': 0, 'create': 0, 'submit': 0})
    remove_custom_perm('Payment Entry', 'Sales Manager')
    remove_custom_perm('Purchase Order', 'Sales Manager')
    remove_custom_perm('Purchase Receipt', 'Sales Manager')
    remove_custom_perm('Work Order', 'Sales Manager')
    remove_custom_perm('Quality Inspection', 'Sales Manager')
    remove_custom_perm('Employee', 'Sales Manager')
    remove_custom_perm('Role', 'Sales Manager')

    # 2. Purchase Manager (Section 5)
    set_custom_perm('Supplier', 'Purchase Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Material Request', 'Purchase Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Request for Quotation', 'Purchase Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Purchase Order', 'Purchase Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Purchase Receipt', 'Purchase Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Item', 'Purchase Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1, 'print': 1})
    set_custom_perm('Stock Entry', 'Purchase Manager', {'read': 1, 'write': 0, 'create': 0, 'submit': 0})
    remove_custom_perm('Sales Order', 'Purchase Manager')
    remove_custom_perm('Work Order', 'Purchase Manager')
    remove_custom_perm('BOM', 'Purchase Manager')
    remove_custom_perm('Quality Inspection', 'Purchase Manager')
    remove_custom_perm('Payment Entry', 'Purchase Manager')
    remove_custom_perm('Employee', 'Purchase Manager')
    remove_custom_perm('Role', 'Purchase Manager')

    # 3. Stock Manager (Section 6)
    set_custom_perm('Item', 'Stock Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Warehouse', 'Stock Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Stock Entry', 'Stock Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Stock Reconciliation', 'Stock Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Batch', 'Stock Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Serial No', 'Stock Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Purchase Receipt', 'Stock Manager', {'read': 1, 'write': 0, 'create': 0, 'submit': 0, 'report': 1})
    set_custom_perm('Delivery Note', 'Stock Manager', {'read': 1, 'write': 0, 'create': 0, 'submit': 0, 'report': 1})
    remove_custom_perm('Employee', 'Stock Manager')
    remove_custom_perm('Role', 'Stock Manager')

    # 4. Manufacturing Manager (Section 7)
    set_custom_perm('BOM', 'Manufacturing Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Work Order', 'Manufacturing Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Job Card', 'Manufacturing Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Operation', 'Manufacturing Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Workstation', 'Manufacturing Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Production Plan', 'Manufacturing Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Stock Entry', 'Manufacturing Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Item', 'Manufacturing Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Warehouse', 'Manufacturing Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Sales Order', 'Manufacturing Manager', {'read': 1, 'write': 0, 'create': 0, 'submit': 0})
    set_custom_perm('Purchase Order', 'Manufacturing Manager', {'read': 1, 'write': 0, 'create': 0, 'submit': 0})
    remove_custom_perm('Employee', 'Manufacturing Manager')
    remove_custom_perm('Role', 'Manufacturing Manager')

    # 5. Shop Floor User (Section 8)
    set_custom_perm('Job Card', 'Shop Floor User', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Work Order', 'Shop Floor User', {'read': 1, 'write': 0, 'create': 0, 'submit': 0, 'report': 1})
    set_custom_perm('BOM', 'Shop Floor User', {'read': 1, 'write': 0, 'create': 0, 'submit': 0, 'report': 1})
    set_custom_perm('Operation', 'Shop Floor User', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Workstation', 'Shop Floor User', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Item', 'Shop Floor User', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Stock Entry', 'Shop Floor User', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1})
    remove_custom_perm('Customer', 'Shop Floor User')
    remove_custom_perm('Supplier', 'Shop Floor User')
    remove_custom_perm('Sales Order', 'Shop Floor User')
    remove_custom_perm('Purchase Order', 'Shop Floor User')
    remove_custom_perm('Employee', 'Shop Floor User')
    remove_custom_perm('Role', 'Shop Floor User')

    # 6. Quality Manager (Section 9)
    set_custom_perm('Quality Inspection', 'Quality Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'cancel': 1, 'report': 1, 'print': 1})
    set_custom_perm('Quality Inspection Template', 'Quality Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Quality Inspection Parameter', 'Quality Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Item', 'Quality Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Work Order', 'Quality Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Job Card', 'Quality Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Batch', 'Quality Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Serial No', 'Quality Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Warehouse', 'Quality Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    remove_custom_perm('Sales Order', 'Quality Manager')
    remove_custom_perm('Purchase Order', 'Quality Manager')
    remove_custom_perm('Employee', 'Quality Manager')
    remove_custom_perm('Role', 'Quality Manager')

    # 7. Delivery Manager (Section 10)
    set_custom_perm('Delivery Note', 'Delivery Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Delivery Trip', 'Delivery Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Sales Order', 'Delivery Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Customer', 'Delivery Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Item', 'Delivery Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Warehouse', 'Delivery Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    remove_custom_perm('Purchase Order', 'Delivery Manager')
    remove_custom_perm('Work Order', 'Delivery Manager')
    remove_custom_perm('BOM', 'Delivery Manager')
    remove_custom_perm('Payment Entry', 'Delivery Manager')
    remove_custom_perm('Employee', 'Delivery Manager')
    remove_custom_perm('Role', 'Delivery Manager')

    # 8. Accounts Manager (Section 11)
    set_custom_perm('Sales Invoice', 'Accounts Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Purchase Invoice', 'Accounts Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Payment Entry', 'Accounts Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('Journal Entry', 'Accounts Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    set_custom_perm('GL Entry', 'Accounts Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1, 'export': 1})
    set_custom_perm('Account', 'Accounts Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    if frappe.db.exists('DocType', 'Budget'):
        set_custom_perm('Budget', 'Accounts Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1})
    remove_custom_perm('Work Order', 'Accounts Manager')
    remove_custom_perm('BOM', 'Accounts Manager')
    remove_custom_perm('Employee', 'Accounts Manager')
    remove_custom_perm('Role', 'Accounts Manager')

    # 9. HR Manager (Section 12)
    set_custom_perm('Employee', 'HR Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Department', 'HR Manager', {'read': 1, 'write': 0, 'create': 0, 'report': 1})
    set_custom_perm('Designation', 'HR Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1, 'print': 1})
    set_custom_perm('Timesheet', 'HR Manager', {'read': 1, 'write': 1, 'create': 1, 'submit': 1, 'report': 1, 'print': 1})
    if frappe.db.exists('DocType', 'Holiday List'):
        set_custom_perm('Holiday List', 'HR Manager', {'read': 1, 'write': 1, 'create': 1, 'report': 1})
    # STRICT HR RESTRICTIONS
    remove_custom_perm('Role', 'HR Manager')
    remove_custom_perm('User', 'HR Manager')

    frappe.clear_cache()
    frappe.db.commit()
    print('Custom DocPerm configurations completed successfully.')

    # -------------------------------------------------------------------------
    # 3. CONFIGURE WORKSPACE / MODULE VISIBILITY (Section 14)
    # -------------------------------------------------------------------------
    print('\n--- 3. Configuring Workspace / Module Visibility ---')
    workspace_visibility = {
        'Selling': ['Sales Manager', 'Delivery Manager', 'Accounts Manager', 'System Manager', 'Administrator'],
        'Buying': ['Purchase Manager', 'Accounts Manager', 'System Manager', 'Administrator'],
        'Stock': ['Stock Manager', 'Manufacturing Manager', 'Delivery Manager', 'Shop Floor User', 'Accounts Manager', 'System Manager', 'Administrator'],
        'Manufacturing': ['Manufacturing Manager', 'Shop Floor User', 'Quality Manager', 'System Manager', 'Administrator'],
        'Quality': ['Quality Manager', 'System Manager', 'Administrator'],
        'Invoicing': ['Accounts Manager', 'System Manager', 'Administrator'],
        'Financial Reports': ['Accounts Manager', 'System Manager', 'Administrator'],
        'Projects': ['Manufacturing Manager', 'System Manager', 'Administrator'],
        'Assets': ['Accounts Manager', 'Manufacturing Manager', 'System Manager', 'Administrator'],
        'Subcontracting': ['System Manager', 'Administrator'],
        'Support': ['System Manager', 'Administrator'],
        'CRM': ['System Manager', 'Administrator'],
        'ERPNext Settings': ['System Manager', 'Administrator'],
        'Users': ['System Manager', 'Administrator'],
        'Build': ['System Manager', 'Administrator'],
        'Integrations': ['System Manager', 'Administrator'],
        'Website': ['System Manager', 'Administrator'],
        'Welcome Workspace': ['System Manager', 'Administrator']
    }

    # Ensure Human Resources workspace exists
    if not frappe.db.exists('Workspace', 'Human Resources'):
        hr_ws = frappe.new_doc('Workspace')
        hr_ws.name = 'Human Resources'
        hr_ws.label = 'Human Resources'
        hr_ws.title = 'Human Resources'
        hr_ws.module = 'Setup'
        hr_ws.public = 1
        hr_ws.icon = 'users'
        hr_ws.type = 'Workspace'
        hr_ws.insert(ignore_permissions=True)
        print('Created Human Resources Workspace')

    workspace_visibility['Human Resources'] = ['HR Manager', 'System Manager', 'Administrator']

    for ws_name, allowed_roles in workspace_visibility.items():
        if frappe.db.exists('Workspace', ws_name):
            ws = frappe.get_doc('Workspace', ws_name)
            if not ws.type:
                ws.type = 'Workspace'
            ws.set('roles', [])
            for r in allowed_roles:
                ws.append('roles', {'role': r})
            ws.save(ignore_permissions=True)
            print(f'Configured Workspace [{ws_name}] for roles: {allowed_roles}')

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 4. VEHICLE MASTER DATA - ITEM CODES (Section 18)
    # -------------------------------------------------------------------------
    print('\n--- 4. Ensuring Vehicle Master Data & Item Codes ---')
    car_codes = [
        ('OCM-CAR-O1', 'Orbis O1 Sedan', 6500000),
        ('OCM-CAR-X1', 'Orbis X1 SUV', 11500000),
        ('OCM-CAR-E1', 'Orbis E1 Electric', 14000000)
    ]
    for code, car_name, price in car_codes:
        if not frappe.db.exists('Item', code):
            car_item = frappe.new_doc('Item')
            car_item.item_code = code
            car_item.item_name = car_name
            car_item.item_group = 'Finished Cars'
            car_item.stock_uom = 'Nos'
            car_item.is_stock_item = 1
            car_item.include_item_in_manufacturing = 1
            car_item.valuation_rate = price
            car_item.default_warehouse = f'Finished Goods Warehouse - {ABBR}'
            car_item.insert(ignore_permissions=True)
            print(f'Created Item with Code {code}: {car_name}')
        else:
            print(f'Item Code exists: {code}')

        # Add price in Standard Selling
        if not frappe.db.exists('Item Price', {'item_code': code, 'price_list': 'Standard Selling'}):
            ip = frappe.new_doc('Item Price')
            ip.item_code = code
            ip.price_list = 'Standard Selling'
            ip.price_list_rate = price
            ip.currency = CURRENCY
            ip.insert(ignore_permissions=True)

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 5. QUALITY DATA: PARAMETERS & TEMPLATE (Section 30)
    # -------------------------------------------------------------------------
    print('\n--- 5. Configuring Quality Parameters & Template ---')
    qa_params = [
        'Body Quality',
        'Paint Quality',
        'Brake Test',
        'Electrical System',
        'Battery Test',
        'Engine Test',
        'Suspension Test',
        'Final Safety Test'
    ]
    for p in qa_params:
        if not frappe.db.exists('Quality Inspection Parameter', p):
            qip = frappe.new_doc('Quality Inspection Parameter')
            qip.parameter = p
            qip.description = f'Standard automobile quality verification for {p}'
            qip.insert(ignore_permissions=True)
            print(f'Created Quality Parameter: {p}')
        else:
            print(f'Quality Parameter exists: {p}')

    template_name = 'OCM Automobile Quality Inspection Template'
    if not frappe.db.exists('Quality Inspection Template', template_name):
        qit = frappe.new_doc('Quality Inspection Template')
        qit.quality_inspection_template_name = template_name
        for p in qa_params:
            qit.append('item_quality_inspection_parameter', {
                'specification': p,
                'numeric': 0
            })
        qit.insert(ignore_permissions=True)
        print(f'Created Quality Inspection Template: {template_name}')
    else:
        print(f'Quality Inspection Template exists: {template_name}')

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 6. PROJECTS & TASKS (Section 34)
    # -------------------------------------------------------------------------
    print('\n--- 6. Configuring OCM Projects & Tasks ---')
    projects_config = [
        {
            'name': 'OCM O1 Sedan Production Project',
            'tasks': ['Component Procurement', 'Prototype Assembly', 'Testing', 'Quality Approval', 'Production Readiness']
        },
        {
            'name': 'OCM X1 SUV Production Improvement',
            'tasks': ['Design Optimization', 'Chassis Reinforcement', 'Suspension Tuning', 'Production Line Setup', 'Quality Sign-Off']
        },
        {
            'name': 'OCM E1 Electric Vehicle Development',
            'tasks': ['Battery Pack Architecture', 'Electric Motor Integration', 'BMS Firmware Validation', 'Crash & HV Safety Testing', 'Pilot Production']
        }
    ]

    for proj in projects_config:
        proj_name = proj['name']
        if not frappe.db.exists('Project', {'project_name': proj_name}):
            pdoc = frappe.new_doc('Project')
            pdoc.project_name = proj_name
            pdoc.company = COMPANY
            pdoc.status = 'Open'
            pdoc.insert(ignore_permissions=True)
            print(f'Created Project: {proj_name}')
        else:
            pdoc_name = frappe.db.get_value('Project', {'project_name': proj_name}, 'name')
            pdoc = frappe.get_doc('Project', pdoc_name)
            print(f'Project exists: {proj_name}')

        # Add tasks
        for t_subj in proj['tasks']:
            if not frappe.db.exists('Task', {'subject': f'{t_subj} ({proj_name[:12]})'}):
                tdoc = frappe.new_doc('Task')
                tdoc.subject = f'{t_subj} ({proj_name[:12]})'
                tdoc.project = pdoc.name
                tdoc.status = 'Open'
                tdoc.company = COMPANY
                tdoc.insert(ignore_permissions=True)

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 7. ASSETS & WORKSTATION MACHINERY (Section 35)
    # -------------------------------------------------------------------------
    print('\n--- 7. Configuring OCM Manufacturing Assets ---')
    # Ensure Asset Category exists
    if not frappe.db.exists('Asset Category', 'Manufacturing Machinery'):
        ac = frappe.new_doc('Asset Category')
        ac.asset_category_name = 'Manufacturing Machinery'
        # Link accounts if available
        fixed_asset_account = frappe.db.get_value('Account', {'company': COMPANY, 'account_type': 'Fixed Asset'}, 'name')
        accum_depr_account = frappe.db.get_value('Account', {'company': COMPANY, 'account_type': 'Accumulated Depreciation'}, 'name')
        depr_expense_account = frappe.db.get_value('Account', {'company': COMPANY, 'account_type': 'Depreciation'}, 'name')
        if fixed_asset_account:
            ac.append('accounts', {
                'company_name': COMPANY,
                'fixed_asset_account': fixed_asset_account,
                'accumulated_depreciation_account': accum_depr_account or fixed_asset_account,
                'depreciation_expense_account': depr_expense_account or fixed_asset_account
            })
        ac.insert(ignore_permissions=True)
        print('Created Asset Category: Manufacturing Machinery')

    # Ensure Location exists
    location_name = 'OCM Assembly Plant - Karachi'
    if not frappe.db.exists('Location', location_name):
        loc = frappe.new_doc('Location')
        loc.location_name = location_name
        loc.insert(ignore_permissions=True)
        print(f'Created Location: {location_name}')

    assets_config = [
        ('CNC Body Cutting Machine', 'Manufacturing / Production', 4500000),
        ('Vehicle Paint Booth', 'Shop Floor / Production Operations', 8000000),
        ('Engine Assembly Machine', 'Manufacturing / Production', 6500000),
        ('Welding Station', 'Shop Floor / Production Operations', 3200000),
        ('Vehicle Testing Machine', 'Quality Control', 5000000),
        ('Battery Testing Equipment', 'Quality Control', 7500000)
    ]

    for asset_name, dept_name, cost in assets_config:
        # Create an Item for this asset
        dept_actual = f"{dept_name} - {ABBR}" if frappe.db.exists('Department', f"{dept_name} - {ABBR}") else dept_name
        item_code = f'ASSET-{asset_name[:15].strip().replace(" ", "-").upper()}'
        if not frappe.db.exists('Item', item_code):
            ai = frappe.new_doc('Item')
            ai.item_code = item_code
            ai.item_name = asset_name
            ai.item_group = 'Manufactured Components'
            ai.stock_uom = 'Nos'
            ai.is_stock_item = 0
            ai.is_fixed_asset = 1
            ai.asset_category = 'Manufacturing Machinery'
            ai.insert(ignore_permissions=True)

        if not frappe.db.exists('Asset', {'asset_name': asset_name}):
            try:
                ad = frappe.new_doc('Asset')
                ad.asset_name = asset_name
                ad.item_code = item_code
                ad.company = COMPANY
                ad.department = dept_actual
                ad.location = location_name
                ad.gross_purchase_amount = cost
                ad.net_purchase_amount = cost
                ad.purchase_date = '2026-01-15'
                ad.is_existing_asset = 1
                ad.calculate_depreciation = 0
                ad.insert(ignore_permissions=True)
                print(f'Created Asset: {asset_name} ({dept_actual})')
            except Exception as e:
                print(f'Notice on Asset {asset_name}: {e}')
        else:
            print(f'Asset exists: {asset_name}')

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 8. HR DATA: EMPLOYEES, DESIGNATIONS & TIMESHEETS (Section 33)
    # -------------------------------------------------------------------------
    print('\n--- 8. Configuring HR Data & Timesheets ---')
    emp_map = [
        ('Ali Khan', 'Sales Manager', 'Sales', 'forw8007+salesmanager@gmail.com'),
        ('Ahmed Raza', 'Purchase Manager', 'Purchasing', 'forw8007+purchasemanager@gmail.com'),
        ('Usman Ali', 'Stock Manager', 'Inventory / Stock', 'forw8007+stockmanager@gmail.com'),
        ('Hassan Malik', 'Manufacturing Manager', 'Manufacturing / Production', 'forw8007+manufacturingmanager@gmail.com'),
        ('Hamza Ahmed', 'Shop Floor User', 'Shop Floor / Production Operations', 'forw8007+flooruser1@gmail.com'),
        ('Bilal Khan', 'Shop Floor User', 'Shop Floor / Production Operations', 'forw8007+flooruser2@gmail.com'),
        ('Sara Ahmed', 'Quality Manager', 'Quality Control', 'forw8007+qualitymanager@gmail.com'),
        ('Usman Shah', 'Delivery Manager', 'Delivery / Logistics', 'forw8007+deliverymanager@gmail.com'),
        ('Ayesha Khan', 'Accounts Manager', 'Accounts / Finance', 'forw8007+accountsmanager@gmail.com'),
        ('Fatima Ali', 'HR Manager', 'Human Resources', 'forw8007+hrmanager@gmail.com')
    ]

    for name, desig, dept, email in emp_map:
        dept_actual = f"{dept} - {ABBR}" if frappe.db.exists('Department', f"{dept} - {ABBR}") else dept
        if not frappe.db.exists('Designation', desig):
            d = frappe.new_doc('Designation')
            d.designation_name = desig
            d.insert(ignore_permissions=True)

        emp_name = frappe.db.get_value('Employee', {'user_id': email}, 'name')
        if emp_name:
            emp = frappe.get_doc('Employee', emp_name)
            emp.first_name = name.split()[0]
            emp.last_name = name.split()[1] if len(name.split()) > 1 else ''
            emp.employee_name = name
            emp.designation = desig
            emp.department = dept_actual
            emp.company = COMPANY
            emp.status = 'Active'
            emp.save(ignore_permissions=True)
            print(f'Updated Employee: {name} -> {desig} in {dept_actual}')

    # Sample Timesheet for Hassan Malik (Manufacturing Manager)
    hassan_emp = frappe.db.get_value('Employee', {'user_id': 'forw8007+manufacturingmanager@gmail.com'}, 'name')
    if hassan_emp and not frappe.db.exists('Timesheet', {'employee': hassan_emp}):
        ts = frappe.new_doc('Timesheet')
        ts.employee = hassan_emp
        ts.company = COMPANY
        ts.append('time_logs', {
            'activity_type': 'Execution',
            'from_time': '2026-10-01 09:00:00',
            'to_time': '2026-10-01 17:00:00',
            'hrs': 8,
            'description': 'Supervising Orbis O1 Sedan and Orbis X1 SUV line setup'
        })
        ts.insert(ignore_permissions=True)
        ts.submit()
        print(f'Created & Submitted Timesheet for Manufacturing Manager ({hassan_emp})')

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 9. PROGRAMMATIC PERMISSION BOUNDARY TESTING (Section 39)
    # -------------------------------------------------------------------------
    print('\n====================================================================')
    print('   --- 9. PROGRAMMATIC PERMISSION BOUNDARY TEST RESULTS ---         ')
    print('====================================================================')

    test_matrix = [
        # (User Email, User Label, Test Type, DocType, PermType, Expected)
        ('forw8007+salesmanager@gmail.com', 'Ali Khan (Sales Mgr)', 'ALLOWED', 'Customer', 'create', True),
        ('forw8007+salesmanager@gmail.com', 'Ali Khan (Sales Mgr)', 'ALLOWED', 'Quotation', 'create', True),
        ('forw8007+salesmanager@gmail.com', 'Ali Khan (Sales Mgr)', 'ALLOWED', 'Sales Order', 'create', True),
        ('forw8007+salesmanager@gmail.com', 'Ali Khan (Sales Mgr)', 'DENIED', 'Work Order', 'create', False),
        ('forw8007+salesmanager@gmail.com', 'Ali Khan (Sales Mgr)', 'DENIED', 'Employee', 'create', False),
        ('forw8007+salesmanager@gmail.com', 'Ali Khan (Sales Mgr)', 'DENIED', 'Payment Entry', 'create', False),
        ('forw8007+salesmanager@gmail.com', 'Ali Khan (Sales Mgr)', 'DENIED', 'Delivery Note', 'create', False),

        ('forw8007+purchasemanager@gmail.com', 'Ahmed Raza (Purchase Mgr)', 'ALLOWED', 'Purchase Order', 'create', True),
        ('forw8007+purchasemanager@gmail.com', 'Ahmed Raza (Purchase Mgr)', 'ALLOWED', 'Supplier', 'create', True),
        ('forw8007+purchasemanager@gmail.com', 'Ahmed Raza (Purchase Mgr)', 'DENIED', 'Sales Order', 'create', False),
        ('forw8007+purchasemanager@gmail.com', 'Ahmed Raza (Purchase Mgr)', 'DENIED', 'Work Order', 'create', False),

        ('forw8007+stockmanager@gmail.com', 'Usman Ali (Stock Mgr)', 'ALLOWED', 'Stock Entry', 'create', True),
        ('forw8007+stockmanager@gmail.com', 'Usman Ali (Stock Mgr)', 'ALLOWED', 'Item', 'create', True),
        ('forw8007+stockmanager@gmail.com', 'Usman Ali (Stock Mgr)', 'DENIED', 'User', 'create', False),
        ('forw8007+stockmanager@gmail.com', 'Usman Ali (Stock Mgr)', 'DENIED', 'Employee', 'create', False),

        ('forw8007+manufacturingmanager@gmail.com', 'Hassan Malik (Mfg Mgr)', 'ALLOWED', 'Work Order', 'create', True),
        ('forw8007+manufacturingmanager@gmail.com', 'Hassan Malik (Mfg Mgr)', 'ALLOWED', 'BOM', 'create', True),
        ('forw8007+manufacturingmanager@gmail.com', 'Hassan Malik (Mfg Mgr)', 'DENIED', 'Employee', 'create', False),
        ('forw8007+manufacturingmanager@gmail.com', 'Hassan Malik (Mfg Mgr)', 'DENIED', 'User', 'create', False),

        ('forw8007+flooruser1@gmail.com', 'Hamza Ahmed (Shop Floor)', 'ALLOWED', 'Job Card', 'write', True),
        ('forw8007+flooruser1@gmail.com', 'Hamza Ahmed (Shop Floor)', 'DENIED', 'Work Order', 'create', False),
        ('forw8007+flooruser1@gmail.com', 'Hamza Ahmed (Shop Floor)', 'DENIED', 'BOM', 'write', False),

        ('forw8007+qualitymanager@gmail.com', 'Sara Ahmed (Quality Mgr)', 'ALLOWED', 'Quality Inspection', 'create', True),
        ('forw8007+qualitymanager@gmail.com', 'Sara Ahmed (Quality Mgr)', 'DENIED', 'Purchase Order', 'create', False),

        ('forw8007+deliverymanager@gmail.com', 'Usman Shah (Delivery Mgr)', 'ALLOWED', 'Delivery Note', 'create', True),
        ('forw8007+deliverymanager@gmail.com', 'Usman Shah (Delivery Mgr)', 'DENIED', 'Payment Entry', 'create', False),

        ('forw8007+accountsmanager@gmail.com', 'Ayesha Khan (Accounts Mgr)', 'ALLOWED', 'Sales Invoice', 'create', True),
        ('forw8007+accountsmanager@gmail.com', 'Ayesha Khan (Accounts Mgr)', 'ALLOWED', 'Payment Entry', 'create', True),
        ('forw8007+accountsmanager@gmail.com', 'Ayesha Khan (Accounts Mgr)', 'DENIED', 'Work Order', 'create', False),

        ('forw8007+hrmanager@gmail.com', 'Fatima Ali (HR Mgr)', 'ALLOWED', 'Employee', 'create', True),
        ('forw8007+hrmanager@gmail.com', 'Fatima Ali (HR Mgr)', 'DENIED', 'User', 'create', False),
        ('forw8007+hrmanager@gmail.com', 'Fatima Ali (HR Mgr)', 'DENIED', 'Role', 'create', False),
        ('forw8007+hrmanager@gmail.com', 'Fatima Ali (HR Mgr)', 'DENIED', 'System Settings', 'write', False)
    ]

    passed_count = 0
    total_count = len(test_matrix)

    for email, user_lbl, test_type, dt, ptype, expected in test_matrix:
        actual = frappe.has_permission(dt, ptype=ptype, user=email)
        status = 'PASS' if actual == expected else 'FAIL'
        if status == 'PASS':
            passed_count += 1
            print(f'[✓] {user_lbl:<28} | {test_type:<7} | {dt:<20} ({ptype}): {actual} == {expected} -> PASS')
        else:
            print(f'[✗] {user_lbl:<28} | {test_type:<7} | {dt:<20} ({ptype}): {actual} != {expected} -> FAIL')

    print(f'\nBoundary Test Score: {passed_count} / {total_count} ({passed_count/total_count*100:.1f}%)')
    print('====================================================================')
    print('--- Step 5 Finished Successfully! ---')
    return {
        'total': total_count,
        'passed': passed_count,
        'status': 'Complete'
    }
