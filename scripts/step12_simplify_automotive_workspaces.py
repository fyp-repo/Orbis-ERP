"""
Step 12: Simplify ERP Interface & Configure Automotive-Focused Workspaces
========================================================================
Implements the automotive-focused OrbisERP workspace and role-based workspaces:
1. Creates custom automotive DocTypes:
   - Vehicle Model (if not already existing)
   - Finished Vehicle Register (VIN, chassis, model, inspection, delivery)
2. Seeds initial automotive vehicle models (Orbis O1 Sedan, Orbis X1 SUV, Orbis E1 Electric)
3. Creates the Primary Automotive Workspace:
   - "OrbisERP" (Automotive Manufacturing Workspace)
   - Navigation Items:
     * Manufacturing Dashboard
     * Vehicle Models
     * BOM and Components
     * Production Plans
     * Work Orders
     * Inventory and Warehouses
     * Procurement and Suppliers
     * Quality Inspection
     * Maintenance
     * Finished Vehicles
     * Essential Finance and Employee functions
4. Configures 5 Dedicated Role-Based Workspaces:
   - Production (Manufacturing Manager, Manufacturing User)
   - Inventory (Stock Manager, Stock User)
   - Procurement (Purchase Manager, Purchase User)
   - Quality (Quality Manager)
   - Management (System Manager, Administrator)
5. Hides irrelevant generic modules/workspaces without deleting any code or database records:
   - CRM, Support, Projects, Assets, Website, Integrations, Subcontracting, Invoicing, etc.
"""

import os
import json
import frappe

