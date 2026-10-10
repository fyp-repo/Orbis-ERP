"""
Step 11: Fix Role-Based Department Module Visibility and Access Control
=======================================================================
This script fixes the sidebar visibility issue for all 10 users.

Root cause: The ocm_boot_session in boot.py was filtering sidebar keys using 
non-existent category names like 'ocm production', 'ocm human resources'. 
The actual Frappe sidebar categories are lowercase versions of Workspace Sidebar
record titles (e.g. 'selling', 'buying', 'manufacturing', 'stock', etc.).

Fix approach:
1. Update the ocm_boot_session role_map to use ACTUAL sidebar category keys 
   that exist in Frappe's 49 built-in sidebar categories.
2. Create custom Workspace Sidebar records for roles that have no matching 
   built-in sidebar (Shop Floor User, HR Manager, Delivery Manager).
3. Ensure Workspace DocType permissions (Has Role) are correct.
4. Add missing 'human resources' sidebar category if it doesn't exist.
5. Validate all 10 users see both workspaces AND sidebar items.
"""
import os
import json
import frappe
import frappe.boot

COMPANY = 'Orbis Car Manufacturing (Pvt.) Ltd.'
ABBR = 'OCM'

def create_missing_workspace_sidebars():
    """Create Workspace Sidebar records for categories that don't exist natively."""
    print('\n--- 1. Creating Missing Workspace Sidebar Records ---')
    
    # Check existing sidebar records
    existing = frappe.get_all('Workspace Sidebar', fields=['name', 'title'])
    existing_titles = {s['title'].lower() for s in existing}
    existing_names = {s['name'] for s in existing}
    print(f'  Existing sidebar records ({len(existing)}): {sorted(existing_titles)}')
    
    # We need sidebar categories for modules that the OCM workspaces use
    # The sidebar key is the lowercase version of the Workspace Sidebar title
    
    # Check what modules generate sidebar entries by examining workspaces
    # OCM Sales -> Selling module -> 'selling' sidebar (exists ✓)
    # OCM Purchasing -> Buying module -> 'buying' sidebar (exists ✓)  
    # OCM Inventory -> Stock module -> 'stock' sidebar (exists ✓)
    # OCM Manufacturing -> Manufacturing module -> 'manufacturing' sidebar (exists ✓)
    # OCM Production -> Manufacturing module -> 'manufacturing' sidebar (exists but shared with Mfg Manager)
    # OCM Quality -> Quality Management module -> 'quality management' sidebar (exists ✓)
    # OCM Delivery -> Selling module -> 'selling' sidebar (exists but shared with Sales)
    # OCM Accounts -> Accounts module -> 'accounts' sidebar (exists ✓)
    # OCM Human Resources -> Setup module -> 'setup' sidebar (exists but wrong)
    
    # The core issue: sidebars are module-level, not workspace-level.
    # Shop Floor and HR don't have unique sidebar categories because their 
    # workspaces map to modules that other workspaces already use.
    
    # Solution: Instead of trying to create new sidebar categories (which won't
    # be populated by Frappe's native get_sidebar_items), we need to fix the
    # boot.py filter to pass through the CORRECT existing sidebar categories
    # for each role, and also handle the OCM workspace page display.
    
    # For HR Manager: The OCM Human Resources workspace uses module 'Setup'.
    # HR-specific sidebar category doesn't exist in standard Frappe/ERPNext.
    # But 'setup' sidebar IS populated. HR Manager should see 'setup' sidebar
    # items (filtered to only HR-relevant items).
    
    # Actually, the better approach is: since Frappe v16 sidebar items are 
    # generated from Workspace Sidebar records which are keyed by module,
    # we should change OCM Human Resources module to something that generates
    # a sidebar. But creating custom sidebar records is fragile.
    
    # BEST FIX: Accept the existing sidebar structure and simply ensure the
    # boot.py filter maps each role to its REAL sidebar categories.
    
    print('  No new sidebar records needed - will fix boot.py filter mapping instead.')


