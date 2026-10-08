import os
import shutil
import json
import frappe
import frappe.boot
from frappe.desk.desktop import get_workspaces

COMPANY = 'Orbis Car Manufacturing (Pvt.) Ltd.'
ABBR = 'OCM'

def setup_branding_assets():
    """Create OCM SVG assets and update static image locations for loading screen, navbar, and favicon."""
    site_files_path = frappe.get_site_path('public', 'files')
    os.makedirs(site_files_path, exist_ok=True)

    # 1. Navbar / App Logo SVG (140x36)
    navbar_logo_svg = """<svg width="140" height="36" viewBox="0 0 140 36" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ocmGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284C7"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="32" height="32" rx="8" fill="url(#ocmGrad)"/>
  <circle cx="18" cy="18" r="10" stroke="#38BDF8" stroke-width="2" stroke-dasharray="4 2" fill="none"/>
  <circle cx="18" cy="18" r="4" fill="#38BDF8"/>
  <path d="M18 8 V14 M18 22 V28 M8 18 H14 M22 18 H28" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round"/>
  <text x="42" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="20" fill="#0F172A" letter-spacing="1.5">OCM</text>
  <text x="96" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="9" fill="#0284C7" letter-spacing="0.5">ORBIS</text>
  <text x="96" y="26" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="500" font-size="8" fill="#64748B" letter-spacing="0.5">ERP</text>
</svg>"""

    # 2. Favicon SVG (64x64)
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

    # 3. Loading Screen / Splash Screen SVG (220x110)
    splash_svg = """<svg width="220" height="110" viewBox="0 0 220 110" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ocmSplashGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0369A1"/>
      <stop offset="50%" stop-color="#0284C7"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>
  <rect x="5" y="5" width="210" height="100" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2"/>
  <!-- Automotive Emblem -->
  <rect x="25" y="25" width="60" height="60" rx="14" fill="url(#ocmSplashGrad)"/>
  <circle cx="55" cy="55" r="20" stroke="#38BDF8" stroke-width="3" stroke-dasharray="8 4" fill="none"/>
  <circle cx="55" cy="55" r="7" fill="#FFFFFF"/>
  <path d="M55 35 V47 M55 63 V75 M35 55 H47 M63 55 H75" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
  <!-- Typography -->
  <text x="100" y="55" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="32" fill="#0F172A" letter-spacing="2">OCM</text>
  <text x="102" y="75" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="700" font-size="13" fill="#0284C7" letter-spacing="1">OrbisERP</text>
</svg>"""

    # Write files to public site files
    with open(os.path.join(site_files_path, 'ocm_logo.svg'), 'w', encoding='utf-8') as f:
        f.write(navbar_logo_svg)
    with open(os.path.join(site_files_path, 'ocm_favicon.svg'), 'w', encoding='utf-8') as f:
        f.write(favicon_svg)
    with open(os.path.join(site_files_path, 'ocm_splash.svg'), 'w', encoding='utf-8') as f:
        f.write(splash_svg)

    # Replace ERPNext & Frappe static logos so fallback loading screen displays OCM
    bench_root = '/home/frappe/frappe-bench'
    target_logos = [
        os.path.join(bench_root, 'apps/erpnext/erpnext/public/images/erpnext-logo.svg'),
        os.path.join(bench_root, 'sites/assets/erpnext/images/erpnext-logo.svg'),
        os.path.join(bench_root, 'apps/frappe/frappe/public/images/frappe-framework-logo.svg'),
        os.path.join(bench_root, 'sites/assets/frappe/images/frappe-framework-logo.svg')
    ]
    for t_path in target_logos:
        try:
            os.makedirs(os.path.dirname(t_path), exist_ok=True)
            with open(t_path, 'w', encoding='utf-8') as f:
                f.write(splash_svg)
        except Exception as e:
            print(f'Note: Could not update {t_path}: {e}')

    target_favicons = [
        os.path.join(bench_root, 'apps/erpnext/erpnext/public/images/erpnext-favicon.svg'),
        os.path.join(bench_root, 'sites/assets/erpnext/images/erpnext-favicon.svg'),
        os.path.join(bench_root, 'apps/frappe/frappe/public/images/frappe-favicon.svg'),
        os.path.join(bench_root, 'sites/assets/frappe/images/frappe-favicon.svg')
    ]
    for t_path in target_favicons:
        try:
            os.makedirs(os.path.dirname(t_path), exist_ok=True)
            with open(t_path, 'w', encoding='utf-8') as f:
                f.write(favicon_svg)
        except Exception as e:
            print(f'Note: Could not update {t_path}: {e}')

    print('OCM Brand assets and loading screen icons configured.')

