import frappe
from frappe.utils.password import update_password

COMPANY = 'Orbis Car Manufacturing (Pvt.) Ltd.'
ABBR = 'OCM'

def run():
    frappe.set_user('Administrator')
    print('--- Step 1: Setting up Organization, Departments, Warehouses, Roles, Users ---')
    
    # 1. Update System & Global Settings
    frappe.db.set_default('company', COMPANY)
    frappe.db.set_default('default_company', COMPANY)
    frappe.db.set_single_value('Global Defaults', 'default_company', COMPANY)
    frappe.db.set_single_value('Global Defaults', 'default_currency', 'PKR')
    frappe.db.set_single_value('Global Defaults', 'country', 'Pakistan')
    
    # System Settings
    sys_settings = frappe.get_single('System Settings')
    sys_settings.app_name = 'OrbisERP'
    sys_settings.save(ignore_permissions=True)
    print('Updated System Settings & Global Defaults to OrbisERP')

    # 2. Departments
    dept_names = [
        'Sales',
        'Purchasing',
        'Inventory / Stock',
        'Manufacturing / Production',
        'Shop Floor / Production Operations',
        'Quality Control',
        'Delivery / Logistics',
        'Accounts / Finance',
        'Human Resources',
        'System Administration'
    ]
    for d in dept_names:
        if not frappe.db.exists('Department', {'department_name': d, 'company': COMPANY}):
            doc = frappe.new_doc('Department')
            doc.department_name = d
            doc.company = COMPANY
            doc.insert(ignore_permissions=True)
            print(f'Created Department: {d}')
        else:
            print(f'Department exists: {d}')

    # 3. Warehouses
    parent_wh = f'All Warehouses - {ABBR}'
    if not frappe.db.exists('Warehouse', parent_wh):
        p_doc = frappe.new_doc('Warehouse')
        p_doc.warehouse_name = 'All Warehouses'
        p_doc.company = COMPANY
        p_doc.is_group = 1
        p_doc.insert(ignore_permissions=True)
        parent_wh = p_doc.name

    wh_list = [
        ('Raw Material Warehouse', 'Stores raw materials: steel, aluminium, rubber, glass, paint, chemicals'),
        ('Components Warehouse', 'Stores engines, batteries, brakes, seats, electrical, steering, suspension'),
        ('Production Store', 'Stores materials ready to be issued to production'),
        ('Work In Progress Warehouse', 'Stores partially manufactured components/products'),
        ('Quality Hold Warehouse', 'Stores products awaiting quality inspection, failed products, rework'),
        ('Finished Goods Warehouse', 'Stores completed and quality-approved cars'),
        ('Spare Parts Warehouse', 'Stores replacement and service parts')
    ]
    for w_name, desc in wh_list:
        wh_full = f'{w_name} - {ABBR}'
        if not frappe.db.exists('Warehouse', wh_full):
            w = frappe.new_doc('Warehouse')
            w.warehouse_name = w_name
            w.company = COMPANY
            w.parent_warehouse = parent_wh
            w.is_group = 0
            w.insert(ignore_permissions=True)
            print(f'Created Warehouse: {w.name}')
        else:
            print(f'Warehouse exists: {wh_full}')

    # 4. Custom Roles if needed
    needed_roles = [
        'Sales Manager', 'Purchase Manager', 'Stock Manager', 
        'Manufacturing Manager', 'Shop Floor User', 'Quality Manager', 
        'Delivery Manager', 'Accounts Manager', 'HR Manager', 'System Manager'
    ]
    for r in needed_roles:
        if not frappe.db.exists('Role', r):
            role_doc = frappe.new_doc('Role')
            role_doc.role_name = r
            role_doc.desk_access = 1
            role_doc.insert(ignore_permissions=True)
            print(f'Created Role: {r}')

    # Role Permissions setup for specialized roles
    # Quality Manager permissions
    for dt in ['Quality Inspection', 'Quality Inspection Parameter', 'Quality Inspection Template']:
        if not frappe.db.exists('Custom DocPerm', {'parent': dt, 'role': 'Quality Manager'}):
            try:
                cdp = frappe.new_doc('Custom DocPerm')
                cdp.parent = dt
                cdp.parenttype = 'DocType'
                cdp.parentfield = 'permissions'
                cdp.role = 'Quality Manager'
                cdp.read = 1
                cdp.write = 1
                cdp.create = 1
                cdp.submit = 1
                cdp.cancel = 1
                cdp.insert(ignore_permissions=True)
            except Exception as e:
                print(f'DocPerm notice for {dt}: {e}')

    # Delivery Manager permissions
    for dt in ['Delivery Note', 'Delivery Trip']:
        if not frappe.db.exists('Custom DocPerm', {'parent': dt, 'role': 'Delivery Manager'}):
            try:
                cdp = frappe.new_doc('Custom DocPerm')
                cdp.parent = dt
                cdp.parenttype = 'DocType'
                cdp.parentfield = 'permissions'
                cdp.role = 'Delivery Manager'
                cdp.read = 1
                cdp.write = 1
                cdp.create = 1
                cdp.submit = 1
                cdp.cancel = 1
                cdp.insert(ignore_permissions=True)
            except Exception as e:
                print(f'DocPerm notice for {dt}: {e}')

    # Shop Floor User permissions
    for dt in ['Job Card', 'Work Order', 'Stock Entry']:
        if not frappe.db.exists('Custom DocPerm', {'parent': dt, 'role': 'Shop Floor User'}):
            try:
                cdp = frappe.new_doc('Custom DocPerm')
                cdp.parent = dt
                cdp.parenttype = 'DocType'
                cdp.parentfield = 'permissions'
                cdp.role = 'Shop Floor User'
                cdp.read = 1
                cdp.write = 1 if dt in ['Job Card', 'Stock Entry'] else 0
                cdp.create = 1 if dt in ['Job Card', 'Stock Entry'] else 0
                cdp.submit = 1 if dt in ['Job Card', 'Stock Entry'] else 0
                cdp.insert(ignore_permissions=True)
            except Exception as e:
                print(f'DocPerm notice for {dt}: {e}')

    # 5. Exactly 10 Users
    users_data = [
        {
            'email': 'forw8007+salesmanager@gmail.com',
            'first_name': 'Ali',
            'last_name': 'Khan',
            'password': 'Orbis@Sales123',
            'role': 'Sales Manager',
            'extra_roles': ['Sales User'],
            'dept': 'Sales'
        },
        {
            'email': 'forw8007+purchasemanager@gmail.com',
            'first_name': 'Ahmed',
            'last_name': 'Raza',
            'password': 'Orbis@Purchase123',
            'role': 'Purchase Manager',
            'extra_roles': ['Purchase User'],
            'dept': 'Purchasing'
        },
        {
            'email': 'forw8007+stockmanager@gmail.com',
            'first_name': 'Usman',
            'last_name': 'Ali',
            'password': 'Orbis@Stock123',
            'role': 'Stock Manager',
            'extra_roles': ['Stock User'],
            'dept': 'Inventory / Stock'
        },
        {
            'email': 'forw8007+manufacturingmanager@gmail.com',
            'first_name': 'Hassan',
            'last_name': 'Malik',
            'password': 'Orbis@Manufacturing123',
            'role': 'Manufacturing Manager',
            'extra_roles': ['Manufacturing User'],
            'dept': 'Manufacturing / Production'
        },
        {
            'email': 'forw8007+flooruser1@gmail.com',
            'first_name': 'Hamza',
            'last_name': 'Ahmed',
            'password': 'Orbis@Floor123',
            'role': 'Shop Floor User',
            'extra_roles': [],
            'dept': 'Shop Floor / Production Operations'
        },
        {
            'email': 'forw8007+flooruser2@gmail.com',
            'first_name': 'Bilal',
            'last_name': 'Khan',
            'password': 'Orbis@Floor123',
            'role': 'Shop Floor User',
            'extra_roles': [],
            'dept': 'Shop Floor / Production Operations'
        },
        {
            'email': 'forw8007+qualitymanager@gmail.com',
            'first_name': 'Sara',
            'last_name': 'Ahmed',
            'password': 'Orbis@Quality123',
            'role': 'Quality Manager',
            'extra_roles': ['Quality User'] if frappe.db.exists('Role', 'Quality User') else [],
            'dept': 'Quality Control'
        },
        {
            'email': 'forw8007+deliverymanager@gmail.com',
            'first_name': 'Usman',
            'last_name': 'Shah',
            'password': 'Orbis@Delivery123',
            'role': 'Delivery Manager',
            'extra_roles': ['Stock User'],
            'dept': 'Delivery / Logistics'
        },
        {
            'email': 'forw8007+accountsmanager@gmail.com',
            'first_name': 'Ayesha',
            'last_name': 'Khan',
            'password': 'Orbis@Accounts123',
            'role': 'Accounts Manager',
            'extra_roles': ['Accounts User'],
            'dept': 'Accounts / Finance'
        },
        {
            'email': 'forw8007+hrmanager@gmail.com',
            'first_name': 'Fatima',
            'last_name': 'Ali',
            'password': 'Orbis@HR123',
            'role': 'HR Manager',
            'extra_roles': ['HR User'],
            'dept': 'Human Resources'
        }
    ]

    for u in users_data:
        email = u['email']
        if not frappe.db.exists('User', email):
            user = frappe.new_doc('User')
            user.email = email
            user.first_name = u['first_name']
            user.last_name = u['last_name']
            user.enabled = 1
            user.send_welcome_email = 0
            user.insert(ignore_permissions=True)
            print(f'Created User: {email}')
        else:
            user = frappe.get_doc('User', email)
            user.enabled = 1
            user.first_name = u['first_name']
            user.last_name = u['last_name']
            print(f'User exists: {email}')

        # Set specific roles (desk user + target role, NO System Manager or Administrator)
        all_target_roles = ['Desk User', u['role']] + u['extra_roles']
        user.roles = []
        for r_name in all_target_roles:
            if frappe.db.exists('Role', r_name):
                user.append('roles', {'role': r_name})
        user.save(ignore_permissions=True)

        # Set password using official Frappe password updater
        update_password(email, u['password'])
        print(f'Configured password for {email}')

        # Set User Permission for Company
        if not frappe.db.exists('User Permission', {'user': email, 'allow': 'Company', 'for_value': COMPANY}):
            up = frappe.new_doc('User Permission')
            up.user = email
            up.allow = 'Company'
            up.for_value = COMPANY
            up.is_default = 1
            up.insert(ignore_permissions=True)

        # 6. Create Employee record for User
        full_name = f"{u['first_name']} {u['last_name']}"
        dept_name = frappe.db.get_value('Department', {'department_name': u['dept'], 'company': COMPANY}, 'name')
        
        # Check designation
        designation = u['role']
        if not frappe.db.exists('Designation', designation):
            des_doc = frappe.new_doc('Designation')
            des_doc.designation_name = designation
            des_doc.insert(ignore_permissions=True)

        if not frappe.db.exists('Employee', {'user_id': email}):
            emp = frappe.new_doc('Employee')
            emp.first_name = u['first_name']
            emp.last_name = u['last_name']
            emp.company = COMPANY
            emp.department = dept_name
            emp.designation = designation
            emp.user_id = email
            emp.status = 'Active'
            emp.gender = 'Female' if u['first_name'] in ['Sara', 'Ayesha', 'Fatima'] else 'Male'
            emp.date_of_birth = '1992-05-15'
            emp.date_of_joining = '2022-01-01'
            emp.insert(ignore_permissions=True)
            print(f'Created Employee: {full_name} ({emp.name})')
        else:
            emp_name = frappe.db.get_value('Employee', {'user_id': email}, 'name')
            emp = frappe.get_doc('Employee', emp_name)
            emp.department = dept_name
            emp.designation = designation
            emp.company = COMPANY
            emp.save(ignore_permissions=True)
            print(f'Updated Employee: {full_name}')

    frappe.db.commit()
    print('--- Step 1 Finished Successfully! ---')
    return 'Step 1 Complete'