def create_automotive_doctypes():
    """Ensure Vehicle Model and Finished Vehicle Register DocTypes exist."""
    print("--- 1. Ensuring Custom Automotive DocTypes Exist ---")
    
    # 1.1 Vehicle Model
    if not frappe.db.exists('DocType', 'Vehicle Model'):
        vm = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'Vehicle Model',
            'module': 'Manufacturing',
            'custom': 1,
            'is_submittable': 0,
            'track_changes': 1,
            'fields': [
                {'fieldname': 'model_code', 'label': 'Model Code', 'fieldtype': 'Data', 'reqd': 1, 'unique': 1, 'in_list_view': 1},
                {'fieldname': 'model_name', 'label': 'Model Name', 'fieldtype': 'Data', 'reqd': 1, 'in_list_view': 1},
                {'fieldname': 'body_style', 'label': 'Body Style', 'fieldtype': 'Select', 'options': 'Sedan\nSUV\nHatchback\nElectric\nPickup', 'in_list_view': 1},
                {'fieldname': 'powertrain_type', 'label': 'Powertrain Type', 'fieldtype': 'Select', 'options': 'ICE (Petrol/Diesel)\nHybrid\nElectric (EV)', 'in_list_view': 1},
                {'fieldname': 'col_break_1', 'fieldtype': 'Column Break'},
                {'fieldname': 'model_year', 'label': 'Model Year', 'fieldtype': 'Int', 'default': 2026},
                {'fieldname': 'base_price', 'label': 'Base Price (PKR)', 'fieldtype': 'Currency'},
                {'fieldname': 'default_bom', 'label': 'Default BOM', 'fieldtype': 'Link', 'options': 'BOM'},
                {'fieldname': 'status', 'label': 'Status', 'fieldtype': 'Select', 'options': 'Active\nIn Development\nDiscontinued', 'default': 'Active', 'in_list_view': 1},
                {'fieldname': 'sec_desc', 'label': 'Specifications & Details', 'fieldtype': 'Section Break'},
                {'fieldname': 'specifications', 'label': 'Technical Specifications', 'fieldtype': 'Small Text'}
            ],
            'permissions': [
                {'role': 'System Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
                {'role': 'Manufacturing Manager', 'read': 1, 'write': 1, 'create': 1},
                {'role': 'Manufacturing User', 'read': 1},
                {'role': 'Stock Manager', 'read': 1},
                {'role': 'Purchase Manager', 'read': 1},
                {'role': 'Quality Manager', 'read': 1}
            ]
        })
        vm.insert(ignore_permissions=True)
        print("  Created DocType: Vehicle Model")
    else:
        print("  DocType Vehicle Model already exists.")

    # 1.2 Finished Vehicle Register
    if not frappe.db.exists('DocType', 'Finished Vehicle Register'):
        fvr = frappe.get_doc({
            'doctype': 'DocType',
            'name': 'Finished Vehicle Register',
            'module': 'Manufacturing',
            'custom': 1,
            'is_submittable': 0,
            'track_changes': 1,
            'fields': [
                {'fieldname': 'vin_number', 'label': 'VIN Number', 'fieldtype': 'Data', 'reqd': 1, 'unique': 1, 'in_list_view': 1},
                {'fieldname': 'chassis_number', 'label': 'Chassis Number', 'fieldtype': 'Data', 'reqd': 1, 'in_list_view': 1},
                {'fieldname': 'vehicle_model', 'label': 'Vehicle Model', 'fieldtype': 'Link', 'options': 'Vehicle Model', 'reqd': 1, 'in_list_view': 1},
                {'fieldname': 'color', 'label': 'Color', 'fieldtype': 'Data', 'in_list_view': 1},
                {'fieldname': 'col_break_1', 'fieldtype': 'Column Break'},
                {'fieldname': 'vehicle_status', 'label': 'Vehicle Status', 'fieldtype': 'Select', 
                 'options': 'In Production\nIn Quality Inspection\nQuality Hold\nReady for Dispatch\nDispatched\nDelivered', 
                 'default': 'In Production', 'in_list_view': 1},
                {'fieldname': 'production_completed_on', 'label': 'Production Date', 'fieldtype': 'Date'},
                {'fieldname': 'work_order', 'label': 'Work Order', 'fieldtype': 'Link', 'options': 'Work Order'},
                {'fieldname': 'warehouse', 'label': 'Current Warehouse', 'fieldtype': 'Link', 'options': 'Warehouse'},
                {'fieldname': 'sec_qc', 'label': 'Quality & Compliance', 'fieldtype': 'Section Break'},
                {'fieldname': 'inspection_status', 'label': 'Quality Inspection Status', 'fieldtype': 'Select', 
                 'options': 'Pending\nPassed\nFailed', 'default': 'Pending'},
                {'fieldname': 'quality_inspection', 'label': 'Quality Inspection Record', 'fieldtype': 'Link', 'options': 'Quality Inspection'},
                {'fieldname': 'inspection_notes', 'label': 'Inspection Notes', 'fieldtype': 'Small Text'},
                {'fieldname': 'sec_dispatch', 'label': 'Dispatch & Sales', 'fieldtype': 'Section Break'},
                {'fieldname': 'customer', 'label': 'Dealer / Customer', 'fieldtype': 'Link', 'options': 'Customer'},
                {'fieldname': 'delivery_note', 'label': 'Delivery Note', 'fieldtype': 'Link', 'options': 'Delivery Note'}
            ],
            'permissions': [
                {'role': 'System Manager', 'read': 1, 'write': 1, 'create': 1, 'delete': 1},
                {'role': 'Manufacturing Manager', 'read': 1, 'write': 1, 'create': 1},
                {'role': 'Manufacturing User', 'read': 1},
                {'role': 'Stock Manager', 'read': 1, 'write': 1},
                {'role': 'Quality Manager', 'read': 1, 'write': 1}
            ]
        })
        fvr.insert(ignore_permissions=True)
        print("  Created DocType: Finished Vehicle Register")
    else:
        print("  DocType Finished Vehicle Register already exists.")

    frappe.db.commit()