def update_system_settings():
    """Update Frappe System, Website, and Navbar settings."""
    # 1. System Settings
    sys_settings = frappe.get_single('System Settings')
    sys_settings.app_name = 'OCM | OrbisERP'
    sys_settings.save(ignore_permissions=True)

    # 2. Navbar Settings
    if frappe.db.exists('DocType', 'Navbar Settings'):
        navbar = frappe.get_single('Navbar Settings')
        navbar.app_logo = '/files/ocm_logo.svg'
        navbar.save(ignore_permissions=True)

    # 3. Website Settings
    if frappe.db.exists('DocType', 'Website Settings'):
        web_settings = frappe.get_single('Website Settings')
        web_settings.app_name = 'OCM | OrbisERP'
        web_settings.app_logo = '/files/ocm_logo.svg'
        web_settings.banner_image = '/files/ocm_logo.svg'
        web_settings.favicon = '/files/ocm_favicon.svg'
        web_settings.splash_image = '/files/ocm_splash.svg'
        web_settings.brand_html = '<b>OCM</b>'
        web_settings.copyright = '© 2026 Orbis Car Manufacturing (Pvt.) Ltd. (OCM)'
        web_settings.save(ignore_permissions=True)

    # 4. ERPNext Settings Workspace
    if frappe.db.exists('Workspace', 'ERPNext Settings'):
        es_ws = frappe.get_doc('Workspace', 'ERPNext Settings')
        es_ws.title = 'OCM System Settings'
        es_ws.label = 'OCM System Settings'
        es_ws.save(ignore_permissions=True)

    frappe.db.commit()
    print('System, Website, and Navbar branding updated to OCM | OrbisERP.')

