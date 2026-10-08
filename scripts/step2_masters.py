# pyrefly: ignore [missing-import]
import frappe

COMPANY = 'Orbis Car Manufacturing (Pvt.) Ltd.'
ABBR = 'OCM'
CURRENCY = 'PKR'

def run():
    frappe.set_user('Administrator')
    print('--- Step 2: Creating Item Groups, Items, Suppliers, Customers, Operations, Workstations, BOMs ---')

    # 1. Item Groups
    # Required groups: Finished Cars, Raw Materials, Metals, Rubber Components, Glass Components, Electrical Components,
    # Engine Components, Interior Components, Safety Components, Battery Components, Manufactured Components, Spare Parts, Consumables
    all_item_groups = [
        ('Finished Cars', 'All Item Groups', 0),
        ('Raw Materials', 'All Item Groups', 1),
        ('Metals', 'Raw Materials', 0),
        ('Rubber Components', 'Raw Materials', 0),
        ('Glass Components', 'Raw Materials', 0),
        ('Electrical Components', 'Raw Materials', 0),
        ('Battery Components', 'Raw Materials', 0),
        ('Consumables', 'Raw Materials', 0),
        ('Manufactured Components', 'All Item Groups', 1),
        ('Engine Components', 'Manufactured Components', 0),
        ('Interior Components', 'Manufactured Components', 0),
        ('Safety Components', 'Manufactured Components', 0),
        ('Spare Parts', 'All Item Groups', 0)
    ]
    for grp_name, parent, is_grp in all_item_groups:
        if not frappe.db.exists('Item Group', grp_name):
            ig = frappe.new_doc('Item Group')
            ig.item_group_name = grp_name
            ig.parent_item_group = parent
            ig.is_group = is_grp
            ig.insert(ignore_permissions=True)
            print(f'Created Item Group: {grp_name}')
        else:
            print(f'Item Group exists: {grp_name}')

    # 2. UOM check
    for u in ['Nos', 'Kg', 'Liter', 'Meter', 'Set']:
        if not frappe.db.exists('UOM', u):
            uom = frappe.new_doc('UOM')
            uom.uom_name = u
            uom.insert(ignore_permissions=True)

    # 3. Suppliers
    suppliers = [
        ('Pakistan Steel Suppliers', 'Raw Material'),
        ('Orbis Auto Components', 'Components'),
        ('Pak Rubber Industries', 'Raw Material'),
        ('National Glass Components', 'Components'),
        ('Pak Battery Solutions', 'Electrical'),
        ('Auto Electrical Supplies', 'Electrical'),
        ('Prime Tyres Pakistan', 'Components'),
        ('Industrial Paint Suppliers', 'Raw Material'),
        ('Auto Interior Materials', 'Raw Material'),
        ('Engineering Components Ltd.', 'Mechanical')
    ]
    for s_name, s_group in suppliers:
        if not frappe.db.exists('Supplier Group', s_group):
            sg = frappe.new_doc('Supplier Group')
            sg.supplier_group_name = s_group
            sg.insert(ignore_permissions=True)
        if not frappe.db.exists('Supplier', s_name):
            s = frappe.new_doc('Supplier')
            s.supplier_name = s_name
            s.supplier_group = s_group
            s.country = 'Pakistan'
            s.insert(ignore_permissions=True)
            print(f'Created Supplier: {s_name}')

    # 4. Customers / Dealers
    dealers = [
        'Ahmed Motors',
        'Karachi Auto Dealers',
        'Lahore Motors',
        'Islamabad Auto Gallery',
        'Pak Wheels Dealership',
        'Multan Auto Center',
        'Faisalabad Motors',
        'Rawalpindi Auto Traders'
    ]
    for c_name in dealers:
        if not frappe.db.exists('Customer', c_name):
            c = frappe.new_doc('Customer')
            c.customer_name = c_name
            c.customer_type = 'Company'
            c.customer_group = 'Commercial'
            c.territory = 'Pakistan'
            c.insert(ignore_permissions=True)
            print(f'Created Customer: {c_name}')

    # 5. Workstations
    workstations = [
        'Body Assembly Station',
        'Engine Assembly Station',
        'Mechanical Assembly Station',
        'Electrical Assembly Station',
        'Interior Assembly Station',
        'Painting Station',
        'Final Assembly Station',
        'Quality Inspection Station',
        'Testing Station'
    ]
    for ws_name in workstations:
        if not frappe.db.exists('Workstation', ws_name):
            ws = frappe.new_doc('Workstation')
            ws.workstation_name = ws_name
            ws.hour_rate = 1500
            ws.insert(ignore_permissions=True)
            print(f'Created Workstation: {ws_name}')

    # 6. Operations
    operations = [
        ('Body Assembly', 'Body Assembly Station'),
        ('Engine Installation', 'Engine Assembly Station'),
        ('Transmission Installation', 'Mechanical Assembly Station'),
        ('Suspension Installation', 'Mechanical Assembly Station'),
        ('Brake Installation', 'Mechanical Assembly Station'),
        ('Electrical Installation', 'Electrical Assembly Station'),
        ('Interior Installation', 'Interior Assembly Station'),
        ('Glass Installation', 'Body Assembly Station'),
        ('Wheel Installation', 'Mechanical Assembly Station'),
        ('Battery Installation', 'Electrical Assembly Station'),
        ('Painting', 'Painting Station'),
        ('Final Assembly', 'Final Assembly Station'),
        ('Quality Inspection', 'Quality Inspection Station'),
        ('Final Testing', 'Testing Station'),
        ('Motor Installation', 'Mechanical Assembly Station'),
        ('Charging System Installation', 'Electrical Assembly Station'),
        ('Electrical System Testing', 'Testing Station')
    ]
    for op_name, ws_name in operations:
        if not frappe.db.exists('Operation', op_name):
            op = frappe.new_doc('Operation')
            op.name = op_name
            op.operation = op_name
            op.workstation = ws_name
            op.insert(ignore_permissions=True)
            print(f'Created Operation: {op_name}')

    # 7. Items
    # Category A: Finished Cars
    finished_cars = [
        ('Orbis O1 Sedan', 'Finished Cars', 'Nos', 6500000),
        ('Orbis X1 SUV', 'Finished Cars', 'Nos', 11500000),
        ('Orbis E1 Electric', 'Finished Cars', 'Nos', 14000000)
    ]

    # Category B: Raw Materials
    raw_materials = [
        # Metals
        ('Steel Sheet', 'Metals', 'Nos', 15000),
        ('Stainless Steel', 'Metals', 'Kg', 850),
        ('Aluminium Sheet', 'Metals', 'Nos', 18000),
        ('Aluminium Components', 'Metals', 'Nos', 5000),
        # Rubber
        ('Tyre Rubber', 'Rubber Components', 'Kg', 600),
        ('Rubber Seals', 'Rubber Components', 'Meter', 250),
        ('Rubber Hoses', 'Rubber Components', 'Meter', 350),
        # Glass
        ('Windshield Glass', 'Glass Components', 'Nos', 25000),
        ('Side Window Glass', 'Glass Components', 'Nos', 8000),
        ('Rear Window Glass', 'Glass Components', 'Nos', 15000),
        # Interior
        ('Seat Fabric', 'Interior Components', 'Meter', 1200),
        ('Leather', 'Interior Components', 'Meter', 3500),
        ('Plastic Interior Material', 'Interior Components', 'Kg', 450),
        ('Dashboard Material', 'Interior Components', 'Nos', 12000),
        # Electrical
        ('Electrical Wiring', 'Electrical Components', 'Meter', 180),
        ('LED Headlights', 'Electrical Components', 'Set', 35000),
        ('Sensors', 'Electrical Components', 'Nos', 4500),
        ('Fuses', 'Electrical Components', 'Nos', 50),
        ('Connectors', 'Electrical Components', 'Nos', 120),
        # Battery
        ('Battery Cells', 'Battery Components', 'Nos', 2200),
        ('Car Battery', 'Battery Components', 'Nos', 28000),
        ('Battery Casing', 'Battery Components', 'Nos', 15000),
        # Consumables / Other
        ('Paint', 'Consumables', 'Liter', 1800),
        ('Lubricant', 'Consumables', 'Liter', 950),
        ('Engine Oil', 'Consumables', 'Liter', 1400),
        ('Coolant', 'Consumables', 'Liter', 750),
        ('Adhesive', 'Consumables', 'Liter', 650),
        ('Fasteners', 'Consumables', 'Nos', 15),
        ('Nuts and Bolts', 'Consumables', 'Set', 45)
    ]

    # Category C: Manufactured Components
    components = [
        ('Engine Assembly', 'Engine Components', 'Nos', 650000),
        ('Transmission Assembly', 'Manufactured Components', 'Nos', 420000),
        ('Brake Assembly', 'Manufactured Components', 'Nos', 85000),
        ('Steering Assembly', 'Manufactured Components', 'Nos', 65000),
        ('Suspension Assembly', 'Manufactured Components', 'Nos', 110000),
        ('Wheel Assembly', 'Manufactured Components', 'Nos', 45000),
        ('Car Body Assembly', 'Manufactured Components', 'Nos', 850000),
        ('Seat Assembly', 'Interior Components', 'Set', 95000),
        ('Dashboard Assembly', 'Interior Components', 'Nos', 75000),
        ('Battery Assembly', 'Battery Components', 'Nos', 90000),
        ('Electrical Assembly', 'Electrical Components', 'Nos', 120000),
        ('Exhaust Assembly', 'Manufactured Components', 'Nos', 55000),
        ('Cooling System Assembly', 'Manufactured Components', 'Nos', 60000),
        ('Fuel System Assembly', 'Manufactured Components', 'Nos', 70000),
        # EV Components
        ('EV Body Assembly', 'Manufactured Components', 'Nos', 950000),
        ('Battery Pack', 'Battery Components', 'Nos', 1800000),
        ('Electric Motor', 'Manufactured Components', 'Nos', 750000),
        ('Battery Management System', 'Electrical Components', 'Nos', 180000),
        ('Charging Components', 'Electrical Components', 'Set', 120000)
    ]

    # Standard Price List
    standard_selling = 'Standard Selling'
    standard_buying = 'Standard Buying'

    # Helper function to create items
    def create_item(name, group, uom, val_rate, is_manufacturing=False):
        if not frappe.db.exists('Item', name):
            it = frappe.new_doc('Item')
            it.item_code = name
            it.item_name = name
            it.item_group = group
            it.stock_uom = uom
            it.is_stock_item = 1
            it.valuation_rate = val_rate
            it.include_item_in_manufacturing = 1 if is_manufacturing else 0
            it.default_warehouse = f'Raw Material Warehouse - {ABBR}' if group in ['Raw Materials', 'Metals', 'Rubber Components', 'Glass Components', 'Consumables'] else f'Components Warehouse - {ABBR}'
            if group == 'Finished Cars':
                it.default_warehouse = f'Finished Goods Warehouse - {ABBR}'
            it.insert(ignore_permissions=True)
            print(f'Created Item: {name}')
        else:
            print(f'Item exists: {name}')

        # Add price in standard price list
        pl = standard_selling if group == 'Finished Cars' else standard_buying
        if not frappe.db.exists('Item Price', {'item_code': name, 'price_list': pl}):
            ip = frappe.new_doc('Item Price')
            ip.item_code = name
            ip.price_list = pl
            ip.price_list_rate = val_rate
            ip.currency = CURRENCY
            ip.insert(ignore_permissions=True)

    for item_tuple in finished_cars:
        create_item(item_tuple[0], item_tuple[1], item_tuple[2], item_tuple[3], is_manufacturing=True)

    for item_tuple in raw_materials:
        create_item(item_tuple[0], item_tuple[1], item_tuple[2], item_tuple[3], is_manufacturing=False)

    for item_tuple in components:
        create_item(item_tuple[0], item_tuple[1], item_tuple[2], item_tuple[3], is_manufacturing=True)

    # 8. Bills of Materials (BOMs)
    boms_config = [
        {
            'item': 'Orbis O1 Sedan',
            'qty': 1,
            'materials': [
                ('Car Body Assembly', 1),
                ('Engine Assembly', 1),
                ('Transmission Assembly', 1),
                ('Wheel Assembly', 4),
                ('Seat Assembly', 1),
                ('Dashboard Assembly', 1),
                ('Windshield Glass', 1),
                ('Side Window Glass', 4),
                ('Rear Window Glass', 1),
                ('Car Battery', 1),
                ('Brake Assembly', 1),
                ('Steering Assembly', 1),
                ('Suspension Assembly', 1),
                ('Electrical Assembly', 1),
                ('LED Headlights', 1),
                ('Cooling System Assembly', 1),
                ('Exhaust Assembly', 1),
                ('Fuel System Assembly', 1),
                ('Fasteners', 50),
                ('Paint', 5),
                ('Engine Oil', 4),
                ('Coolant', 4)
            ],
            'operations': [
                ('Body Assembly', 'Body Assembly Station', 60),
                ('Engine Installation', 'Engine Assembly Station', 45),
                ('Transmission Installation', 'Mechanical Assembly Station', 45),
                ('Suspension Installation', 'Mechanical Assembly Station', 30),
                ('Brake Installation', 'Mechanical Assembly Station', 30),
                ('Electrical Installation', 'Electrical Assembly Station', 45),
                ('Interior Installation', 'Interior Assembly Station', 40),
                ('Glass Installation', 'Body Assembly Station', 25),
                ('Wheel Installation', 'Mechanical Assembly Station', 20),
                ('Painting', 'Painting Station', 90),
                ('Final Assembly', 'Final Assembly Station', 60),
                ('Quality Inspection', 'Quality Inspection Station', 30),
                ('Final Testing', 'Testing Station', 30)
            ]
        },
        {
            'item': 'Orbis X1 SUV',
            'qty': 1,
            'materials': [
                ('Car Body Assembly', 1),
                ('Engine Assembly', 1),
                ('Transmission Assembly', 1),
                ('Wheel Assembly', 4),
                ('Seat Assembly', 1),
                ('Dashboard Assembly', 1),
                ('Windshield Glass', 1),
                ('Side Window Glass', 4),
                ('Rear Window Glass', 1),
                ('Car Battery', 1),
                ('Brake Assembly', 1),
                ('Steering Assembly', 1),
                ('Suspension Assembly', 1),
                ('Electrical Assembly', 1),
                ('LED Headlights', 1),
                ('Cooling System Assembly', 1),
                ('Exhaust Assembly', 1),
                ('Fuel System Assembly', 1),
                ('Fasteners', 60),
                ('Paint', 7),
                ('Engine Oil', 5),
                ('Coolant', 5)
            ],
            'operations': [
                ('Body Assembly', 'Body Assembly Station', 75),
                ('Engine Installation', 'Engine Assembly Station', 50),
                ('Transmission Installation', 'Mechanical Assembly Station', 50),
                ('Suspension Installation', 'Mechanical Assembly Station', 35),
                ('Brake Installation', 'Mechanical Assembly Station', 35),
                ('Electrical Installation', 'Electrical Assembly Station', 50),
                ('Interior Installation', 'Interior Assembly Station', 45),
                ('Glass Installation', 'Body Assembly Station', 30),
                ('Wheel Installation', 'Mechanical Assembly Station', 25),
                ('Painting', 'Painting Station', 100),
                ('Final Assembly', 'Final Assembly Station', 70),
                ('Quality Inspection', 'Quality Inspection Station', 35),
                ('Final Testing', 'Testing Station', 35)
            ]
        },
        {
            'item': 'Orbis E1 Electric',
            'qty': 1,
            'materials': [
                ('EV Body Assembly', 1),
                ('Battery Pack', 1),
                ('Electric Motor', 1),
                ('Battery Management System', 1),
                ('Charging Components', 1),
                ('Wheel Assembly', 4),
                ('Seat Assembly', 1),
                ('Dashboard Assembly', 1),
                ('Windshield Glass', 1),
                ('Side Window Glass', 4),
                ('Rear Window Glass', 1),
                ('Brake Assembly', 1),
                ('Steering Assembly', 1),
                ('Suspension Assembly', 1),
                ('Electrical Assembly', 1),
                ('LED Headlights', 1),
                ('Fasteners', 40),
                ('Paint', 6),
                ('Coolant', 3)
            ],
            'operations': [
                ('Body Assembly', 'Body Assembly Station', 60),
                ('Motor Installation', 'Mechanical Assembly Station', 40),
                ('Battery Installation', 'Electrical Assembly Station', 50),
                ('Charging System Installation', 'Electrical Assembly Station', 30),
                ('Suspension Installation', 'Mechanical Assembly Station', 30),
                ('Brake Installation', 'Mechanical Assembly Station', 30),
                ('Interior Installation', 'Interior Assembly Station', 40),
                ('Glass Installation', 'Body Assembly Station', 25),
                ('Wheel Installation', 'Mechanical Assembly Station', 20),
                ('Painting', 'Painting Station', 90),
                ('Final Assembly', 'Final Assembly Station', 60),
                ('Electrical System Testing', 'Testing Station', 45),
                ('Quality Inspection', 'Quality Inspection Station', 30),
                ('Final Testing', 'Testing Station', 30)
            ]
        }
    ]

    for b in boms_config:
        item_code = b['item']
        if not frappe.db.exists('BOM', {'item': item_code, 'is_active': 1}):
            bom = frappe.new_doc('BOM')
            bom.item = item_code
            bom.quantity = b['qty']
            bom.company = COMPANY
            bom.is_active = 1
            bom.is_default = 1
            bom.with_operations = 1

            for mat_item, mat_qty in b['materials']:
                uom = frappe.db.get_value('Item', mat_item, 'stock_uom') or 'Nos'
                bom.append('items', {
                    'item_code': mat_item,
                    'qty': mat_qty,
                    'uom': uom,
                    'stock_uom': uom
                })

            for op_name, ws_name, time_mins in b['operations']:
                bom.append('operations', {
                    'operation': op_name,
                    'workstation': ws_name,
                    'time_in_mins': time_mins,
                    'hour_rate': 1500
                })

            bom.insert(ignore_permissions=True)
            bom.submit()
            print(f'Created & Submitted BOM: {bom.name} for {item_code}')
        else:
            bom_name = frappe.db.get_value('BOM', {'item': item_code, 'is_active': 1}, 'name')
            print(f'BOM exists: {bom_name} for {item_code}')

    frappe.db.commit()
    print('--- Step 2 Finished Successfully! ---')
    return 'Step 2 Complete'
