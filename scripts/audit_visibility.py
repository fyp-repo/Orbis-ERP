"""Audit script v2: Check workspace visibility, sidebar items, and permissions for all 10 users."""
import json
import frappe
import frappe.boot

def run():
    frappe.set_user('Administrator')
    
    print('=' * 70)
    print('  AUDIT: ROLE-BASED WORKSPACE & SIDEBAR VISIBILITY FOR ALL USERS')
    print('=' * 70)
    
    # 1. Check workspace roles
    print('\n--- 1. Workspace Role Assignments ---')
    ocm_ws = frappe.get_all('Workspace', filters={'name': ['like', 'OCM%']}, 
                            fields=['name', 'title', 'module', 'public'], order_by='sequence_id')
    for w in ocm_ws:
        roles = frappe.get_all('Has Role', filters={'parent': w['name'], 'parenttype': 'Workspace'}, fields=['role'])
        role_names = [r['role'] for r in roles]
        print(f"  {w['name']:<25} -> Roles: {role_names}")
    
    # 2. Check Workspace Sidebar structure
    print('\n--- 2. Workspace Sidebar DocType Check ---')
    if frappe.db.exists('DocType', 'Workspace Sidebar'):
        sidebar_count = frappe.db.count('Workspace Sidebar')
        print(f'  Workspace Sidebar records: {sidebar_count}')
        # Get the fields of this doctype
        meta = frappe.get_meta('Workspace Sidebar')
        fields = [f.fieldname for f in meta.fields]
        print(f'  Fields: {fields}')
        items = frappe.get_all('Workspace Sidebar', fields=['name', 'title'], limit=20)
        for item in items:
            print(f'    {item}')
    else:
        print('  Workspace Sidebar DocType does NOT exist')
    
    # 3. Check what frappe.boot returns for each user
    print('\n--- 3. User Boot Session Data ---')
    users = [
        ('forw8007+salesmanager@gmail.com', 'Sales Manager'),
        ('forw8007+purchasemanager@gmail.com', 'Purchase Manager'),
        ('forw8007+stockmanager@gmail.com', 'Stock Manager'),
        ('forw8007+manufacturingmanager@gmail.com', 'Manufacturing Manager'),
        ('forw8007+flooruser1@gmail.com', 'Shop Floor User 1'),
        ('forw8007+flooruser2@gmail.com', 'Shop Floor User 2'),
        ('forw8007+qualitymanager@gmail.com', 'Quality Manager'),
        ('forw8007+deliverymanager@gmail.com', 'Delivery Manager'),
        ('forw8007+accountsmanager@gmail.com', 'Accounts Manager'),
        ('forw8007+hrmanager@gmail.com', 'HR Manager'),
    ]
    
    for email, label in users:
        frappe.set_user(email)
        user_roles = frappe.get_roles(email)
        boot = frappe.boot.get_bootinfo()
        
        # Get workspace pages
        ws_pages = boot.get('workspaces', {}).get('pages', [])
        ws_names = [w.get('name') for w in ws_pages] if ws_pages else []
        
        # Get sidebar items
        sidebar = boot.get('workspace_sidebar_item', {})
        sidebar_keys = list(sidebar.keys()) if sidebar else []
        
        print(f'\n  [{label}] {email}')
        print(f'    Roles: {[r for r in user_roles if r not in ["Guest", "All"]]}')
        print(f'    Workspaces visible ({len(ws_names)}): {ws_names}')
        print(f'    Sidebar keys ({len(sidebar_keys)}): {sidebar_keys}')
    
    # 4. Check Administrator sidebar structure
    print('\n--- 4. Administrator Sidebar Structure ---')
    frappe.set_user('Administrator')
    admin_boot = frappe.boot.get_bootinfo()
    admin_sidebar = admin_boot.get('workspace_sidebar_item', {})
    print(f'  Total sidebar categories: {len(admin_sidebar)}')
    for key in sorted(admin_sidebar.keys()):
        items = admin_sidebar[key]
        if isinstance(items, list):
            ws_titles = [i.get('title', i.get('name', '?')) for i in items if isinstance(i, dict)]
            print(f'    {key:<30} -> {len(items)} items: {ws_titles[:5]}')
        elif isinstance(items, dict):
            sub_keys = list(items.keys())
            print(f'    {key:<30} -> dict keys: {sub_keys[:5]}')
        else:
            print(f'    {key:<30} -> {type(items).__name__}: {str(items)[:100]}')
    
    # 5. Raw sample of one sidebar entry
    print('\n--- 5. Raw sidebar sample ---')
    first_key = list(admin_sidebar.keys())[0] if admin_sidebar else None
    if first_key:
        val = admin_sidebar[first_key]
        print(f'  Key: {first_key}')
        print(f'  Type: {type(val).__name__}')
        sample = json.dumps(val, default=str)
        print(f'  Value: {sample[:800]}')
    
    # 6. User roles detail
    print('\n--- 6. All User Roles ---')
    for email, label in users:
        roles = frappe.get_all('Has Role', filters={'parent': email, 'parenttype': 'User'}, fields=['role'])
        role_names = sorted([r['role'] for r in roles])
        print(f'  {label:<22} -> {role_names}')
    
    frappe.set_user('Administrator')
    print('\n' + '=' * 70)
    print('  AUDIT COMPLETE')
    print('=' * 70)