def fix_boot_py_role_map():
    """Fix the ocm_boot_session function in boot.py to use correct sidebar keys."""
    print('\n--- 2. Fixing boot.py ocm_boot_session Role Map ---')
    
    boot_file = '/home/frappe/frappe-bench/apps/erpnext/erpnext/startup/boot.py'
    
    with open(boot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the entire ocm_boot_session function
    old_func_start = 'def ocm_boot_session(bootinfo):'
    if old_func_start not in content:
        print('  ERROR: ocm_boot_session not found in boot.py!')
        return
    
    # Split content at the function definition
    parts = content.split(old_func_start)
    before_func = parts[0]
    
    # The new ocm_boot_session function with correct sidebar mapping
    new_function = '''def ocm_boot_session(bootinfo):
\t"""Enforce OCM branding, logo, and role-based workspace/sidebar isolation."""
\t# --- OCM Branding ---
\tbootinfo.sysdefaults["app_name"] = "OCM | OrbisERP"
\tif "navbar_settings" in bootinfo:
\t\tbootinfo.navbar_settings.app_logo = "/files/ocm_logo.png"

\tfor app in bootinfo.get("app_data", []):
\t\tapp["app_title"] = "OCM"
\t\tapp["app_logo_url"] = "/files/ocm_logo.png"

\tfor icon in bootinfo.get("desktop_icons", []):
\t\tif icon.get("parent_icon") in ["ERPNext", "erpnext", None, ""]:
\t\t\ticon["parent_icon"] = "OCM"
\t\tif icon.get("label") == "ERPNext":
\t\t\ticon["label"] = "OCM"
\t\ticon["logo_url"] = "/files/ocm_logo.png"

\tfor k, v in bootinfo.get("workspace_sidebar_item", {}).items():
\t\tif isinstance(v, dict):
\t\t\tv["app"] = "OCM"
\t\t\tv["header_icon"] = "/files/ocm_logo.png"

\t# --- Role-Based Workspace & Sidebar Isolation ---
\tuser = frappe.session.user
\tif not user or user in ["Guest", "Administrator"] or "System Manager" in frappe.get_roles(user):
\t\treturn

\tuser_roles = set(frappe.get_roles(user))

\t# Map each departmental role to:
\t#   workspaces: list of OCM workspace names the role can see
\t#   sidebars: list of ACTUAL Frappe sidebar category keys (lowercase) 
\t#             that exist in workspace_sidebar_item
\t#
\t# These sidebar keys come from Workspace Sidebar DocType records and are
\t# populated by Frappe based on the workspace's 'module' field.
\t# The 49 built-in categories include: selling, buying, stock, manufacturing,
\t# quality, quality management, accounts, payments, invoicing, financial reports,
\t# crm, setup, organization, home, etc.
\trole_map = {
\t\t"Sales Manager": {
\t\t\t"workspaces": ["OCM Sales"],
\t\t\t"sidebars": ["selling", "crm"]
\t\t},
\t\t"Purchase Manager": {
\t\t\t"workspaces": ["OCM Purchasing"],
\t\t\t"sidebars": ["buying"]
\t\t},
\t\t"Stock Manager": {
\t\t\t"workspaces": ["OCM Inventory"],
\t\t\t"sidebars": ["stock"]
\t\t},
\t\t"Manufacturing Manager": {
\t\t\t"workspaces": ["OCM Manufacturing"],
\t\t\t"sidebars": ["manufacturing"]
\t\t},
\t\t"Shop Floor User": {
\t\t\t"workspaces": ["OCM Production"],
\t\t\t"sidebars": ["manufacturing"]
\t\t},
\t\t"Quality Manager": {
\t\t\t"workspaces": ["OCM Quality"],
\t\t\t"sidebars": ["quality", "quality management"]
\t\t},
\t\t"Delivery Manager": {
\t\t\t"workspaces": ["OCM Delivery"],
\t\t\t"sidebars": ["selling"]
\t\t},
\t\t"Accounts Manager": {
\t\t\t"workspaces": ["OCM Accounts"],
\t\t\t"sidebars": ["accounts", "invoicing", "payments", "financial reports"]
\t\t},
\t\t"HR Manager": {
\t\t\t"workspaces": ["OCM Human Resources"],
\t\t\t"sidebars": ["setup", "organization"]
\t\t}
\t}

\tallowed_ws = set()
\tallowed_sb = set()
\tfor r, conf in role_map.items():
\t\tif r in user_roles:
\t\t\tallowed_ws.update(conf["workspaces"])
\t\t\tallowed_sb.update(conf["sidebars"])

\tif not allowed_ws:
\t\treturn

\t# Filter workspace pages to only show allowed OCM workspaces
\tif "workspaces" in bootinfo and "pages" in bootinfo["workspaces"]:
\t\tbootinfo["workspaces"]["pages"] = [
\t\t\tw for w in bootinfo["workspaces"]["pages"]
\t\t\tif w.get("name") in allowed_ws
\t\t]

\t# Filter sidebar categories to only show allowed ones
\tif "workspace_sidebar_item" in bootinfo:
\t\tbootinfo["workspace_sidebar_item"] = {
\t\t\tk: v for k, v in bootinfo["workspace_sidebar_item"].items()
\t\t\tif k in allowed_sb
\t\t}

\t# Filter desktop icons
\tif "desktop_icons" in bootinfo:
\t\tbootinfo["desktop_icons"] = [
\t\t\ticon for icon in bootinfo["desktop_icons"]
\t\t\tif icon.get("label") in allowed_ws or icon.get("label", "").lower() in allowed_sb
\t\t]
'''
    
    # Write the new boot.py
    new_content = before_func + new_function
    
    with open(boot_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print('  Updated ocm_boot_session with correct sidebar category mappings.')
    print('  Key changes:')
    print('    - Shop Floor User: now maps to "manufacturing" sidebar (real category)')
    print('    - HR Manager: now maps to "setup" + "organization" sidebars (real categories)')
    print('    - Removed non-existent sidebar keys like "ocm production", "ocm human resources"')
    print('    - All sidebar keys now match actual Workspace Sidebar record titles')


def ensure_correct_workspace_roles():
    """Verify and fix workspace role assignments."""
    print('\n--- 3. Verifying Workspace Role Assignments ---')
    
    expected_roles = {
        'OCM Sales': ['Sales Manager', 'System Manager', 'Administrator'],
        'OCM Purchasing': ['Purchase Manager', 'System Manager', 'Administrator'],
        'OCM Inventory': ['Stock Manager', 'System Manager', 'Administrator'],
        'OCM Manufacturing': ['Manufacturing Manager', 'System Manager', 'Administrator'],
        'OCM Production': ['Shop Floor User', 'System Manager', 'Administrator'],
        'OCM Quality': ['Quality Manager', 'System Manager', 'Administrator'],
        'OCM Delivery': ['Delivery Manager', 'System Manager', 'Administrator'],
        'OCM Accounts': ['Accounts Manager', 'System Manager', 'Administrator'],
        'OCM Human Resources': ['HR Manager', 'System Manager', 'Administrator'],
    }
    
    for ws_name, roles in expected_roles.items():
        if not frappe.db.exists('Workspace', ws_name):
            print(f'  WARNING: Workspace {ws_name} does not exist!')
            continue
        
        w = frappe.get_doc('Workspace', ws_name)
        current_roles = {r.role for r in w.roles}
        expected_set = set(roles)
        
        if current_roles != expected_set:
            w.set('roles', [])
            for r in roles:
                w.append('roles', {'role': r})
            w.save(ignore_permissions=True)
            print(f'  FIXED {ws_name}: {current_roles} -> {expected_set}')
        else:
            print(f'  OK    {ws_name}: {current_roles}')
    
    frappe.db.commit()


def ensure_user_roles():
    """Ensure all 10 users have exactly the correct roles."""
    print('\n--- 4. Verifying User Role Assignments ---')
    
    user_role_map = {
        'forw8007+salesmanager@gmail.com': ['Sales Manager', 'Desk User'],
        'forw8007+purchasemanager@gmail.com': ['Purchase Manager', 'Desk User'],
        'forw8007+stockmanager@gmail.com': ['Stock Manager', 'Desk User'],
        'forw8007+manufacturingmanager@gmail.com': ['Manufacturing Manager', 'Desk User'],
        'forw8007+flooruser1@gmail.com': ['Shop Floor User', 'Desk User'],
        'forw8007+flooruser2@gmail.com': ['Shop Floor User', 'Desk User'],
        'forw8007+qualitymanager@gmail.com': ['Quality Manager', 'Desk User'],
        'forw8007+deliverymanager@gmail.com': ['Delivery Manager', 'Desk User'],
        'forw8007+accountsmanager@gmail.com': ['Accounts Manager', 'Desk User'],
        'forw8007+hrmanager@gmail.com': ['HR Manager', 'Desk User'],
    }
    
    for email, expected_roles in user_role_map.items():
        if not frappe.db.exists('User', email):
            print(f'  WARNING: User {email} does not exist!')
            continue
        
        u = frappe.get_doc('User', email)
        current_roles = {r.role for r in u.roles}
        expected_set = set(expected_roles)
        
        if current_roles != expected_set:
            u.set('roles', [])
            for r in expected_roles:
                u.append('roles', {'role': r})
            u.save(ignore_permissions=True)
            frappe.clear_cache(user=email)
            print(f'  FIXED {email}: {current_roles} -> {expected_set}')
        else:
            print(f'  OK    {email}: {current_roles}')
    
    frappe.db.commit()


def validate_all_users():
    """Validate workspace and sidebar visibility for all 10 users."""
    print('\n' + '=' * 70)
    print('  VALIDATION: WORKSPACE & SIDEBAR VISIBILITY FOR ALL 10 USERS')
    print('=' * 70)
    
    users = [
        ('forw8007+salesmanager@gmail.com', 'Sales Manager', ['OCM Sales'], ['selling', 'crm']),
        ('forw8007+purchasemanager@gmail.com', 'Purchase Manager', ['OCM Purchasing'], ['buying']),
        ('forw8007+stockmanager@gmail.com', 'Stock Manager', ['OCM Inventory'], ['stock']),
        ('forw8007+manufacturingmanager@gmail.com', 'Manufacturing Manager', ['OCM Manufacturing'], ['manufacturing']),
        ('forw8007+flooruser1@gmail.com', 'Shop Floor User 1', ['OCM Production'], ['manufacturing']),
        ('forw8007+flooruser2@gmail.com', 'Shop Floor User 2', ['OCM Production'], ['manufacturing']),
        ('forw8007+qualitymanager@gmail.com', 'Quality Manager', ['OCM Quality'], ['quality', 'quality management']),
        ('forw8007+deliverymanager@gmail.com', 'Delivery Manager', ['OCM Delivery'], ['selling']),
        ('forw8007+accountsmanager@gmail.com', 'Accounts Manager', ['OCM Accounts'], ['accounts', 'invoicing', 'payments', 'financial reports']),
        ('forw8007+hrmanager@gmail.com', 'HR Manager', ['OCM Human Resources'], ['setup', 'organization']),
    ]
    
    all_passed = True
    
    for email, label, expected_ws, expected_sidebar in users:
        frappe.set_user(email)
        boot = frappe.boot.get_bootinfo()
        
        # Check workspaces
        ws_pages = boot.get('workspaces', {}).get('pages', [])
        ws_names = [w.get('name') for w in ws_pages] if ws_pages else []
        ws_ok = set(ws_names) == set(expected_ws)
        
        # Check sidebar
        sidebar = boot.get('workspace_sidebar_item', {})
        sidebar_keys = sorted(sidebar.keys()) if sidebar else []
        sb_ok = set(sidebar_keys) == set(expected_sidebar)
        
        # Overall status
        ok = ws_ok and sb_ok
        if not ok:
            all_passed = False
        
        icon = '✓' if ok else '✗'
        status = 'PASS' if ok else 'FAIL'
        print(f'\n  [{icon}] {label:<22} -> {status}')
        print(f'       Workspaces: {ws_names} (expected: {expected_ws}) -> {"OK" if ws_ok else "FAIL"}')
        print(f'       Sidebar:    {sidebar_keys} (expected: {sorted(expected_sidebar)}) -> {"OK" if sb_ok else "FAIL"}')
    
    # Check Administrator
    frappe.set_user('Administrator')
    admin_boot = frappe.boot.get_bootinfo()
    admin_ws = admin_boot.get('workspaces', {}).get('pages', [])
    admin_sidebar = admin_boot.get('workspace_sidebar_item', {})
    admin_ws_count = len(admin_ws)
    admin_sb_count = len(admin_sidebar)
    print(f'\n  [✓] Administrator -> Workspaces: {admin_ws_count}, Sidebar categories: {admin_sb_count}')
    
    return all_passed


def validate_permissions_matrix():
    """Validate DocType permissions for all 10 users."""
    print('\n' + '=' * 70)
    print('  VALIDATION: DOCTYPE PERMISSIONS MATRIX')
    print('=' * 70)
    
    test_matrix = [
        ('forw8007+salesmanager@gmail.com', 'Sales Manager', 
         [('Customer', 'create'), ('Quotation', 'create'), ('Sales Order', 'create')],
         [('Quality Inspection', 'create'), ('Work Order', 'create'), ('Employee', 'read')]),
        
        ('forw8007+purchasemanager@gmail.com', 'Purchase Manager',
         [('Supplier', 'create'), ('Purchase Order', 'create')],
         [('Sales Order', 'create'), ('Work Order', 'create')]),
        
        ('forw8007+stockmanager@gmail.com', 'Stock Manager',
         [('Stock Entry', 'create'), ('Item', 'read')],
         [('Sales Order', 'create'), ('Work Order', 'create')]),
        
        ('forw8007+manufacturingmanager@gmail.com', 'Manufacturing Manager',
         [('BOM', 'create'), ('Work Order', 'create')],
         [('Sales Order', 'create'), ('Purchase Order', 'create')]),
        
        ('forw8007+flooruser1@gmail.com', 'Shop Floor User 1',
         [('Job Card', 'read'), ('Work Order', 'read')],
         [('BOM', 'create'), ('Customer', 'read'), ('Sales Order', 'read')]),
        
        ('forw8007+qualitymanager@gmail.com', 'Quality Manager',
         [('Quality Inspection', 'create')],
         [('Sales Order', 'create'), ('Purchase Order', 'create')]),
        
        ('forw8007+deliverymanager@gmail.com', 'Delivery Manager',
         [('Delivery Note', 'create')],
         [('Work Order', 'create'), ('Purchase Order', 'read')]),
        
        ('forw8007+accountsmanager@gmail.com', 'Accounts Manager',
         [('Sales Invoice', 'create'), ('Payment Entry', 'create')],
         [('Work Order', 'create'), ('BOM', 'create')]),
        
        ('forw8007+hrmanager@gmail.com', 'HR Manager',
         [('Employee', 'create'), ('Department', 'read')],
         [('Work Order', 'read'), ('Sales Order', 'read'), ('Purchase Order', 'read')]),
    ]
    
    total_pass = 0
    total_tests = 0
    
    for email, label, allowed, denied in test_matrix:
        frappe.set_user(email)
        
        allowed_ok = True
        for dt, ptype in allowed:
            has = frappe.has_permission(dt, ptype=ptype, user=email)
            total_tests += 1
            if has:
                total_pass += 1
            else:
                allowed_ok = False
                print(f'  [✗] {label}: Should ALLOW {dt}.{ptype} but DENIED')
        
        denied_ok = True
        for dt, ptype in denied:
            has = frappe.has_permission(dt, ptype=ptype, user=email)
            total_tests += 1
            if not has:
                total_pass += 1
            else:
                denied_ok = False
                print(f'  [✗] {label}: Should DENY {dt}.{ptype} but ALLOWED')
        
        status = 'PASS' if (allowed_ok and denied_ok) else 'FAIL'
        icon = '✓' if (allowed_ok and denied_ok) else '✗'
        print(f'  [{icon}] {label:<22} -> {status}')
    
    frappe.set_user('Administrator')
    pct = (total_pass / total_tests * 100) if total_tests else 0
    print(f'\n  Permissions Score: {total_pass}/{total_tests} ({pct:.1f}%)')
    
    return total_pass == total_tests


def run():
    frappe.set_user('Administrator')
    print('=' * 70)
    print('  STEP 11: FIX ROLE-BASED VISIBILITY & ACCESS CONTROL')
    print('=' * 70)
    
    # 1. Check/create sidebar records
    create_missing_workspace_sidebars()
    
    # 2. Fix boot.py role map
    fix_boot_py_role_map()
    
    # 3. Verify workspace roles
    ensure_correct_workspace_roles()
    
    # 4. Verify user roles
    ensure_user_roles()
    
    # 5. Clear all caches
    print('\n--- 5. Clearing All Caches ---')
    frappe.clear_cache()
    frappe.db.commit()
    print('  All caches cleared.')
    
    # 6. Validate visibility
    visibility_ok = validate_all_users()
    
    # 7. Validate permissions
    permissions_ok = validate_permissions_matrix()
    
    print('\n' + '=' * 70)
    if visibility_ok and permissions_ok:
        print('  ✓ ALL TESTS PASSED - ROLE-BASED ACCESS CONTROL IS COMPLETE')
    else:
        print('  ✗ SOME TESTS FAILED - SEE DETAILS ABOVE')
    print('=' * 70)
    
    return {
        'visibility_ok': visibility_ok,
        'permissions_ok': permissions_ok
    }

if __name__ == '__main__':
    run()
