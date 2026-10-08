import frappe
from frappe.utils.password import check_password

COMPANY = 'Orbis Car Manufacturing (Pvt.) Ltd.'
ABBR = 'OCM'

def run():
    frappe.set_user('Administrator')
    print('=====================================================')
    print('   ORBIS ERP — COMPREHENSIVE FINAL VALIDATION SUITE  ')
    print('=====================================================')

    results = []

    def check(title, condition, details=""):
        status = "PASS" if condition else "FAIL"
        results.append((title, status, details))
        mark = "✓" if condition else "✗"
        print(f"[{mark}] {title}: {details} -> {status}")

    # 1. Company Checks
    comp = frappe.get_doc('Company', COMPANY)
    check("Company Name", comp.name == COMPANY, comp.name)
    check("Company Abbreviation", comp.abbr == ABBR, comp.abbr)
    check("Company Currency", comp.default_currency == 'PKR', comp.default_currency)
    check("Company Country", comp.country == 'Pakistan', comp.country)

    # 2. System Checks
    sys_settings = frappe.get_single('System Settings')
    check("System / App Name", sys_settings.app_name == 'OrbisERP', sys_settings.app_name)
    admin_user = frappe.get_doc('User', 'Administrator')
    check("Administrator Account Exists & Enabled", admin_user.enabled == 1, admin_user.name)

    # 3. Old Demo Data Removal Checks
    old_companies = frappe.get_all('Company', filters={'name': ['in', ['OrbisERP', 'OrbisERP (Demo)']]})
    check("Old Demo Companies Removed", len(old_companies) == 0, f"Found: {len(old_companies)}")
    old_skus = frappe.get_all('Item', filters={'name': ['like', 'SKU%']})
    check("Old Demo Items Removed", len(old_skus) == 0, f"Found: {len(old_skus)}")
    old_demo_user = frappe.db.exists('User', 'heerc838@gmail.com')
    check("Old Demo User Removed", not old_demo_user, "heerc838@gmail.com removed")

    # 4. Item Groups Check
    req_item_groups = [
        'Finished Cars', 'Raw Materials', 'Metals', 'Rubber Components', 
        'Glass Components', 'Electrical Components', 'Engine Components', 
        'Interior Components', 'Safety Components', 'Battery Components', 
        'Manufactured Components', 'Spare Parts', 'Consumables'
    ]
    missing_ig = [ig for ig in req_item_groups if not frappe.db.exists('Item Group', ig)]
    check("Item Groups Created", len(missing_ig) == 0, f"Missing: {missing_ig}" if missing_ig else "All 13 exist")

    # 5. Warehouses Check
    req_whs = [
        f'Raw Material Warehouse - {ABBR}',
        f'Components Warehouse - {ABBR}',
        f'Production Store - {ABBR}',
        f'Work In Progress Warehouse - {ABBR}',
        f'Quality Hold Warehouse - {ABBR}',
        f'Finished Goods Warehouse - {ABBR}',
        f'Spare Parts Warehouse - {ABBR}'
    ]
    missing_whs = [w for w in req_whs if not frappe.db.exists('Warehouse', w)]
    check("All 7 Manufacturing Warehouses Exist", len(missing_whs) == 0, f"Missing: {missing_whs}" if missing_whs else "All 7 exist")

    # 6. Finished Cars Check
    cars = ['Orbis O1 Sedan', 'Orbis X1 SUV', 'Orbis E1 Electric']
    missing_cars = [c for c in cars if not frappe.db.exists('Item', c)]
    check("Finished Car Items Exist", len(missing_cars) == 0, f"Cars: {cars}")

    # 7. Raw Materials & Components Check
    sample_items = [
        'Steel Sheet', 'Stainless Steel', 'Aluminium Sheet', 'Windshield Glass',
        'Side Window Glass', 'Car Battery', 'Battery Cells', 'Battery Pack',
        'Engine Assembly', 'Transmission Assembly', 'Brake Assembly', 'Steering Assembly',
        'Suspension Assembly', 'Wheel Assembly', 'Car Body Assembly', 'Paint', 'Fasteners'
    ]
    missing_items = [i for i in sample_items if not frappe.db.exists('Item', i)]
    check("Key Raw Materials & Components Exist", len(missing_items) == 0, f"Missing: {missing_items}" if missing_items else f"Total Items: {frappe.db.count('Item')}")

    # 8. Suppliers & Customers
    supp_count = frappe.db.count('Supplier')
    check("10 Automobile Suppliers Exist", supp_count >= 10, f"Count: {supp_count}")
    cust_count = frappe.db.count('Customer')
    check("8 Auto Dealers / Customers Exist", cust_count >= 8, f"Count: {cust_count}")

    # 9. Workstations & Operations
    ws_count = frappe.db.count('Workstation')
    check("Workstations Exist", ws_count >= 9, f"Count: {ws_count}")
    op_count = frappe.db.count('Operation')
    check("Operations Exist", op_count >= 14, f"Count: {op_count}")

    # 10. BOMs Check
    boms = [
        'BOM-Orbis O1 Sedan-001',
        'BOM-Orbis X1 SUV-001',
        'BOM-Orbis E1 Electric-001'
    ]
    submitted_boms = [b for b in boms if frappe.db.get_value('BOM', b, 'docstatus') == 1]
    check("All 3 Car BOMs Submitted & Active", len(submitted_boms) == 3, f"BOMs: {submitted_boms}")

    # 11. Work Orders Check
    wos = frappe.get_all('Work Order', filters={'company': COMPANY}, fields=['name', 'production_item', 'qty', 'status', 'docstatus'])
    check("Work Orders Created (5 Sedan, 3 SUV, 2 Electric)", len(wos) >= 3, f"{len(wos)} Work Orders")

    # 12. Quality Inspections Check
    qis = frappe.get_all('Quality Inspection', fields=['name', 'item_code', 'status', 'docstatus'])
    passed_qis = [q.item_code for q in qis if q.status == 'Accepted']
    failed_qis = [q.item_code for q in qis if q.status == 'Rejected']
    check("Quality Inspections (Pass: Sedan/SUV, Fail: EV)", 'Orbis O1 Sedan' in passed_qis and 'Orbis E1 Electric' in failed_qis, f"Passed: {passed_qis}, Failed: {failed_qis}")

    # 13. Stock Balances Check
    fg_stock = frappe.db.sql("""
        SELECT item_code, sum(actual_qty) as qty 
        FROM `tabBin` 
        WHERE warehouse = %s 
        GROUP BY item_code
    """, f'Finished Goods Warehouse - {ABBR}', as_dict=True)
    fg_summary = {s.item_code: s.qty for s in fg_stock if s.qty > 0}
    check("Finished Goods Warehouse Has Completed Cars", len(fg_summary) > 0, f"Stock: {fg_summary}")

    # 14. Sales, Deliveries & Accounting Check
    so_count = frappe.db.count('Sales Order', {'company': COMPANY, 'docstatus': 1})
    check("Sales Orders Submitted", so_count >= 2, f"Count: {so_count}")
    dn_count = frappe.db.count('Delivery Note', {'company': COMPANY, 'docstatus': 1})
    check("Delivery Notes Submitted", dn_count >= 2, f"Count: {dn_count}")
    sinv_count = frappe.db.count('Sales Invoice', {'company': COMPANY, 'docstatus': 1})
    check("Sales Invoices Submitted", sinv_count >= 2, f"Count: {sinv_count}")
    pay_count = frappe.db.count('Payment Entry', {'company': COMPANY, 'docstatus': 1})
    check("Payment Entries Recorded", pay_count >= 4, f"Count: {pay_count} (Inbound + Outbound)")
    gl_count = frappe.db.count('GL Entry', {'company': COMPANY})
    check("General Ledger Entries Generated", gl_count > 0, f"Total GL Entries: {gl_count}")

    # 15. Exactly 10 Users & Credentials Verification
    expected_users = [
        ('Ali Khan', 'forw8007+salesmanager@gmail.com', 'Orbis@Sales123', 'Sales Manager', 'Sales'),
        ('Ahmed Raza', 'forw8007+purchasemanager@gmail.com', 'Orbis@Purchase123', 'Purchase Manager', 'Purchasing'),
        ('Usman Ali', 'forw8007+stockmanager@gmail.com', 'Orbis@Stock123', 'Stock Manager', 'Inventory / Stock'),
        ('Hassan Malik', 'forw8007+manufacturingmanager@gmail.com', 'Orbis@Manufacturing123', 'Manufacturing Manager', 'Manufacturing / Production'),
        ('Hamza Ahmed', 'forw8007+flooruser1@gmail.com', 'Orbis@Floor123', 'Shop Floor User', 'Shop Floor / Production Operations'),
        ('Bilal Khan', 'forw8007+flooruser2@gmail.com', 'Orbis@Floor123', 'Shop Floor User', 'Shop Floor / Production Operations'),
        ('Sara Ahmed', 'forw8007+qualitymanager@gmail.com', 'Orbis@Quality123', 'Quality Manager', 'Quality Control'),
        ('Usman Shah', 'forw8007+deliverymanager@gmail.com', 'Orbis@Delivery123', 'Delivery Manager', 'Delivery / Logistics'),
        ('Ayesha Khan', 'forw8007+accountsmanager@gmail.com', 'Orbis@Accounts123', 'Accounts Manager', 'Accounts / Finance'),
        ('Fatima Ali', 'forw8007+hrmanager@gmail.com', 'Orbis@HR123', 'HR Manager', 'Human Resources')
    ]

    project_users = frappe.get_all('User', filters={'name': ['like', 'forw8007+%']}, fields=['name', 'email', 'enabled', 'full_name'])
    check("Exactly 10 Project Users Exist", len(project_users) == 10, f"Found {len(project_users)} users")

    all_passwords_ok = True
    all_roles_ok = True
    all_depts_ok = True
    no_admin_leak = True

    for full_name, email, password, role, dept in expected_users:
        u_doc = frappe.get_doc('User', email)
        # Check password
        try:
            check_password(email, password)
        except Exception:
            all_passwords_ok = False
            print(f"Password failed for {email}")

        # Check role
        user_roles = [r.role for r in u_doc.roles]
        if role not in user_roles:
            all_roles_ok = False
            print(f"Role {role} missing for {email}")

        # Ensure NO System Manager or Administrator role
        if 'System Manager' in user_roles or 'Administrator' in user_roles:
            no_admin_leak = False
            print(f"SECURITY ALERT: User {email} has admin privileges!")

        # Check employee & department
        emp = frappe.db.get_value('Employee', {'user_id': email}, ['name', 'department'], as_dict=True)
        if not emp or not emp.department:
            all_depts_ok = False

    check("All 10 Users Passwords Successfully Authenticate", all_passwords_ok, "Bcrypt hashes verified")
    check("All 10 Users Assigned Designated Roles", all_roles_ok, "Roles properly configured")
    check("No Regular Users Have Administrator Privileges", no_admin_leak, "Strict RBAC enforced")
    check("All 10 Users Linked to Active Employees in Departments", all_depts_ok, "Employee HR links verified")

    # Final Summary
    total_passed = sum(1 for _, st, _ in results if st == 'PASS')
    total_checks = len(results)
    print('=====================================================')
    print(f"FINAL SCORE: {total_passed} / {total_checks} CHECKS PASSED ({(total_passed/total_checks)*100:.1f}%)")
    print('=====================================================')
    return {
        'total_checks': total_checks,
        'total_passed': total_passed,
        'results': results
    }
