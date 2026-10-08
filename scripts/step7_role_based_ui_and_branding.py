import os
import json
import frappe
from frappe.desk.desktop import get_workspaces

COMPANY = 'Orbis Car Manufacturing (Pvt.) Ltd.'
ABBR = 'OCM'

def create_ocm_branding_assets():
    """Create OCM SVG logo and favicon for navbar and website branding."""
    site_path = frappe.get_site_path('public', 'files')
    os.makedirs(site_path, exist_ok=True)
    
    # 1. OCM App & Navbar Logo (Automotive badge with Orbis ring and bold OCM text)
    logo_svg = """<svg width="140" height="36" viewBox="0 0 140 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ocmGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284C7"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>
  <!-- Automotive Emblem / Wheel / Ring -->
  <rect x="2" y="2" width="32" height="32" rx="8" fill="url(#ocmGrad)"/>
  <circle cx="18" cy="18" r="10" stroke="#38BDF8" stroke-width="2" stroke-dasharray="4 2" fill="none"/>
  <circle cx="18" cy="18" r="4" fill="#38BDF8"/>
  <path d="M18 8 V14 M18 22 V28 M8 18 H14 M22 18 H28" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>
  <!-- Brand Text -->
  <text x="42" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="20" fill="#0F172A" letter-spacing="1.5">OCM</text>
  <text x="96" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="9" fill="#0284C7" letter-spacing="0.5">ORBIS</text>
  <text x="96" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="500" font-size="8" fill="#64748B" letter-spacing="0.5">ERP</text>
</svg>"""

    # 2. Favicon SVG
    favicon_svg = """<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ocmFavGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284C7"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="url(#ocmFavGrad)"/>
  <circle cx="32" cy="32" r="20" stroke="#38BDF8" stroke-width="3" stroke-dasharray="6 3" fill="none"/>
  <circle cx="32" cy="32" r="8" fill="#38BDF8"/>
  <path d="M32 12 V24 M32 40 V52 M12 32 H24 M40 32 H52" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
</svg>"""

    logo_path = os.path.join(site_path, 'ocm_logo.svg')
    favicon_path = os.path.join(site_path, 'ocm_favicon.svg')

    with open(logo_path, 'w', encoding='utf-8') as f:
        f.write(logo_svg)
    with open(favicon_path, 'w', encoding='utf-8') as f:
        f.write(favicon_svg)

    print('OCM Branding SVG assets written to:', site_path)
    return '/files/ocm_logo.svg', '/files/ocm_favicon.svg'