def seed_automotive_models():
    """Seed sample vehicle models if table is empty."""
    print("\n--- 2. Seeding Automotive Vehicle Models ---")
    models_data = [
        {
            'model_code': 'OCM-SED-01',
            'model_name': 'Orbis O1 Executive Sedan',
            'body_style': 'Sedan',
            'powertrain_type': 'ICE (Petrol/Diesel)',
            'model_year': 2026,
            'base_price': 6500000,
            'status': 'Active',
            'specifications': '1.5L Turbocharged Petrol, 6-Speed Automatic, 5-Seater Executive Sedan.'
        },
        {
            'model_code': 'OCM-SUV-01',
            'model_name': 'Orbis X1 AWD SUV',
            'body_style': 'SUV',
            'powertrain_type': 'Hybrid',
            'model_year': 2026,
            'base_price': 8900000,
            'status': 'Active',
            'specifications': '2.0L Hybrid AWD, Electronic Stability Control, 7-Seater Family SUV.'
        },
        {
            'model_code': 'OCM-EV-01',
            'model_name': 'Orbis E1 Electric Car',
            'body_style': 'Electric',
            'powertrain_type': 'Electric (EV)',
            'model_year': 2026,
            'base_price': 11200000,
            'status': 'In Development',
            'specifications': '75 kWh High-Capacity Lithium Battery, Dual Motor AWD, 520 km Range.'
        }
    ]
    for m in models_data:
        if not frappe.db.exists('Vehicle Model', {'model_code': m['model_code']}):
            doc = frappe.get_doc({'doctype': 'Vehicle Model', **m})
            doc.insert(ignore_permissions=True)
            print(f"  Inserted Vehicle Model: {m['model_name']} ({m['model_code']})")
        else:
            print(f"  Vehicle Model {m['model_code']} already exists.")
    frappe.db.commit()


def hide_irrelevant_workspaces():
    """Hide generic irrelevant workspaces from navigation without deleting code or data."""
    print("\n--- 3. Hiding Irrelevant Workspaces from Navigation ---")
    irrelevant_workspaces = [
        'CRM', 'Support', 'Projects', 'Assets', 'Website', 
        'Integrations', 'Subcontracting', 'Invoicing', 
        'Financial Reports', 'Users', 'Build', 'Welcome Workspace',
        'Stock', 'Buying', 'Selling', 'Manufacturing'
    ]
    
    for ws_name in irrelevant_workspaces:
        if frappe.db.exists('Workspace', ws_name):
            try:
                ws = frappe.get_doc('Workspace', ws_name)
                if not ws.type:
                    ws.type = 'Workspace'
                ws.is_hidden = 1
                ws.public = 0
                # Clear all roles and set to System Manager only so regular users cannot see it
                ws.set('roles', [])
                ws.append('roles', {'role': 'System Manager'})
                ws.save(ignore_permissions=True)
                print(f"  Hidden from navigation: {ws_name}")
            except Exception as e:
                print(f"  Error updating workspace {ws_name}: {e}")
    frappe.db.commit()