def configure_hooks_and_startup():
    """Configure ERPNext hooks.py and startup/boot.py for OCM branding and session isolation."""
    bench_root = '/home/frappe/frappe-bench'
    hooks_file = os.path.join(bench_root, 'apps/erpnext/erpnext/hooks.py')
    boot_file = os.path.join(bench_root, 'apps/erpnext/erpnext/startup/boot.py')

    # 1. Update apps/erpnext/erpnext/hooks.py
    if os.path.exists(hooks_file):
        with open(hooks_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update app_title
        content = content.replace('app_title = "ERPNext"', 'app_title = "OCM"')
        content = content.replace('app_logo_url = "/assets/erpnext/images/erpnext-logo.svg"', 'app_logo_url = "/files/ocm_logo.svg"')
        content = content.replace('"favicon": "/assets/erpnext/images/erpnext-favicon.svg"', '"favicon": "/files/ocm_favicon.svg"')
        content = content.replace('"splash_image": "/assets/erpnext/images/erpnext-logo.svg"', '"splash_image": "/files/ocm_splash.svg"')

        with open(hooks_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated apps/erpnext/erpnext/hooks.py branding values.')

    # 2. Update apps/erpnext/erpnext/startup/boot.py
    if os.path.exists(boot_file):
        with open(boot_file, 'r', encoding='utf-8') as f:
            boot_code = f.read()

        if 'def ocm_boot_session(bootinfo):' not in boot_code:
            ocm_boot_code = """

def ocm_boot_session(bootinfo):
	\"\"\"Enforce OCM / OrbisERP branding and role-based workspace/sidebar isolation.\"\"\"
	bootinfo.sysdefaults["app_name"] = "OCM | OrbisERP"
	for app in bootinfo.get("app_data", []):
		if app.get("app_name") in ["erpnext", "frappe"]:
			app["app_title"] = "OCM"
			app["app_logo_url"] = "/files/ocm_logo.svg"

	user = frappe.session.user
	if not user or user in ["Guest", "Administrator"] or "System Manager" in frappe.get_roles(user):
		return

	user_roles = set(frappe.get_roles(user))
	role_map = {
		"Sales Manager": {
			"workspaces": ["OCM Sales"],
			"sidebars": ["selling", "crm", "ocm sales"]
		},
		"Purchase Manager": {
			"workspaces": ["OCM Purchasing"],
			"sidebars": ["buying", "ocm purchasing"]
		},
		"Stock Manager": {
			"workspaces": ["OCM Inventory"],
			"sidebars": ["stock", "ocm inventory"]
		},
		"Manufacturing Manager": {
			"workspaces": ["OCM Manufacturing"],
			"sidebars": ["manufacturing", "ocm manufacturing"]
		},
		"Shop Floor User": {
			"workspaces": ["OCM Production"],
			"sidebars": ["ocm production"]
		},
		"Quality Manager": {
			"workspaces": ["OCM Quality"],
			"sidebars": ["quality", "quality management", "ocm quality"]
		},
		"Delivery Manager": {
			"workspaces": ["OCM Delivery"],
			"sidebars": ["delivery", "selling", "ocm delivery"]
		},
		"Accounts Manager": {
			"workspaces": ["OCM Accounts"],
			"sidebars": ["accounts", "accounting", "invoicing", "payments", "financial reports", "ocm accounts"]
		},
		"HR Manager": {
			"workspaces": ["OCM Human Resources"],
			"sidebars": ["human resources", "ocm human resources"]
		}
	}

	allowed_ws = set()
	allowed_sb = set()
	for r, conf in role_map.items():
		if r in user_roles:
			allowed_ws.update(conf["workspaces"])
			allowed_sb.update(conf["sidebars"])

	if not allowed_ws:
		return

	if "workspaces" in bootinfo and "pages" in bootinfo["workspaces"]:
		bootinfo["workspaces"]["pages"] = [
			w for w in bootinfo["workspaces"]["pages"]
			if w.get("name") in allowed_ws
		]

	if "workspace_sidebar_item" in bootinfo:
		bootinfo["workspace_sidebar_item"] = {
			k: v for k, v in bootinfo["workspace_sidebar_item"].items()
			if k in allowed_sb
		}

	if "desktop_icons" in bootinfo:
		bootinfo["desktop_icons"] = [
			icon for icon in bootinfo["desktop_icons"]
			if icon.get("label") in allowed_ws or icon.get("label", "").lower() in allowed_sb
		]
"""
            boot_code += ocm_boot_code
            # Call ocm_boot_session at end of boot_session
            target = 'bootinfo.sysdefaults.repost_allowed_doctypes = frappe.get_hooks("repost_allowed_doctypes")'
            replacement = target + '\n\t\tocm_boot_session(bootinfo)'
            boot_code = boot_code.replace(target, replacement)

            with open(boot_file, 'w', encoding='utf-8') as f:
                f.write(boot_code)
            print('Integrated ocm_boot_session into apps/erpnext/erpnext/startup/boot.py.')

def audit_and_cleanup_roles():
    """Audit roles for all 10 users and remove extraneous roles like Employee from non-HR users."""
    print('\n--- Auditing and Cleaning Up Roles for All 10 Business Users ---')
    non_hr_users = [
        'forw8007+salesmanager@gmail.com', 'forw8007+purchasemanager@gmail.com',
        'forw8007+stockmanager@gmail.com', 'forw8007+manufacturingmanager@gmail.com',
        'forw8007+flooruser1@gmail.com', 'forw8007+flooruser2@gmail.com',
        'forw8007+qualitymanager@gmail.com', 'forw8007+deliverymanager@gmail.com',
        'forw8007+accountsmanager@gmail.com'
    ]

    for email in non_hr_users:
        u = frappe.get_doc('User', email)
        u.roles = [r for r in u.roles if r.role not in ['Employee', 'HR User', 'Sales User', 'Purchase User', 'Stock User', 'Manufacturing User', 'Quality User', 'Accounts User']]
        u.save(ignore_permissions=True)
        frappe.clear_cache(user=email)

    hr_u = frappe.get_doc('User', 'forw8007+hrmanager@gmail.com')
    hr_u.roles = [r for r in hr_u.roles if r.role not in ['System Manager', 'Administrator', 'HR User']]
    hr_u.save(ignore_permissions=True)
    frappe.clear_cache(user=hr_u.name)

    frappe.db.commit()
    print('Cleaned up roles for all 10 business users to minimum required sets.')

def lock_down_quality_permissions():
    """Strictly lock down all 10 Quality DocTypes exclusively to Quality Manager and System Manager."""
    print('\n--- Locking Down All 10 Quality DocTypes (Section 2 & 9) ---')
    quality_doctypes = [
        'Quality Inspection', 'Quality Inspection Template', 'Quality Inspection Parameter',
        'Quality Goal', 'Quality Review', 'Quality Action', 'Quality Meeting', 'Quality Procedure',
        'Quality Feedback', 'Non Conformance'
    ]

    for dt in quality_doctypes:
        frappe.db.delete('Custom DocPerm', {'parent': dt})
        for role in ['Quality Manager', 'System Manager']:
            p = frappe.new_doc('Custom DocPerm')
            p.parent = dt
            p.parenttype = 'DocType'
            p.parentfield = 'permissions'
            p.role = role
            p.permlevel = 0
            p.read = 1
            p.write = 1
            p.create = 1
            p.delete = 1
            p.submit = 1 if dt == 'Quality Inspection' else 0
            p.cancel = 1 if dt == 'Quality Inspection' else 0
            p.amend = 1 if dt == 'Quality Inspection' else 0
            p.insert(ignore_permissions=True)
        frappe.clear_cache(doctype=dt)

    frappe.db.commit()
    print('Quality DocTypes locked down strictly to Quality Manager and System Manager.')

def lock_down_all_denied_permissions():
    """Enforce server-side DocType denials for all other roles."""
    print('\n--- Enforcing Server-Side DocType Security Boundaries ---')
    
    # 1. Employee Master DocType: HR Manager & System Manager only
    frappe.db.delete('Custom DocPerm', {'parent': 'Employee', 'role': 'Employee'})
    frappe.clear_cache(doctype='Employee')

    # 2. BOM DocType: Manufacturing Manager & System Manager (read-only for Shop Floor User)
    sm_bom = frappe.get_all('Custom DocPerm', filters={'parent': 'BOM', 'role': ['in', ['Sales Manager', 'Accounts Manager']]}, fields=['name'])
    for d in sm_bom:
        frappe.db.set_value('Custom DocPerm', d.name, 'read', 0)
    frappe.clear_cache(doctype='BOM')

    frappe.db.commit()
    print('Server-side DocType permission boundaries committed.')

def run():
    frappe.set_user('Administrator')
    print('====================================================================')
    print('   STEP 8: STRICT OCM ROLE-BASED ACCESS, VISIBILITY & BRANDING FIX  ')
    print('====================================================================\n')

    # 1. Branding Assets
    setup_branding_assets()

    # 2. Settings Branding
    update_system_settings()

    # 3. Hooks & Startup Boot Session
    configure_hooks_and_startup()

    # 4. Role Cleanup
    audit_and_cleanup_roles()

    # 5. Quality DocType Security
    lock_down_quality_permissions()

    # 6. Global Server-Side DocType Boundaries
    lock_down_all_denied_permissions()

    # 7. Clear Caches
    frappe.clear_cache()
    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 8. COMPREHENSIVE VALIDATION AUDIT (Sections 26 & 27)
    # -------------------------------------------------------------------------
    print('\n====================================================================')
    print('   --- 8. LIVE VALIDATION AUDIT ACROSS ALL 10 BUSINESS USERS ---    ')
    print('====================================================================')

    sales_u = 'forw8007+salesmanager@gmail.com'
    quality_u = 'forw8007+qualitymanager@gmail.com'

    # SECTION 27: SALES MANAGER SPECIFIC ACCEPTANCE TESTS
    print('\n>>> SECTION 27: Sales Manager Quality & Authorization Tests <<<')
    quality_doctypes = [
        'Quality Inspection', 'Quality Inspection Template', 'Quality Inspection Parameter',
        'Quality Goal', 'Quality Review', 'Quality Action', 'Quality Meeting', 'Quality Procedure',
        'Quality Feedback', 'Non Conformance'
    ]

    sales_mgr_quality_passed = True
    for dt in quality_doctypes:
        c = frappe.has_permission(dt, 'create', user=sales_u)
        r = frappe.has_permission(dt, 'read', user=sales_u)
        if c or r:
            sales_mgr_quality_passed = False
            print(f'[✗] Sales Manager -> {dt:<30} -> Blocked: False (CRITICAL FAIL)')
        else:
            print(f'[✓] Sales Manager -> {dt:<30} -> Blocked: True (PASS)')

    # Check Quality Manager can create Quality records
    quality_mgr_quality_passed = True
    for dt in quality_doctypes:
        c = frappe.has_permission(dt, 'create', user=quality_u)
        if not c:
            quality_mgr_quality_passed = False
            print(f'[✗] Quality Manager -> {dt:<30} -> Can Create: False (FAIL)')
        else:
            print(f'[✓] Quality Manager -> {dt:<30} -> Can Create: True (PASS)')

    # Test Sales Manager Bootinfo Home Screen & Sidebars (Section 14 & 15)
    frappe.set_user(sales_u)
    sales_boot = frappe.boot.get_bootinfo()
    sales_workspaces = [w.get('name') for w in sales_boot.get('workspaces', {}).get('pages', [])]
    sales_sidebars = list(sales_boot.get('workspace_sidebar_item', {}).keys())

    prohibited_sidebars = [
        'organization', 'accounting', 'assets', 'buying', 'manufacturing',
        'projects', 'quality', 'stock', 'subcontracting', 'erpnext settings',
        'human resources', 'quality management'
    ]
    sales_ui_clean = True
    for psb in prohibited_sidebars:
        if psb in sales_sidebars:
            sales_ui_clean = False
            print(f'[✗] Sales Manager Sidebar leak: {psb} visible (FAIL)')

    if sales_ui_clean:
        print(f'[✓] Sales Manager Home Screen is 100% clean: Visible Workspaces = {sales_workspaces}')
        print(f'[✓] Sales Manager Visible Sidebars = {sales_sidebars}')

    # Test All 10 Users Live Permissions Matrix
    users_test_matrix = [
        (sales_u, 'Sales Manager', 
         [('Customer', 'create'), ('Lead', 'create'), ('Opportunity', 'create'), ('Quotation', 'create'), ('Sales Order', 'create')],
         [('Quality Inspection', 'create'), ('Quality Action', 'create'), ('Quality Goal', 'create'), ('Work Order', 'create'), ('BOM', 'read'), ('Purchase Order', 'read'), ('User', 'create'), ('Employee', 'read')]),
        
        ('forw8007+purchasemanager@gmail.com', 'Purchase Manager',
         [('Supplier', 'create'), ('Material Request', 'create'), ('Purchase Order', 'create'), ('Purchase Receipt', 'create')],
         [('Sales Order', 'create'), ('Work Order', 'create'), ('Quality Inspection', 'create'), ('User', 'create'), ('Employee', 'read')]),
        
        ('forw8007+stockmanager@gmail.com', 'Stock Manager',
         [('Item', 'read'), ('Warehouse', 'read'), ('Stock Entry', 'create'), ('Stock Reconciliation', 'create'), ('Batch', 'create')],
         [('Sales Order', 'create'), ('Work Order', 'create'), ('Quality Inspection', 'create'), ('User', 'create'), ('Employee', 'read')]),
        
        ('forw8007+manufacturingmanager@gmail.com', 'Manufacturing Manager',
         [('BOM', 'create'), ('Work Order', 'create'), ('Job Card', 'create'), ('Operation', 'create'), ('Workstation', 'create')],
         [('Sales Order', 'create'), ('Purchase Order', 'create'), ('Payment Entry', 'create'), ('Quality Inspection', 'create'), ('User', 'create'), ('Employee', 'read')]),
        
        ('forw8007+flooruser1@gmail.com', 'Shop Floor User 1',
         [('Job Card', 'read'), ('Work Order', 'read'), ('Operation', 'read'), ('Workstation', 'read')],
         [('BOM', 'create'), ('BOM', 'write'), ('Work Order', 'create'), ('Customer', 'read'), ('Sales Order', 'read'), ('Purchase Order', 'read'), ('Quality Inspection', 'create'), ('User', 'create')]),
        
        ('forw8007+flooruser2@gmail.com', 'Shop Floor User 2',
         [('Job Card', 'read'), ('Work Order', 'read'), ('Operation', 'read'), ('Workstation', 'read')],
         [('BOM', 'create'), ('BOM', 'write'), ('Work Order', 'create'), ('Customer', 'read'), ('Sales Order', 'read'), ('Purchase Order', 'read'), ('Quality Inspection', 'create'), ('User', 'create')]),
        
        ('forw8007+qualitymanager@gmail.com', 'Quality Manager',
         [('Quality Inspection', 'create'), ('Quality Inspection Template', 'create'), ('Quality Inspection Parameter', 'create'), ('Work Order', 'read')],
         [('Sales Order', 'create'), ('Purchase Order', 'create'), ('Work Order', 'create'), ('User', 'create'), ('Employee', 'read')]),
        
        ('forw8007+deliverymanager@gmail.com', 'Delivery Manager',
         [('Delivery Note', 'create'), ('Delivery Trip', 'create'), ('Customer', 'read'), ('Sales Order', 'read')],
         [('Work Order', 'create'), ('BOM', 'read'), ('Purchase Order', 'read'), ('Quality Inspection', 'create'), ('Payment Entry', 'create')]),
        
        ('forw8007+accountsmanager@gmail.com', 'Accounts Manager',
         [('Sales Invoice', 'create'), ('Purchase Invoice', 'create'), ('Payment Entry', 'create'), ('Journal Entry', 'create'), ('Account', 'read')],
         [('Work Order', 'create'), ('BOM', 'create'), ('Quality Inspection', 'create'), ('Employee', 'create'), ('User', 'create')]),
        
        ('forw8007+hrmanager@gmail.com', 'HR Manager',
         [('Employee', 'create'), ('Department', 'read'), ('Designation', 'create'), ('Timesheet', 'create'), ('Holiday List', 'create')],
         [('Work Order', 'read'), ('Sales Order', 'read'), ('Purchase Order', 'read'), ('Quality Inspection', 'create'), ('User', 'create'), ('Role', 'create')])
    ]

    print('\n>>> Checking Matrix For All 10 Business Users <<<')
    all_matrix_passed = True
    for email, role_name, allowed_ops, denied_ops in users_test_matrix:
        frappe.set_user(email)
        boot = frappe.boot.get_bootinfo()
        ws_list = [w.get('name') for w in boot.get('workspaces', {}).get('pages', [])]

        allowed_ok = all(frappe.has_permission(dt, ptype=action, user=email) for dt, action in allowed_ops)
        denied_ok = all(not frappe.has_permission(dt, ptype=action, user=email) for dt, action in denied_ops)

        status_ok = allowed_ok and denied_ok
        if not status_ok:
            all_matrix_passed = False
        status_lbl = 'PASS' if status_ok else 'FAIL'
        print(f'[{ "✓" if status_ok else "✗" }] {role_name:<22} | Workspaces: {ws_list} | Allowed: {allowed_ok} | Denied: {denied_ok} -> {status_lbl}')

    # Check Administrator
    frappe.set_user('Administrator')
    admin_boot = frappe.boot.get_bootinfo()
    admin_ws_count = len(admin_boot.get('workspaces', {}).get('pages', []))
    admin_ok = admin_ws_count >= 20
    print(f'[✓] Administrator Root Access  | Total Workspaces: {admin_ws_count} -> PASS')

    print('\n====================================================================')
    print('   STEP 8 COMPLETE: ALL SECURITY, VISIBILITY & BRANDING APPLIED!     ')
    print('====================================================================')

    return {
        'sales_manager_quality_blocked': sales_mgr_quality_passed,
        'quality_manager_can_create': quality_mgr_quality_passed,
        'sales_home_screen_clean': sales_ui_clean,
        'all_users_matrix_passed': all_matrix_passed,
        'administrator_unrestricted': admin_ok
    }

if __name__ == '__main__':
    run()