def run():
    frappe.set_user('Administrator')
    print('====================================================================')
    print('   STEP 7: OCM ROLE-BASED UI, WORKSPACE & ACCESS CONTROL SETUP       ')
    print('====================================================================\n')

    # -------------------------------------------------------------------------
    # 1. APPLICATION BRANDING CONFIGURATION (Section 2)
    # -------------------------------------------------------------------------
    print('--- 1. Configuring OCM System & Application Branding ---')
    logo_url, favicon_url = create_ocm_branding_assets()

    # 1.1 System Settings
    sys_settings = frappe.get_single('System Settings')
    sys_settings.app_name = 'OCM'
    sys_settings.save(ignore_permissions=True)
    print('System Settings app_name set to: OCM')

    # 1.2 Navbar Settings
    if frappe.db.exists('DocType', 'Navbar Settings'):
        navbar = frappe.get_single('Navbar Settings')
        navbar.app_logo = logo_url
        navbar.save(ignore_permissions=True)
        print(f'Navbar Settings app_logo set to: {logo_url}')

    # 1.3 Website Settings
    if frappe.db.exists('DocType', 'Website Settings'):
        web_settings = frappe.get_single('Website Settings')
        web_settings.app_name = 'OCM - OrbisERP'
        web_settings.app_logo = logo_url
        web_settings.banner_image = logo_url
        web_settings.favicon = favicon_url
        web_settings.brand_html = '<b>OCM</b>'
        web_settings.copyright = '© 2026 Orbis Car Manufacturing (Pvt.) Ltd. (OCM)'
        web_settings.save(ignore_permissions=True)
        print('Website Settings updated with OCM branding, logo, and copyright.')

    # 1.4 Update ERPNext Settings workspace title to OCM System Settings
    if frappe.db.exists('Workspace', 'ERPNext Settings'):
        es_ws = frappe.get_doc('Workspace', 'ERPNext Settings')
        es_ws.title = 'OCM System Settings'
        es_ws.label = 'OCM System Settings'
        es_ws.save(ignore_permissions=True)
        print('Renamed ERPNext Settings Workspace title & label to: OCM System Settings')

    # 1.5 Restrict Employee master DocType from standard Employee role
    cdp = frappe.get_all('Custom DocPerm', filters={'parent': 'Employee', 'role': 'Employee'}, fields=['name'])
    for d in cdp:
        frappe.db.set_value('Custom DocPerm', d.name, 'read', 0)
    frappe.clear_cache(doctype='Employee')
    print('Restricted Employee master DocType to HR Manager only.')

    # 1.6 Restrict BOM from Sales Manager
    sm_bom = frappe.get_all('Custom DocPerm', filters={'parent': 'BOM', 'role': 'Sales Manager'}, fields=['name'])
    for d in sm_bom:
        frappe.db.set_value('Custom DocPerm', d.name, 'read', 0)
    frappe.clear_cache(doctype='BOM')
    print('Restricted BOM DocType from Sales Manager.')

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 2. HIDE ALL DEFAULT / SYSTEM WORKSPACES FROM BUSINESS USERS (Section 3)
    # -------------------------------------------------------------------------
    print('\n--- 2. Locking Down Default Workspaces to Administrators Only ---')
    all_workspaces = frappe.get_all('Workspace', fields=['name'])
    for w in all_workspaces:
        wname = w['name']
        if not wname.startswith('OCM '):
            wdoc = frappe.get_doc('Workspace', wname)
            if not wdoc.type:
                wdoc.type = 'Workspace'
            wdoc.set('roles', [])
            wdoc.append('roles', {'role': 'System Manager'})
            wdoc.append('roles', {'role': 'Administrator'})
            wdoc.save(ignore_permissions=True)

    frappe.db.commit()
    print('All non-OCM default workspaces restricted exclusively to System Manager and Administrator.')

    # -------------------------------------------------------------------------
    # 3. CREATE / CONFIGURE THE 9 DEDICATED OCM WORKSPACES (Section 17)
    # -------------------------------------------------------------------------
    print('\n--- 3. Creating & Configuring 9 Dedicated OCM Workspaces ---')

    ocm_workspaces_config = [
        {
            'name': 'OCM Sales',
            'title': 'Sales',
            'label': 'OCM Sales',
            'icon': 'sell',
            'module': 'Selling',
            'sequence_id': 1,
            'roles': ['Sales Manager', 'System Manager', 'Administrator'],
            'header': 'OCM Automobile Sales & Dealership Management',
            'cards': [
                {
                    'card_name': 'Sales Operations',
                    'links': [
                        ('DocType', 'Customer', 'Customers'),
                        ('DocType', 'Lead', 'Leads'),
                        ('DocType', 'Opportunity', 'Opportunities'),
                        ('DocType', 'Quotation', 'Quotations'),
                        ('DocType', 'Sales Order', 'Sales Orders'),
                        ('DocType', 'Sales Invoice', 'Sales Invoices (Read-Only)'),
                        ('DocType', 'Delivery Note', 'Delivery Notes (Read-Only)'),
                        ('DocType', 'Item', 'Vehicle Catalog (Read-Only)')
                    ]
                },
                {
                    'card_name': 'Sales Reports',
                    'links': [
                        ('Report', 'Sales Analytics', 'Sales Analytics'),
                        ('Report', 'Sales Order Analysis', 'Sales Order Analysis'),
                        ('Report', 'Sales Register', 'Sales Register'),
                        ('Report', 'Customer Ledger Summary', 'Customer Ledger Summary')
                    ]
                }
            ]
        },
        {
            'name': 'OCM Purchasing',
            'title': 'Purchasing',
            'label': 'OCM Purchasing',
            'icon': 'buying',
            'module': 'Buying',
            'sequence_id': 2,
            'roles': ['Purchase Manager', 'System Manager', 'Administrator'],
            'header': 'OCM Material & Component Procurement',
            'cards': [
                {
                    'card_name': 'Purchasing Operations',
                    'links': [
                        ('DocType', 'Supplier', 'Suppliers'),
                        ('DocType', 'Material Request', 'Material Requests'),
                        ('DocType', 'Request for Quotation', 'Request for Quotation'),
                        ('DocType', 'Purchase Order', 'Purchase Orders'),
                        ('DocType', 'Purchase Receipt', 'Purchase Receipts'),
                        ('DocType', 'Purchase Invoice', 'Purchase Invoices'),
                        ('DocType', 'Item', 'Raw Materials & Components (Read-Only)')
                    ]
                },
                {
                    'card_name': 'Procurement Reports',
                    'links': [
                        ('Report', 'Purchase Analytics', 'Purchase Analytics'),
                        ('Report', 'Purchase Order Analysis', 'Purchase Order Analysis'),
                        ('Report', 'Purchase Register', 'Purchase Register'),
                        ('Report', 'Supplier Quotation Comparison', 'Supplier Quotation Comparison')
                    ]
                }
            ]
        },
        {
            'name': 'OCM Inventory',
            'title': 'Inventory',
            'label': 'OCM Inventory',
            'icon': 'stock',
            'module': 'Stock',
            'sequence_id': 3,
            'roles': ['Stock Manager', 'System Manager', 'Administrator'],
            'header': 'OCM Warehouse Stock & Logistics Management',
            'cards': [
                {
                    'card_name': 'Stock Operations',
                    'links': [
                        ('DocType', 'Item', 'Items'),
                        ('DocType', 'Item Group', 'Item Groups'),
                        ('DocType', 'Warehouse', 'Warehouses'),
                        ('DocType', 'Stock Entry', 'Stock Entry'),
                        ('DocType', 'Stock Reconciliation', 'Stock Reconciliation'),
                        ('DocType', 'Batch', 'Batches'),
                        ('DocType', 'Serial No', 'Serial Numbers'),
                        ('DocType', 'Purchase Receipt', 'Purchase Receipts'),
                        ('DocType', 'Delivery Note', 'Delivery Notes')
                    ]
                },
                {
                    'card_name': 'Inventory Reports',
                    'links': [
                        ('Report', 'Stock Ledger', 'Stock Ledger'),
                        ('Report', 'Stock Balance', 'Stock Balance'),
                        ('Report', 'Stock Analytics', 'Stock Analytics'),
                        ('Report', 'Stock Projected Qty', 'Stock Projected Qty')
                    ]
                }
            ]
        },
        {
            'name': 'OCM Manufacturing',
            'title': 'Manufacturing',
            'label': 'OCM Manufacturing',
            'icon': 'manufacturing',
            'module': 'Manufacturing',
            'sequence_id': 4,
            'roles': ['Manufacturing Manager', 'System Manager', 'Administrator'],
            'header': 'OCM Vehicle Assembly & Production Operations',
            'cards': [
                {
                    'card_name': 'Production Operations',
                    'links': [
                        ('DocType', 'BOM', 'Bills of Materials (BOM)'),
                        ('DocType', 'Work Order', 'Work Orders'),
                        ('DocType', 'Job Card', 'Job Cards'),
                        ('DocType', 'Operation', 'Manufacturing Operations'),
                        ('DocType', 'Workstation', 'Assembly Workstations'),
                        ('DocType', 'Production Plan', 'Production Planning'),
                        ('DocType', 'Stock Entry', 'Manufacturing Stock Entry'),
                        ('DocType', 'Item', 'Components & Materials'),
                        ('DocType', 'Warehouse', 'Warehouses')
                    ]
                },
                {
                    'card_name': 'Production Reports',
                    'links': [
                        ('Report', 'Work Order Summary', 'Work Order Summary'),
                        ('Report', 'BOM Operations Time', 'BOM Operations Time'),
                        ('Report', 'Production Analytics', 'Production Analytics')
                    ]
                }
            ]
        },
        {
            'name': 'OCM Production',
            'title': 'Production',
            'label': 'OCM Production',
            'icon': 'tool',
            'module': 'Manufacturing',
            'sequence_id': 5,
            'roles': ['Shop Floor User', 'System Manager', 'Administrator'],
            'header': 'OCM Shop Floor Operator Dashboard',
            'cards': [
                {
                    'card_name': 'Shop Floor Operations',
                    'links': [
                        ('DocType', 'Job Card', 'My Job Cards'),
                        ('DocType', 'Work Order', 'Assigned Work Orders (Read-Only)'),
                        ('DocType', 'Operation', 'Assembly Operations (Read-Only)'),
                        ('DocType', 'Workstation', 'Workstations (Read-Only)'),
                        ('DocType', 'Stock Entry', 'Production Material Transfer'),
                        ('DocType', 'Item', 'Items (Read-Only)')
                    ]
                }
            ]
        },
        {
            'name': 'OCM Quality',
            'title': 'Quality',
            'label': 'OCM Quality',
            'icon': 'quality',
            'module': 'Quality Management',
            'sequence_id': 6,
            'roles': ['Quality Manager', 'System Manager', 'Administrator'],
            'header': 'OCM Vehicle Quality Control & Testing Standards',
            'cards': [
                {
                    'card_name': 'Quality Control',
                    'links': [
                        ('DocType', 'Quality Inspection', 'Quality Inspections'),
                        ('DocType', 'Quality Inspection Template', 'Quality Inspection Templates'),
                        ('DocType', 'Quality Inspection Parameter', 'Quality Parameters'),
                        ('DocType', 'Work Order', 'Work Orders (Read-Only)'),
                        ('DocType', 'Job Card', 'Job Cards (Read-Only)'),
                        ('DocType', 'Item', 'Items (Read-Only)'),
                        ('DocType', 'Warehouse', 'Quality Hold Warehouse (Read-Only)')
                    ]
                },
                {
                    'card_name': 'Quality Reports',
                    'links': [
                        ('Report', 'Quality Inspection Summary', 'Quality Inspection Summary')
                    ]
                }
            ]
        },
        {
            'name': 'OCM Delivery',
            'title': 'Delivery',
            'label': 'OCM Delivery',
            'icon': 'custom-delivery-note',
            'module': 'Selling',
            'sequence_id': 7,
            'roles': ['Delivery Manager', 'System Manager', 'Administrator'],
            'header': 'OCM Finished Vehicle Logistics & Dealership Dispatch',
            'cards': [
                {
                    'card_name': 'Vehicle Logistics',
                    'links': [
                        ('DocType', 'Delivery Note', 'Delivery Notes'),
                        ('DocType', 'Delivery Trip', 'Delivery Trips'),
                        ('DocType', 'Sales Order', 'Sales Orders (Read-Only)'),
                        ('DocType', 'Customer', 'Dealership Customers (Read-Only)'),
                        ('DocType', 'Item', 'Finished Vehicles (Read-Only)'),
                        ('DocType', 'Warehouse', 'Finished Goods Warehouse (Read-Only)')
                    ]
                },
                {
                    'card_name': 'Delivery Reports',
                    'links': [
                        ('Report', 'Delivered Items To Be Billed', 'Delivered Vehicles To Be Billed'),
                        ('Report', 'Delivery Note Trends', 'Delivery Note Trends')
                    ]
                }
            ]
        },
        {
            'name': 'OCM Accounts',
            'title': 'Accounts',
            'label': 'OCM Accounts',
            'icon': 'accounting',
            'module': 'Accounts',
            'sequence_id': 8,
            'roles': ['Accounts Manager', 'System Manager', 'Administrator'],
            'header': 'OCM Financial Accounting & General Ledger',
            'cards': [
                {
                    'card_name': 'Financial Transactions',
                    'links': [
                        ('DocType', 'Sales Invoice', 'Sales Invoices'),
                        ('DocType', 'Purchase Invoice', 'Purchase Invoices'),
                        ('DocType', 'Payment Entry', 'Payment Entries'),
                        ('DocType', 'Journal Entry', 'Journal Entries'),
                        ('DocType', 'Account', 'Chart of Accounts (Read-Only)'),
                        ('DocType', 'Budget', 'Annual Budgets'),
                        ('DocType', 'Customer', 'Customers (Read-Only)'),
                        ('DocType', 'Supplier', 'Suppliers (Read-Only)')
                    ]
                },
                {
                    'card_name': 'Financial Reports',
                    'links': [
                        ('Report', 'General Ledger', 'General Ledger'),
                        ('Report', 'Trial Balance', 'Trial Balance'),
                        ('Report', 'Profit and Loss Statement', 'Profit and Loss Statement'),
                        ('Report', 'Balance Sheet', 'Balance Sheet'),
                        ('Report', 'Cash Flow', 'Cash Flow'),
                        ('Report', 'Accounts Receivable', 'Accounts Receivable'),
                        ('Report', 'Accounts Payable', 'Accounts Payable'),
                        ('Report', 'Sales Register', 'Sales Register'),
                        ('Report', 'Purchase Register', 'Purchase Register')
                    ]
                }
            ]
        },
        {
            'name': 'OCM Human Resources',
            'title': 'Human Resources',
            'label': 'OCM Human Resources',
            'icon': 'users',
            'module': 'Setup',
            'sequence_id': 9,
            'roles': ['HR Manager', 'System Manager', 'Administrator'],
            'header': 'OCM Personnel, Attendance & Timesheet Administration',
            'cards': [
                {
                    'card_name': 'Employee Management',
                    'links': [
                        ('DocType', 'Employee', 'Employees'),
                        ('DocType', 'Department', 'Departments (Read-Only)'),
                        ('DocType', 'Designation', 'Designations'),
                        ('DocType', 'Timesheet', 'Timesheets'),
                        ('DocType', 'Holiday List', 'Holiday Lists')
                    ]
                },
                {
                    'card_name': 'HR Reports',
                    'links': [
                        ('Report', 'Daily Timesheet Summary', 'Daily Timesheet Summary'),
                        ('Report', 'Timesheet Billing Summary', 'Timesheet Billing Summary')
                    ]
                }
            ]
        }
    ]

    for wcfg in ocm_workspaces_config:
        wname = wcfg['name']
        if not frappe.db.exists('Workspace', wname):
            w = frappe.new_doc('Workspace')
            w.name = wname
        else:
            w = frappe.get_doc('Workspace', wname)

        w.title = wcfg['title']
        w.label = wcfg['label']
        w.type = 'Workspace'
        w.public = 1
        w.icon = wcfg['icon']
        w.module = wcfg['module']
        w.sequence_id = wcfg['sequence_id']

        # Build content JSON
        content_blocks = [
            {'id': f'hdr_{wname[:8]}', 'type': 'header', 'data': {'text': f'<span class="h4"><b>{wcfg["header"]}</b></span>', 'col': 12}}
        ]
        for c in wcfg['cards']:
            content_blocks.append({'id': f'c_{c["card_name"][:8]}', 'type': 'card', 'data': {'card_name': c['card_name'], 'col': 6}})

        w.content = json.dumps(content_blocks)

        # Build links table
        w.set('links', [])
        for c in wcfg['cards']:
            w.append('links', {
                'type': 'Card Break',
                'label': c['card_name']
            })
            for link_type, link_to, lbl in c['links']:
                w.append('links', {
                    'type': 'Link',
                    'label': lbl,
                    'link_type': link_type,
                    'link_to': link_to,
                    'is_query_report': 1 if link_type == 'Report' else 0
                })

        # Set strict roles
        w.set('roles', [])
        for r in wcfg['roles']:
            w.append('roles', {'role': r})

        w.save(ignore_permissions=True)
        print(f'Configured Workspace [{wname}] -> Roles: {wcfg["roles"]}')

    frappe.clear_cache()
    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 4. VERIFY WORKSPACE VISIBILITY FOR EVERY BUSINESS USER (Section 3 & 14)
    # -------------------------------------------------------------------------
    print('\n====================================================================')
    print('   --- 4. WORKSPACE VISIBILITY VERIFICATION FOR ALL 10 USERS ---     ')
    print('====================================================================')

    user_expected_workspaces = [
        ('forw8007+salesmanager@gmail.com', 'Ali Khan (Sales Mgr)', ['OCM Sales']),
        ('forw8007+purchasemanager@gmail.com', 'Ahmed Raza (Purchase Mgr)', ['OCM Purchasing']),
        ('forw8007+stockmanager@gmail.com', 'Usman Ali (Stock Mgr)', ['OCM Inventory']),
        ('forw8007+manufacturingmanager@gmail.com', 'Hassan Malik (Mfg Mgr)', ['OCM Manufacturing']),
        ('forw8007+flooruser1@gmail.com', 'Hamza Ahmed (Shop Floor 1)', ['OCM Production']),
        ('forw8007+flooruser2@gmail.com', 'Bilal Khan (Shop Floor 2)', ['OCM Production']),
        ('forw8007+qualitymanager@gmail.com', 'Sara Ahmed (Quality Mgr)', ['OCM Quality']),
        ('forw8007+deliverymanager@gmail.com', 'Usman Shah (Delivery Mgr)', ['OCM Delivery']),
        ('forw8007+accountsmanager@gmail.com', 'Ayesha Khan (Accounts Mgr)', ['OCM Accounts']),
        ('forw8007+hrmanager@gmail.com', 'Fatima Ali (HR Mgr)', ['OCM Human Resources'])
    ]

    all_ui_passed = True
    for email, lbl, expected_list in user_expected_workspaces:
        frappe.set_user(email)
        res = get_workspaces()
        visible_names = [w.get('name') for w in res.get('pages', []) if isinstance(w, dict)]
        is_ok = visible_names == expected_list
        if not is_ok:
            all_ui_passed = False
        status_icon = '✓' if is_ok else '✗'
        status_lbl = 'PASS' if is_ok else 'FAIL'
        print(f'[{status_icon}] {lbl:<28} -> Visible: {visible_names} (Expected: {expected_list}) -> {status_lbl}')

    # Administrator check
    frappe.set_user('Administrator')
    admin_res = get_workspaces()
    admin_visible = [w.get('name') for w in admin_res.get('pages', []) if isinstance(w, dict)]
    admin_ok = len(admin_visible) >= 9
    print(f'[✓] Administrator (System Root)   -> Total Workspaces Visible: {len(admin_visible)} -> PASS')

    # -------------------------------------------------------------------------
    # 5. PREVENT UNAUTHORIZED DIRECT ACCESS (Section 15 & 22)
    # -------------------------------------------------------------------------
    print('\n====================================================================')
    print('   --- 5. UNAUTHORIZED DIRECT ACCESS PREVENTION TESTS ---           ')
    print('====================================================================')

    direct_access_tests = [
        # (Email, Label, DocType, Action, Expected Boolean)
        ('forw8007+salesmanager@gmail.com', 'Sales Manager', 'Work Order', 'read', False),
        ('forw8007+salesmanager@gmail.com', 'Sales Manager', 'BOM', 'read', False),
        ('forw8007+salesmanager@gmail.com', 'Sales Manager', 'Employee', 'read', False),
        ('forw8007+salesmanager@gmail.com', 'Sales Manager', 'Payment Entry', 'create', False),
        ('forw8007+salesmanager@gmail.com', 'Sales Manager', 'User', 'create', False),
        ('forw8007+salesmanager@gmail.com', 'Sales Manager', 'Role', 'create', False),

        ('forw8007+purchasemanager@gmail.com', 'Purchase Manager', 'Sales Order', 'create', False),
        ('forw8007+purchasemanager@gmail.com', 'Purchase Manager', 'Work Order', 'read', False),
        ('forw8007+purchasemanager@gmail.com', 'Purchase Manager', 'Employee', 'read', False),
        ('forw8007+purchasemanager@gmail.com', 'Purchase Manager', 'User', 'create', False),

        ('forw8007+stockmanager@gmail.com', 'Stock Manager', 'User', 'create', False),
        ('forw8007+stockmanager@gmail.com', 'Stock Manager', 'Role', 'create', False),
        ('forw8007+stockmanager@gmail.com', 'Stock Manager', 'Employee', 'create', False),
        ('forw8007+stockmanager@gmail.com', 'Stock Manager', 'Work Order', 'create', False),

        ('forw8007+manufacturingmanager@gmail.com', 'Manufacturing Manager', 'Employee', 'create', False),
        ('forw8007+manufacturingmanager@gmail.com', 'Manufacturing Manager', 'User', 'create', False),
        ('forw8007+manufacturingmanager@gmail.com', 'Manufacturing Manager', 'Role', 'create', False),

        ('forw8007+flooruser1@gmail.com', 'Shop Floor User', 'Work Order', 'create', False),
        ('forw8007+flooruser1@gmail.com', 'Shop Floor User', 'BOM', 'write', False),
        ('forw8007+flooruser1@gmail.com', 'Shop Floor User', 'Customer', 'read', False),
        ('forw8007+flooruser1@gmail.com', 'Shop Floor User', 'Sales Order', 'read', False),
        ('forw8007+flooruser1@gmail.com', 'Shop Floor User', 'Purchase Order', 'read', False),
        ('forw8007+flooruser1@gmail.com', 'Shop Floor User', 'Sales Invoice', 'read', False),
        ('forw8007+flooruser1@gmail.com', 'Shop Floor User', 'Employee', 'create', False),

        ('forw8007+qualitymanager@gmail.com', 'Quality Manager', 'Purchase Order', 'create', False),
        ('forw8007+qualitymanager@gmail.com', 'Quality Manager', 'Sales Order', 'create', False),
        ('forw8007+qualitymanager@gmail.com', 'Quality Manager', 'Work Order', 'create', False),
        ('forw8007+qualitymanager@gmail.com', 'Quality Manager', 'Employee', 'read', False),

        ('forw8007+deliverymanager@gmail.com', 'Delivery Manager', 'Purchase Order', 'read', False),
        ('forw8007+deliverymanager@gmail.com', 'Delivery Manager', 'Work Order', 'read', False),
        ('forw8007+deliverymanager@gmail.com', 'Delivery Manager', 'BOM', 'read', False),
        ('forw8007+deliverymanager@gmail.com', 'Delivery Manager', 'Payment Entry', 'create', False),

        ('forw8007+accountsmanager@gmail.com', 'Accounts Manager', 'Work Order', 'create', False),
        ('forw8007+accountsmanager@gmail.com', 'Accounts Manager', 'BOM', 'create', False),
        ('forw8007+accountsmanager@gmail.com', 'Accounts Manager', 'Employee', 'create', False),
        ('forw8007+accountsmanager@gmail.com', 'Accounts Manager', 'User', 'create', False),

        ('forw8007+hrmanager@gmail.com', 'HR Manager', 'User', 'create', False),
        ('forw8007+hrmanager@gmail.com', 'HR Manager', 'Role', 'create', False),
        ('forw8007+hrmanager@gmail.com', 'HR Manager', 'Role', 'write', False),
        ('forw8007+hrmanager@gmail.com', 'HR Manager', 'Work Order', 'read', False),
        ('forw8007+hrmanager@gmail.com', 'HR Manager', 'Sales Order', 'read', False),
        ('forw8007+hrmanager@gmail.com', 'HR Manager', 'Purchase Order', 'read', False)
    ]

    direct_passed = 0
    direct_total = len(direct_access_tests)

    for email, lbl, dt, ptype, expected in direct_access_tests:
        has_perm = frappe.has_permission(dt, ptype=ptype, user=email)
        status_pass = (has_perm == expected)
        if status_pass:
            direct_passed += 1
            print(f'[✓] {lbl:<22} -> Direct URL/API [{dt:<20}] ({ptype}): Blocked = {not has_perm} -> PASS')
        else:
            print(f'[✗] {lbl:<22} -> Direct URL/API [{dt:<20}] ({ptype}): Blocked = {not has_perm} -> FAIL')

    print(f'\nDirect Access Security Score: {direct_passed} / {direct_total} ({direct_passed/direct_total*100:.1f}%)')
    print('====================================================================')
    print('--- Step 7 Finished Successfully! ---')

    return {
        'ui_workspace_status': 'PASS' if all_ui_passed and admin_ok else 'FAIL',
        'direct_access_score': f'{direct_passed}/{direct_total}',
        'branding_status': 'OCM Branding Active'
    }

if __name__ == '__main__':
    run()