def setup_primary_automotive_workspace():
    """Create or update the primary automotive-focused OrbisERP workspace."""
    print("\n--- 4. Creating Primary Automotive OrbisERP Workspace ---")
    ws_name = "OrbisERP"
    
    cards = [
        {
            'card_name': 'Automotive Manufacturing & Assembly',
            'links': [
                ('DocType', 'Vehicle Model', 'Vehicle Models'),
                ('DocType', 'BOM', 'BOM (Bill of Materials)'),
                ('DocType', 'Item', 'Components & Automotive Parts'),
                ('DocType', 'Production Plan', 'Production Plans'),
                ('DocType', 'Work Order', 'Work Orders'),
                ('DocType', 'Job Card', 'Assembly Job Cards'),
                ('DocType', 'Workstation', 'Assembly Workstations'),
                ('DocType', 'Operation', 'Manufacturing Operations')
            ]
        },
        {
            'card_name': 'Finished Vehicles & Quality Control',
            'links': [
                ('DocType', 'Finished Vehicle Register', 'Finished Vehicles'),
                ('DocType', 'Serial No', 'Vehicle VINs & Serial Numbers'),
                ('DocType', 'Quality Inspection', 'Quality Inspection'),
                ('DocType', 'Quality Inspection Template', 'Inspection Templates (Body, Paint, Road Test)'),
                ('DocType', 'Non Conformance', 'Defect Tracking & Rework')
            ]
        },
        {
            'card_name': 'Inventory & Supply Chain',
            'links': [
                ('DocType', 'Warehouse', 'Warehouses (Parts, WIP, Finished Goods)'),
                ('DocType', 'Stock Entry', 'Inventory Transfers & Consumption'),
                ('DocType', 'Supplier', 'Suppliers & Parts Vendors'),
                ('DocType', 'Material Request', 'Procurement Material Requests'),
                ('DocType', 'Purchase Order', 'Purchase Orders'),
                ('DocType', 'Purchase Receipt', 'Parts Purchase Receipts')
            ]
        },
        {
            'card_name': 'Plant Maintenance & Enterprise Functions',
            'links': [
                ('DocType', 'Maintenance Visit', 'Maintenance Visits'),
                ('DocType', 'Maintenance Schedule', 'Equipment Maintenance Schedules'),
                ('DocType', 'Sales Invoice', 'Sales Invoices'),
                ('DocType', 'Purchase Invoice', 'Purchase Invoices'),
                ('DocType', 'Payment Entry', 'Payment Entries'),
                ('DocType', 'Employee', 'Employees & Workforce'),
                ('DocType', 'Timesheet', 'Production Timesheets')
            ]
        },
        {
            'card_name': 'Manufacturing Reports & Analytics',
            'links': [
                ('Report', 'Work Order Summary', 'Work Order Summary'),
                ('Report', 'Production Analytics', 'Production Analytics'),
                ('Report', 'Stock Ledger', 'Stock Ledger'),
                ('Report', 'Stock Balance', 'Stock Balance'),
                ('Report', 'General Ledger', 'General Ledger')
            ]
        }
    ]

    shortcuts = [
        {'label': 'Manufacturing Dashboard', 'type': 'Dashboard', 'link_to': 'Manufacturing'},
        {'label': 'Vehicle Models', 'type': 'DocType', 'link_to': 'Vehicle Model'},
        {'label': 'Production Plans', 'type': 'DocType', 'link_to': 'Production Plan'},
        {'label': 'Work Orders', 'type': 'DocType', 'link_to': 'Work Order'},
        {'label': 'Finished Vehicles', 'type': 'DocType', 'link_to': 'Finished Vehicle Register'},
        {'label': 'Quality Inspection', 'type': 'DocType', 'link_to': 'Quality Inspection'},
        {'label': 'Warehouses', 'type': 'DocType', 'link_to': 'Warehouse'},
        {'label': 'Suppliers', 'type': 'DocType', 'link_to': 'Supplier'}
    ]

    charts = [
        {'chart_name': 'Produced Quantity', 'label': 'Vehicles & Units Produced'},
        {'chart_name': 'Work Order Analysis', 'label': 'Work Order Status Analysis'}
    ]

    content_blocks = [
        {'id': 'hdr_orbis_main', 'type': 'header', 'data': {'text': '<span class="h4"><b>OrbisERP Automotive Manufacturing Hub</b></span>', 'col': 12}},
        {'id': 'sc_orbis_main', 'type': 'shortcut', 'data': {'shortcut_name': 'Vehicle Models', 'col': 3}},
        {'id': 'sc_orbis_wo', 'type': 'shortcut', 'data': {'shortcut_name': 'Work Orders', 'col': 3}},
        {'id': 'sc_orbis_fvr', 'type': 'shortcut', 'data': {'shortcut_name': 'Finished Vehicles', 'col': 3}},
        {'id': 'sc_orbis_qi', 'type': 'shortcut', 'data': {'shortcut_name': 'Quality Inspection', 'col': 3}},
        {'id': 'ch_produced', 'type': 'chart', 'data': {'chart_name': 'Produced Quantity', 'col': 12}}
    ]
    for c in cards:
        content_blocks.append({'id': f'c_{c["card_name"][:8]}', 'type': 'card', 'data': {'card_name': c['card_name'], 'col': 6}})

    if not frappe.db.exists('Workspace', ws_name):
        w = frappe.new_doc('Workspace')
        w.name = ws_name
    else:
        w = frappe.get_doc('Workspace', ws_name)

    w.title = "OrbisERP"
    w.label = "OrbisERP"
    w.type = "Workspace"
    w.public = 1
    w.is_hidden = 0
    w.icon = "car" if frappe.db.exists('Workspace', ws_name) else "manufacturing"
    w.module = "Manufacturing"
    w.sequence_id = 1
    w.content = json.dumps(content_blocks)

    # Build Links
    w.set('links', [])
    for c in cards:
        w.append('links', {'type': 'Card Break', 'label': c['card_name']})
        for link_type, link_to, lbl in c['links']:
            w.append('links', {
                'type': 'Link',
                'label': lbl,
                'link_type': link_type,
                'link_to': link_to,
                'is_query_report': 1 if link_type == 'Report' else 0
            })

    # Build Shortcuts
    w.set('shortcuts', [])
    for sc in shortcuts:
        w.append('shortcuts', {
            'label': sc['label'],
            'type': sc['type'],
            'link_to': sc['link_to']
        })

    # Build Charts
    w.set('charts', [])
    for ch in charts:
        if frappe.db.exists('Dashboard Chart', ch['chart_name']):
            w.append('charts', {
                'label': ch['label'],
                'chart_name': ch['chart_name']
            })

    # Available to all Desk Users
    w.set('roles', [])
    w.append('roles', {'role': 'Desk User'})
    w.append('roles', {'role': 'System Manager'})
    w.append('roles', {'role': 'Manufacturing Manager'})
    w.append('roles', {'role': 'Stock Manager'})
    w.append('roles', {'role': 'Purchase Manager'})
    w.append('roles', {'role': 'Quality Manager'})

    w.save(ignore_permissions=True)
    print("  Configured Primary Workspace: OrbisERP")
    frappe.db.commit()


def setup_role_based_workspaces():
    """Create dedicated role-based workspaces for Production, Inventory, Procurement, Quality, and Management."""
    print("\n--- 5. Configuring Role-Based Workspaces ---")

    role_workspaces = [
        {
            'name': 'Production',
            'title': 'Production',
            'label': 'Production',
            'icon': 'tool',
            'module': 'Manufacturing',
            'sequence_id': 2,
            'roles': ['Manufacturing Manager', 'Manufacturing User', 'System Manager'],
            'header': 'Automotive Production & Assembly Operations',
            'shortcuts': [
                {'label': 'Work Orders', 'type': 'DocType', 'link_to': 'Work Order'},
                {'label': 'Job Cards', 'type': 'DocType', 'link_to': 'Job Card'},
                {'label': 'Production Plans', 'type': 'DocType', 'link_to': 'Production Plan'},
                {'label': 'Vehicle Models', 'type': 'DocType', 'link_to': 'Vehicle Model'}
            ],
            'cards': [
                {
                    'card_name': 'Shop Floor Execution',
                    'links': [
                        ('DocType', 'Work Order', 'Work Orders'),
                        ('DocType', 'Job Card', 'Job Cards'),
                        ('DocType', 'Production Plan', 'Production Plans'),
                        ('DocType', 'Stock Entry', 'Material Issue & Completion'),
                        ('DocType', 'Vehicle Model', 'Vehicle Models (Catalog)')
                    ]
                },
                {
                    'card_name': 'Assembly Setup & Maintenance',
                    'links': [
                        ('DocType', 'BOM', 'Bills of Materials (BOM)'),
                        ('DocType', 'Workstation', 'Assembly Workstations'),
                        ('DocType', 'Operation', 'Production Operations'),
                        ('DocType', 'Maintenance Visit', 'Workstation Maintenance Visits'),
                        ('DocType', 'Maintenance Schedule', 'Preventive Maintenance Schedules')
                    ]
                },
                {
                    'card_name': 'Production Analytics',
                    'links': [
                        ('Report', 'Work Order Summary', 'Work Order Summary'),
                        ('Report', 'Production Analytics', 'Production Analytics'),
                        ('Report', 'BOM Operations Time', 'BOM Operations Time')
                    ]
                }
            ]
        },
        {
            'name': 'Inventory',
            'title': 'Inventory',
            'label': 'Inventory',
            'icon': 'stock',
            'module': 'Stock',
            'sequence_id': 3,
            'roles': ['Stock Manager', 'Stock User', 'System Manager'],
            'header': 'Automotive Components, Warehouses & Vehicle Stock',
            'shortcuts': [
                {'label': 'Warehouses', 'type': 'DocType', 'link_to': 'Warehouse'},
                {'label': 'Finished Vehicles', 'type': 'DocType', 'link_to': 'Finished Vehicle Register'},
                {'label': 'Stock Entry', 'type': 'DocType', 'link_to': 'Stock Entry'},
                {'label': 'Automotive Items', 'type': 'DocType', 'link_to': 'Item'}
            ],
            'cards': [
                {
                    'card_name': 'Component & Finished Vehicle Stock',
                    'links': [
                        ('DocType', 'Item', 'Automotive Items & Raw Materials'),
                        ('DocType', 'Finished Vehicle Register', 'Finished Vehicle Stock'),
                        ('DocType', 'Serial No', 'Vehicle VINs / Serial Numbers'),
                        ('DocType', 'Item Group', 'Item Groups (Engine, Tyres, Body, etc.)'),
                        ('DocType', 'Warehouse', 'Warehouses (Raw Material, WIP, Finished Cars)')
                    ]
                },
                {
                    'card_name': 'Stock Movements & Logistics',
                    'links': [
                        ('DocType', 'Stock Entry', 'Stock Entries (Receipt, Transfer, Scrap)'),
                        ('DocType', 'Purchase Receipt', 'Incoming Parts Receipts'),
                        ('DocType', 'Delivery Note', 'Finished Vehicle Dispatch Notes'),
                        ('DocType', 'Stock Reconciliation', 'Stock Reconciliation')
                    ]
                },
                {
                    'card_name': 'Inventory Reports',
                    'links': [
                        ('Report', 'Stock Balance', 'Stock Balance Report'),
                        ('Report', 'Stock Ledger', 'Stock Ledger'),
                        ('Report', 'Stock Analytics', 'Stock Analytics'),
                        ('Report', 'Stock Projected Qty', 'Stock Projected Quantity')
                    ]
                }
            ]
        },
        {
            'name': 'Procurement',
            'title': 'Procurement',
            'label': 'Procurement',
            'icon': 'buying',
            'module': 'Buying',
            'sequence_id': 4,
            'roles': ['Purchase Manager', 'Purchase User', 'System Manager'],
            'header': 'Supplier Management & Component Procurement',
            'shortcuts': [
                {'label': 'Purchase Orders', 'type': 'DocType', 'link_to': 'Purchase Order'},
                {'label': 'Suppliers', 'type': 'DocType', 'link_to': 'Supplier'},
                {'label': 'Material Requests', 'type': 'DocType', 'link_to': 'Material Request'},
                {'label': 'Purchase Receipts', 'type': 'DocType', 'link_to': 'Purchase Receipt'}
            ],
            'cards': [
                {
                    'card_name': 'Procurement Cycle',
                    'links': [
                        ('DocType', 'Supplier', 'Suppliers & Parts Manufacturers'),
                        ('DocType', 'Material Request', 'Material Requisitions'),
                        ('DocType', 'Request for Quotation', 'Request for Quotation (RFQ)'),
                        ('DocType', 'Supplier Quotation', 'Supplier Quotations'),
                        ('DocType', 'Purchase Order', 'Purchase Orders'),
                        ('DocType', 'Purchase Receipt', 'Purchase Receipts')
                    ]
                },
                {
                    'card_name': 'Procurement Analytics & Invoicing',
                    'links': [
                        ('DocType', 'Purchase Invoice', 'Purchase Invoices'),
                        ('Report', 'Purchase Order Analysis', 'Purchase Order Analysis'),
                        ('Report', 'Purchase Analytics', 'Purchase Analytics'),
                        ('Report', 'Supplier Quotation Comparison', 'Supplier Price Comparison')
                    ]
                }
            ]
        },
        {
            'name': 'Quality',
            'title': 'Quality',
            'label': 'Quality',
            'icon': 'quality',
            'module': 'Quality Management',
            'sequence_id': 5,
            'roles': ['Quality Manager', 'System Manager'],
            'header': 'Automotive Quality Assurance & Inspection Control',
            'shortcuts': [
                {'label': 'Quality Inspection', 'type': 'DocType', 'link_to': 'Quality Inspection'},
                {'label': 'Inspection Templates', 'type': 'DocType', 'link_to': 'Quality Inspection Template'},
                {'label': 'Defect Tracking', 'type': 'DocType', 'link_to': 'Non Conformance'},
                {'label': 'Finished Vehicles', 'type': 'DocType', 'link_to': 'Finished Vehicle Register'}
            ],
            'cards': [
                {
                    'card_name': 'Inspections & Standards',
                    'links': [
                        ('DocType', 'Quality Inspection', 'Quality Inspections (Incoming / In-Process / Final)'),
                        ('DocType', 'Quality Inspection Template', 'Inspection Templates (Body, Paint, Dyno)'),
                        ('DocType', 'Finished Vehicle Register', 'Finished Vehicle Sign-offs'),
                        ('DocType', 'Work Order', 'Work Orders (Read-Only)'),
                        ('DocType', 'Job Card', 'Assembly Job Cards (Read-Only)')
                    ]
                },
                {
                    'card_name': 'Defects & Non-Conformance',
                    'links': [
                        ('DocType', 'Non Conformance', 'Defect Tracking & Non Conformance'),
                        ('DocType', 'Item', 'Component Catalog (Read-Only)'),
                        ('Report', 'Quality Inspection Summary', 'Quality Inspection Summary Report')
                    ]
                }
            ]
        },
        {
            'name': 'Management',
            'title': 'Management',
            'label': 'Management',
            'icon': 'dashboard',
            'module': 'Manufacturing',
            'sequence_id': 6,
            'roles': ['System Manager', 'Administrator'],
            'header': 'Automotive Executive Overview & Management',
            'shortcuts': [
                {'label': 'Manufacturing Dashboard', 'type': 'Dashboard', 'link_to': 'Manufacturing'},
                {'label': 'Vehicle Models', 'type': 'DocType', 'link_to': 'Vehicle Model'},
                {'label': 'Production Plans', 'type': 'DocType', 'link_to': 'Production Plan'},
                {'label': 'Finished Vehicles', 'type': 'DocType', 'link_to': 'Finished Vehicle Register'},
                {'label': 'General Ledger', 'type': 'Report', 'link_to': 'General Ledger'}
            ],
            'cards': [
                {
                    'card_name': 'Executive Overview',
                    'links': [
                        ('DocType', 'Vehicle Model', 'Vehicle Models'),
                        ('DocType', 'Finished Vehicle Register', 'Finished Vehicle Fleet'),
                        ('DocType', 'Production Plan', 'Production Plans'),
                        ('DocType', 'Work Order', 'Work Orders Overview'),
                        ('DocType', 'Supplier', 'Suppliers'),
                        ('DocType', 'Customer', 'Dealers & Customers')
                    ]
                },
                {
                    'card_name': 'Essential Finance & HR',
                    'links': [
                        ('DocType', 'Sales Invoice', 'Sales Invoices'),
                        ('DocType', 'Purchase Invoice', 'Purchase Invoices'),
                        ('DocType', 'Payment Entry', 'Payment Entries'),
                        ('DocType', 'Employee', 'Plant Personnel & Workforce'),
                        ('DocType', 'Timesheet', 'Production Timesheets')
                    ]
                },
                {
                    'card_name': 'Executive Reports',
                    'links': [
                        ('Report', 'Profit and Loss Statement', 'Profit & Loss Statement'),
                        ('Report', 'General Ledger', 'General Ledger'),
                        ('Report', 'Work Order Summary', 'Production Summary'),
                        ('Report', 'Stock Balance', 'Inventory Valuation')
                    ]
                }
            ]
        }
    ]

    for wcfg in role_workspaces:
        wname = wcfg['name']
        wlabel = wcfg['label']
        if frappe.db.exists('Workspace', wlabel):
            w = frappe.get_doc('Workspace', wlabel)
        elif frappe.db.exists('Workspace', wname):
            w = frappe.get_doc('Workspace', wname)
        else:
            w = frappe.new_doc('Workspace')
            w.name = wlabel

        w.title = wcfg['title']
        w.label = wcfg['label']
        w.type = 'Workspace'
        w.public = 1
        w.is_hidden = 0
        w.icon = wcfg['icon']
        w.module = wcfg['module']
        w.sequence_id = wcfg['sequence_id']

        # Content blocks
        content_blocks = [
            {'id': f'hdr_{wname[:8]}', 'type': 'header', 'data': {'text': f'<span class="h4"><b>{wcfg["header"]}</b></span>', 'col': 12}}
        ]
        for sc in wcfg.get('shortcuts', []):
            content_blocks.append({
                'id': f'sc_{sc["label"][:8]}',
                'type': 'shortcut',
                'data': {'shortcut_name': sc['label'], 'col': 3}
            })
        for c in wcfg['cards']:
            content_blocks.append({
                'id': f'c_{c["card_name"][:8]}',
                'type': 'card',
                'data': {'card_name': c['card_name'], 'col': 6}
            })
        w.content = json.dumps(content_blocks)

        # Links
        w.set('links', [])
        for c in wcfg['cards']:
            w.append('links', {'type': 'Card Break', 'label': c['card_name']})
            for link_type, link_to, lbl in c['links']:
                w.append('links', {
                    'type': 'Link',
                    'label': lbl,
                    'link_type': link_type,
                    'link_to': link_to,
                    'is_query_report': 1 if link_type == 'Report' else 0
                })

        # Shortcuts
        w.set('shortcuts', [])
        for sc in wcfg.get('shortcuts', []):
            w.append('shortcuts', {
                'label': sc['label'],
                'type': sc['type'],
                'link_to': sc['link_to']
            })

        # Roles
        w.set('roles', [])
        for r in wcfg['roles']:
            w.append('roles', {'role': r})

        w.save(ignore_permissions=True)
        print(f"  Configured Role Workspace [{wname}] -> Roles: {wcfg['roles']}")

    frappe.clear_cache()
    frappe.db.commit()


def run():
    frappe.set_user('Administrator')
    print("====================================================================")
    print("   ORBIS ERP: AUTOMOTIVE WORKSPACE & INTERFACE SIMPLIFICATION        ")
    print("====================================================================\n")

    create_automotive_doctypes()
    seed_automotive_models()
    hide_irrelevant_workspaces()
    setup_primary_automotive_workspace()
    setup_role_based_workspaces()

    print("\n====================================================================")
    print("   AUTOMOTIVE WORKSPACE CONFIGURATION COMPLETED SUCCESSFULLY        ")
    print("====================================================================")
    return "SUCCESS"

if __name__ == '__main__':
    frappe.init(site='frontend', sites_path='/home/frappe/frappe-bench/sites')
    frappe.connect()
    run()
    frappe.destroy()
