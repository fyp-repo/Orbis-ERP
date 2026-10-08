import frappe
from frappe.utils import nowdate, add_days

COMPANY = 'Orbis Car Manufacturing (Pvt.) Ltd.'
ABBR = 'OCM'
CURRENCY = 'PKR'

def run():
    frappe.set_user('Administrator')
    print('--- Step 3: Setting up Connected Transactions (Purchasing, Stock, Manufacturing, Quality, Sales, Accounting) ---')

    today = nowdate()

    # 1. Bank Account Setup for OCM
    bank_parent = f'Bank Accounts - {ABBR}'
    bank_acc_name = f'Habib Bank Limited - {ABBR}'
    if not frappe.db.exists('Account', bank_acc_name):
        ba = frappe.new_doc('Account')
        ba.account_name = 'Habib Bank Limited'
        ba.parent_account = bank_parent
        ba.company = COMPANY
        ba.account_type = 'Bank'
        ba.is_group = 0
        ba.insert(ignore_permissions=True)
        print(f'Created Bank Account: {bank_acc_name}')

    comp_doc = frappe.get_doc('Company', COMPANY)
    comp_doc.default_bank_account = bank_acc_name
    comp_doc.default_cost_center = f'Main - {ABBR}'
    comp_doc.default_operating_cost_account = f'Expenses Included In Valuation - {ABBR}'
    comp_doc.save(ignore_permissions=True)

    # Ensure all warehouses have stock account set
    wh_qb = frappe.qb.DocType('Warehouse')
    frappe.qb.update(wh_qb).set(wh_qb.account, f'Stock In Hand - {ABBR}').where(wh_qb.company == COMPANY).run()
    frappe.db.commit()

    # Ensure all BOM items have include_item_in_manufacturing = 1
    frappe.qb.update(frappe.qb.DocType('BOM Item')).set('include_item_in_manufacturing', 1).run()
    frappe.qb.update(frappe.qb.DocType('BOM Explosion Item')).set('include_item_in_manufacturing', 1).run()
    frappe.db.commit()

    # 2. Quality Inspection Parameters
    qi_params = [
        'Engine Performance Check',
        'Brake Force & Response Test',
        'Safety & Restraint System Check',
        'Electrical System Diagnostic',
        'Paint & Finish Quality Check',
        'Road Handling & Suspension Test'
    ]
    for param in qi_params:
        if not frappe.db.exists('Quality Inspection Parameter', param):
            qip = frappe.new_doc('Quality Inspection Parameter')
            qip.parameter = param
            qip.description = param
            qip.insert(ignore_permissions=True)
            print(f'Created Quality Inspection Parameter: {param}')

    # 3. Material Requests & Purchase Orders
    raw_wh = f'Raw Material Warehouse - {ABBR}'
    comp_wh = f'Components Warehouse - {ABBR}'
    wip_wh = f'Work In Progress Warehouse - {ABBR}'
    fg_wh = f'Finished Goods Warehouse - {ABBR}'
    quality_wh = f'Quality Hold Warehouse - {ABBR}'
    prod_store_wh = f'Production Store - {ABBR}'
    spare_wh = f'Spare Parts Warehouse - {ABBR}'

    # Create Material Request
    if not frappe.db.exists('Material Request', {'company': COMPANY}):
        mr = frappe.new_doc('Material Request')
        mr.company = COMPANY
        mr.material_request_type = 'Purchase'
        mr.schedule_date = add_days(today, 7)
        for it_name, qty, wh in [
            ('Steel Sheet', 500, raw_wh),
            ('Windshield Glass', 100, raw_wh),
            ('Car Battery', 100, comp_wh),
            ('Brake Assembly', 500, comp_wh),
            ('Wheel Assembly', 200, comp_wh)
        ]:
            uom = frappe.db.get_value('Item', it_name, 'stock_uom') or 'Nos'
            mr.append('items', {
                'item_code': it_name,
                'qty': qty,
                'schedule_date': add_days(today, 7),
                'warehouse': wh,
                'uom': uom
            })
        mr.insert(ignore_permissions=True)
        mr.submit()
        print(f'Created & Submitted Material Request: {mr.name}')

    # Helper function to create Purchase Order and Receipt
    def create_po_and_receipt(supplier, items_list, bill_and_pay=False):
        po = frappe.new_doc('Purchase Order')
        po.supplier = supplier
        po.company = COMPANY
        po.transaction_date = today
        po.schedule_date = add_days(today, 5)
        po.currency = CURRENCY

        for item_code, qty, rate, wh in items_list:
            uom = frappe.db.get_value('Item', item_code, 'stock_uom') or 'Nos'
            po.append('items', {
                'item_code': item_code,
                'qty': qty,
                'rate': rate,
                'warehouse': wh,
                'uom': uom,
                'stock_uom': uom,
                'schedule_date': add_days(today, 5)
            })

        po.insert(ignore_permissions=True)
        po.submit()
        print(f'Created & Submitted Purchase Order: {po.name} for {supplier}')

        # Create Purchase Receipt
        pr = frappe.new_doc('Purchase Receipt')
        pr.supplier = supplier
        pr.company = COMPANY
        pr.posting_date = today
        pr.currency = CURRENCY
        pr.purchase_order = po.name

        for po_item in po.items:
            pr.append('items', {
                'item_code': po_item.item_code,
                'qty': po_item.qty,
                'rate': po_item.rate,
                'warehouse': po_item.warehouse,
                'purchase_order': po.name,
                'purchase_order_item': po_item.name,
                'uom': po_item.uom,
                'stock_uom': po_item.stock_uom
            })

        pr.insert(ignore_permissions=True)
        pr.submit()
        print(f'Created & Submitted Purchase Receipt: {pr.name}')

        # Create Purchase Invoice and Payment if requested
        if bill_and_pay:
            pi = frappe.new_doc('Purchase Invoice')
            pi.supplier = supplier
            pi.company = COMPANY
            pi.posting_date = today
            pi.currency = CURRENCY
            pi.credit_to = f'Creditors - {ABBR}'

            for pr_item in pr.items:
                pi.append('items', {
                    'item_code': pr_item.item_code,
                    'qty': pr_item.qty,
                    'rate': pr_item.rate,
                    'purchase_receipt': pr.name,
                    'pr_detail': pr_item.name,
                    'purchase_order': po.name,
                    'po_detail': pr_item.purchase_order_item,
                    'uom': pr_item.uom,
                    'stock_uom': pr_item.stock_uom,
                    'expense_account': f'Cost of Goods Sold - {ABBR}'
                })

            pi.insert(ignore_permissions=True)
            pi.submit()
            print(f'Created & Submitted Purchase Invoice: {pi.name}')

            # Create Payment Entry
            pe = frappe.new_doc('Payment Entry')
            pe.payment_type = 'Pay'
            pe.party_type = 'Supplier'
            pe.party = supplier
            pe.company = COMPANY
            pe.posting_date = today
            pe.paid_from = bank_acc_name
            pe.paid_to = f'Creditors - {ABBR}'
            pe.paid_amount = pi.grand_total
            pe.received_amount = pi.grand_total
            pe.reference_no = f'PAY-REF-{po.name}'
            pe.reference_date = today

            pe.append('references', {
                'reference_doctype': 'Purchase Invoice',
                'reference_name': pi.name,
                'total_amount': pi.grand_total,
                'outstanding_amount': pi.grand_total,
                'allocated_amount': pi.grand_total
            })

            pe.insert(ignore_permissions=True)
            pe.submit()
            print(f'Created & Submitted Payment Entry to {supplier}: {pe.name} (PKR {pe.paid_amount:,})')

        return po, pr

    # Check if Purchase Orders already created
    if frappe.db.count('Purchase Order', {'company': COMPANY}) == 0:
        # 1. Pakistan Steel Suppliers
        create_po_and_receipt('Pakistan Steel Suppliers', [
            ('Steel Sheet', 500, 15000, raw_wh),
            ('Stainless Steel', 100, 850, raw_wh),
            ('Aluminium Sheet', 100, 18000, raw_wh),
            ('Aluminium Components', 50, 5000, raw_wh)
        ], bill_and_pay=True)

        # 2. Orbis Auto Components
        create_po_and_receipt('Orbis Auto Components', [
            ('Brake Assembly', 500, 85000, comp_wh),
            ('Steering Assembly', 30, 65000, comp_wh),
            ('Suspension Assembly', 30, 110000, comp_wh),
            ('Engine Assembly', 30, 650000, comp_wh),
            ('Transmission Assembly', 30, 420000, comp_wh),
            ('Car Body Assembly', 20, 850000, comp_wh),
            ('Exhaust Assembly', 30, 55000, comp_wh),
            ('Cooling System Assembly', 30, 60000, comp_wh),
            ('Fuel System Assembly', 30, 70000, comp_wh)
        ], bill_and_pay=True)

        # 3. Prime Tyres Pakistan
        create_po_and_receipt('Prime Tyres Pakistan', [
            ('Wheel Assembly', 200, 45000, comp_wh)
        ])

        # 4. National Glass Components
        create_po_and_receipt('National Glass Components', [
            ('Windshield Glass', 100, 25000, raw_wh),
            ('Side Window Glass', 200, 8000, raw_wh),
            ('Rear Window Glass', 100, 15000, raw_wh)
        ])

        # 5. Pak Battery Solutions
        create_po_and_receipt('Pak Battery Solutions', [
            ('Car Battery', 100, 28000, comp_wh),
            ('Battery Assembly', 50, 90000, comp_wh)
        ])

        # 6. Auto Electrical Supplies
        create_po_and_receipt('Auto Electrical Supplies', [
            ('Electrical Assembly', 30, 120000, comp_wh),
            ('LED Headlights', 50, 35000, comp_wh),
            ('Electrical Wiring', 1000, 180, raw_wh),
            ('Sensors', 100, 4500, comp_wh)
        ])

        # 7. Industrial Paint Suppliers
        create_po_and_receipt('Industrial Paint Suppliers', [
            ('Paint', 200, 1800, raw_wh),
            ('Engine Oil', 200, 1400, raw_wh),
            ('Coolant', 200, 750, raw_wh),
            ('Fasteners', 2000, 15, raw_wh)
        ])

        # 8. Auto Interior Materials
        create_po_and_receipt('Auto Interior Materials', [
            ('Seat Assembly', 30, 95000, comp_wh),
            ('Dashboard Assembly', 30, 75000, comp_wh)
        ])

        # 9. Engineering Components Ltd.
        create_po_and_receipt('Engineering Components Ltd.', [
            ('EV Body Assembly', 10, 950000, comp_wh),
            ('Battery Pack', 10, 1800000, comp_wh),
            ('Electric Motor', 10, 750000, comp_wh),
            ('Battery Management System', 10, 180000, comp_wh),
            ('Charging Components', 10, 120000, comp_wh)
        ])

        # Also place some spare items into Spare Parts Warehouse
        se_spare = frappe.new_doc('Stock Entry')
        se_spare.purpose = 'Material Transfer'
        se_spare.stock_entry_type = 'Material Transfer'
        se_spare.company = COMPANY
        se_spare.posting_date = today
        for itm_name, s_wh, qty in [
            ('Brake Assembly', comp_wh, 20),
            ('Wheel Assembly', comp_wh, 20),
            ('LED Headlights', comp_wh, 10),
            ('Car Battery', comp_wh, 10),
            ('Windshield Glass', raw_wh, 10)
        ]:
            se_spare.append('items', {
                'item_code': itm_name,
                'qty': qty,
                's_warehouse': s_wh,
                't_warehouse': spare_wh,
                'uom': 'Nos',
                'stock_uom': 'Nos',
                'conversion_factor': 1
            })
        se_spare.insert(ignore_permissions=True)
        se_spare.submit()
        print(f'Stocked Spare Parts Warehouse: {se_spare.name}')

    # 4. Manufacturing Work Orders
    # Required Work Orders:
    # 5 x Orbis O1 Sedan
    # 3 x Orbis X1 SUV
    # 2 x Orbis E1 Electric
    wo_orders = [
        ('Orbis O1 Sedan', 'BOM-Orbis O1 Sedan-001', 5, True),
        ('Orbis X1 SUV', 'BOM-Orbis X1 SUV-001', 3, True),
        ('Orbis E1 Electric', 'BOM-Orbis E1 Electric-001', 2, False)  # Material issued to WIP, tested & failed
    ]

    raw_items = ['Steel Sheet', 'Windshield Glass', 'Side Window Glass', 'Rear Window Glass', 'Paint', 'Engine Oil', 'Coolant', 'Fasteners', 'Tyre Rubber', 'Rubber Seals', 'Rubber Hoses', 'Electrical Wiring']
    from erpnext.manufacturing.doctype.work_order.work_order import make_stock_entry

    created_wos = {}
    created_ste = {}

    for item_code, bom_name, qty, complete_manufacture in wo_orders:
        if not frappe.db.exists('Work Order', {'production_item': item_code, 'company': COMPANY}):
            wo = frappe.new_doc('Work Order')
            wo.company = COMPANY
            wo.production_item = item_code
            wo.bom_no = bom_name
            wo.qty = qty
            wo.wip_warehouse = wip_wh
            wo.fg_warehouse = fg_wh
            wo.planned_start_date = today
            wo.insert(ignore_permissions=True)
            wo.submit()
            created_wos[item_code] = wo
            print(f'Created & Submitted Work Order: {wo.name} for {qty} x {item_code}')

            # 1. Material Transfer for Manufacture
            se_transfer = frappe.get_doc(make_stock_entry(wo.name, 'Material Transfer for Manufacture', qty=qty))
            for itm in se_transfer.items:
                itm.s_warehouse = raw_wh if itm.item_code in raw_items else comp_wh
                itm.t_warehouse = wip_wh
            se_transfer.insert(ignore_permissions=True)
            se_transfer.submit()
            print(f'Created & Submitted Material Transfer Stock Entry: {se_transfer.name} for {wo.name}')

            # 2. Complete Manufacture into Finished Goods if completed
            if complete_manufacture:
                se_mfg = frappe.get_doc(make_stock_entry(wo.name, 'Manufacture', qty=qty))
                for itm in se_mfg.items:
                    if not itm.is_finished_item:
                        itm.s_warehouse = wip_wh
                    else:
                        itm.t_warehouse = fg_wh
                se_mfg.insert(ignore_permissions=True)
                se_mfg.submit()
                created_ste[item_code] = se_mfg
                print(f'Created & Submitted Manufacture Stock Entry: {se_mfg.name} -> {qty} x {item_code} in {fg_wh}')
            else:
                created_ste[item_code] = se_transfer
        else:
            wo_name = frappe.db.get_value('Work Order', {'production_item': item_code, 'company': COMPANY}, 'name')
            created_wos[item_code] = frappe.get_doc('Work Order', wo_name)

    # 5. Quality Inspections
    # Passed Examples: Orbis O1 Sedan, Orbis X1 SUV
    # Failed Example: Orbis E1 Electric (Reason: Electrical system issue)
    qi_records = [
        {
            'item': 'Orbis O1 Sedan',
            'status': 'Accepted',
            'ref_type': 'Stock Entry',
            'ref_name': created_ste.get('Orbis O1 Sedan', frappe._dict(name='MAT-STE-2026-00003')).name,
            'remarks': 'All 150-point factory quality checks PASSED. Emissions, drivetrain, safety approved.',
            'readings': [
                ('Engine Performance Check', 'Accepted'),
                ('Brake Force & Response Test', 'Accepted'),
                ('Safety & Restraint System Check', 'Accepted'),
                ('Electrical System Diagnostic', 'Accepted'),
                ('Paint & Finish Quality Check', 'Accepted'),
                ('Road Handling & Suspension Test', 'Accepted')
            ]
        },
        {
            'item': 'Orbis X1 SUV',
            'status': 'Accepted',
            'ref_type': 'Stock Entry',
            'ref_name': created_ste.get('Orbis X1 SUV', frappe._dict(name='MAT-STE-2026-00005')).name,
            'remarks': 'AWD drivetrain, suspension, structural integrity, and brake balance verified PASSED.',
            'readings': [
                ('Engine Performance Check', 'Accepted'),
                ('Brake Force & Response Test', 'Accepted'),
                ('Safety & Restraint System Check', 'Accepted'),
                ('Electrical System Diagnostic', 'Accepted'),
                ('Paint & Finish Quality Check', 'Accepted'),
                ('Road Handling & Suspension Test', 'Accepted')
            ]
        },
        {
            'item': 'Orbis E1 Electric',
            'status': 'Rejected',
            'ref_type': 'Stock Entry',
            'ref_name': created_ste.get('Orbis E1 Electric', frappe._dict(name='MAT-STE-2026-00006')).name,
            'remarks': 'Electrical system issue detected: High voltage BMS communication timeout on bus 2. Quarantined in Quality Hold Warehouse for rework.',
            'readings': [
                ('Brake Force & Response Test', 'Accepted'),
                ('Safety & Restraint System Check', 'Accepted'),
                ('Electrical System Diagnostic', 'Rejected'),
                ('Paint & Finish Quality Check', 'Accepted'),
                ('Road Handling & Suspension Test', 'Accepted')
            ]
        }
    ]

    for q in qi_records:
        if not frappe.db.exists('Quality Inspection', {'item_code': q['item'], 'status': q['status']}):
            qi = frappe.new_doc('Quality Inspection')
            qi.report_date = today
            qi.inspection_type = 'In Process'
            qi.reference_type = q['ref_type']
            qi.reference_name = q['ref_name']
            qi.item_code = q['item']
            qi.sample_size = 1
            qi.inspected_by = 'forw8007+qualitymanager@gmail.com'
            qi.status = q['status']
            qi.remarks = q['remarks']

            for spec, spec_status in q['readings']:
                qi.append('readings', {
                    'specification': spec,
                    'status': spec_status,
                    'manual_inspection': 1,
                    'numeric': 0,
                    'reading_value': 'Pass' if spec_status == 'Accepted' else 'Fail - BMS Error'
                })

            qi.insert(ignore_permissions=True)
            qi.submit()
            print(f"Created & Submitted Quality Inspection: {qi.name} for {q['item']} ({q['status']})")

    # Transfer quarantined EV materials into Quality Hold Warehouse
    if not frappe.db.exists('Stock Entry', {'purpose': 'Material Transfer', 'to_warehouse': quality_wh, 'company': COMPANY}):
        se_quarantine = frappe.new_doc('Stock Entry')
        se_quarantine.purpose = 'Material Transfer'
        se_quarantine.stock_entry_type = 'Material Transfer'
        se_quarantine.company = COMPANY
        se_quarantine.posting_date = today
        se_quarantine.remarks = 'Quarantined Orbis E1 Electric components to Quality Hold Warehouse due to Electrical System Issue'
        se_quarantine.append('items', {
            'item_code': 'EV Body Assembly',
            'qty': 1,
            's_warehouse': wip_wh,
            't_warehouse': quality_wh,
            'uom': 'Nos',
            'stock_uom': 'Nos',
            'conversion_factor': 1
        })
        se_quarantine.append('items', {
            'item_code': 'Battery Management System',
            'qty': 1,
            's_warehouse': wip_wh,
            't_warehouse': quality_wh,
            'uom': 'Nos',
            'stock_uom': 'Nos',
            'conversion_factor': 1
        })
        se_quarantine.insert(ignore_permissions=True)
        se_quarantine.submit()
        print(f'Transferred quarantined components to Quality Hold Warehouse: {se_quarantine.name}')

    # 6. Sales Cycle & Deliveries
    # Order 1: Ahmed Motors -> 2 x Orbis O1 Sedan, 1 x Orbis X1 SUV
    # Order 2: Lahore Motors -> 1 x Orbis X1 SUV

    # Quotation 1 for Ahmed Motors
    if not frappe.db.exists('Quotation', {'party_name': 'Ahmed Motors', 'company': COMPANY}):
        quo1 = frappe.new_doc('Quotation')
        quo1.quotation_to = 'Customer'
        quo1.party_name = 'Ahmed Motors'
        quo1.company = COMPANY
        quo1.transaction_date = today
        quo1.valid_till = add_days(today, 30)
        quo1.currency = CURRENCY
        quo1.order_type = 'Sales'

        quo1.append('items', {
            'item_code': 'Orbis O1 Sedan',
            'qty': 2,
            'rate': 6500000,
            'warehouse': fg_wh
        })
        quo1.append('items', {
            'item_code': 'Orbis X1 SUV',
            'qty': 1,
            'rate': 11500000,
            'warehouse': fg_wh
        })
        quo1.insert(ignore_permissions=True)
        quo1.submit()
        print(f'Created & Submitted Quotation: {quo1.name} for Ahmed Motors')

        # Sales Order 1
        so1 = frappe.new_doc('Sales Order')
        so1.customer = 'Ahmed Motors'
        so1.company = COMPANY
        so1.transaction_date = today
        so1.delivery_date = add_days(today, 3)
        so1.currency = CURRENCY
        so1.order_type = 'Sales'

        for q_item in quo1.items:
            so1.append('items', {
                'item_code': q_item.item_code,
                'qty': q_item.qty,
                'rate': q_item.rate,
                'warehouse': fg_wh,
                'quotation': quo1.name,
                'quotation_item': q_item.name
            })
        so1.insert(ignore_permissions=True)
        so1.submit()
        print(f'Created & Submitted Sales Order: {so1.name} (PKR {so1.grand_total:,})')

        # Delivery Note 1: Deliver 2 x Orbis O1 Sedan to Ahmed Motors
        dn1 = frappe.new_doc('Delivery Note')
        dn1.customer = 'Ahmed Motors'
        dn1.company = COMPANY
        dn1.posting_date = today
        dn1.currency = CURRENCY

        so_o1_item = [it for it in so1.items if it.item_code == 'Orbis O1 Sedan'][0]
        dn1.append('items', {
            'item_code': 'Orbis O1 Sedan',
            'qty': 2,
            'rate': 6500000,
            'warehouse': fg_wh,
            'against_sales_order': so1.name,
            'so_detail': so_o1_item.name,
            'expense_account': f'Cost of Goods Sold - {ABBR}',
            'cost_center': f'Main - {ABBR}'
        })
        dn1.insert(ignore_permissions=True)
        dn1.submit()
        print(f'Created & Submitted Delivery Note: {dn1.name} (2 x Orbis O1 Sedan to Ahmed Motors)')

        # Sales Invoice 1 for delivered cars
        si1 = frappe.new_doc('Sales Invoice')
        si1.customer = 'Ahmed Motors'
        si1.company = COMPANY
        si1.posting_date = today
        si1.due_date = add_days(today, 15)
        si1.currency = CURRENCY
        si1.debit_to = f'Debtors - {ABBR}'

        for dn_item in dn1.items:
            si1.append('items', {
                'item_code': dn_item.item_code,
                'qty': dn_item.qty,
                'rate': dn_item.rate,
                'warehouse': fg_wh,
                'delivery_note': dn1.name,
                'dn_detail': dn_item.name,
                'sales_order': so1.name,
                'so_detail': dn_item.so_detail,
                'income_account': f'Sales - {ABBR}',
                'cost_center': f'Main - {ABBR}'
            })
        si1.insert(ignore_permissions=True)
        si1.submit()
        print(f'Created & Submitted Sales Invoice: {si1.name} (PKR {si1.grand_total:,})')

        # Payment Entry 1 from Ahmed Motors
        pe1 = frappe.new_doc('Payment Entry')
        pe1.payment_type = 'Receive'
        pe1.party_type = 'Customer'
        pe1.party = 'Ahmed Motors'
        pe1.company = COMPANY
        pe1.posting_date = today
        pe1.paid_from = f'Debtors - {ABBR}'
        pe1.paid_to = bank_acc_name
        pe1.paid_amount = si1.grand_total
        pe1.received_amount = si1.grand_total
        pe1.reference_no = f'CHEQUE-AHMED-{so1.name}'
        pe1.reference_date = today

        pe1.append('references', {
            'reference_doctype': 'Sales Invoice',
            'reference_name': si1.name,
            'total_amount': si1.grand_total,
            'outstanding_amount': si1.grand_total,
            'allocated_amount': si1.grand_total
        })
        pe1.insert(ignore_permissions=True)
        pe1.submit()
        print(f'Created & Submitted Payment Entry: {pe1.name} from Ahmed Motors (PKR {pe1.paid_amount:,})')

    # Quotation 2 & Sales Order 2 for Lahore Motors (1 x Orbis X1 SUV)
    if not frappe.db.exists('Sales Order', {'customer': 'Lahore Motors', 'company': COMPANY}):
        so2 = frappe.new_doc('Sales Order')
        so2.customer = 'Lahore Motors'
        so2.company = COMPANY
        so2.transaction_date = today
        so2.delivery_date = add_days(today, 2)
        so2.currency = CURRENCY
        so2.order_type = 'Sales'

        so2.append('items', {
            'item_code': 'Orbis X1 SUV',
            'qty': 1,
            'rate': 11500000,
            'warehouse': fg_wh
        })
        so2.insert(ignore_permissions=True)
        so2.submit()
        print(f'Created & Submitted Sales Order: {so2.name} for Lahore Motors')

        # Delivery Note 2: Deliver 1 x Orbis X1 SUV
        dn2 = frappe.new_doc('Delivery Note')
        dn2.customer = 'Lahore Motors'
        dn2.company = COMPANY
        dn2.posting_date = today
        dn2.currency = CURRENCY

        so2_item = so2.items[0]
        dn2.append('items', {
            'item_code': 'Orbis X1 SUV',
            'qty': 1,
            'rate': 11500000,
            'warehouse': fg_wh,
            'against_sales_order': so2.name,
            'so_detail': so2_item.name,
            'expense_account': f'Cost of Goods Sold - {ABBR}',
            'cost_center': f'Main - {ABBR}'
        })
        dn2.insert(ignore_permissions=True)
        dn2.submit()
        print(f'Created & Submitted Delivery Note: {dn2.name} (1 x Orbis X1 SUV to Lahore Motors)')

        # Sales Invoice 2
        si2 = frappe.new_doc('Sales Invoice')
        si2.customer = 'Lahore Motors'
        si2.company = COMPANY
        si2.posting_date = today
        si2.due_date = add_days(today, 15)
        si2.currency = CURRENCY
        si2.debit_to = f'Debtors - {ABBR}'

        dn2_item = dn2.items[0]
        si2.append('items', {
            'item_code': dn2_item.item_code,
            'qty': dn2_item.qty,
            'rate': dn2_item.rate,
            'warehouse': fg_wh,
            'delivery_note': dn2.name,
            'dn_detail': dn2_item.name,
            'sales_order': so2.name,
            'so_detail': dn2_item.so_detail,
            'income_account': f'Sales - {ABBR}',
            'cost_center': f'Main - {ABBR}'
        })
        si2.insert(ignore_permissions=True)
        si2.submit()
        print(f'Created & Submitted Sales Invoice: {si2.name} (PKR {si2.grand_total:,})')

        # Payment Entry 2 from Lahore Motors
        pe2 = frappe.new_doc('Payment Entry')
        pe2.payment_type = 'Receive'
        pe2.party_type = 'Customer'
        pe2.party = 'Lahore Motors'
        pe2.company = COMPANY
        pe2.posting_date = today
        pe2.paid_from = f'Debtors - {ABBR}'
        pe2.paid_to = bank_acc_name
        pe2.paid_amount = si2.grand_total
        pe2.received_amount = si2.grand_total
        pe2.reference_no = f'ONLINE-LHR-{so2.name}'
        pe2.reference_date = today

        pe2.append('references', {
            'reference_doctype': 'Sales Invoice',
            'reference_name': si2.name,
            'total_amount': si2.grand_total,
            'outstanding_amount': si2.grand_total,
            'allocated_amount': si2.grand_total
        })
        pe2.insert(ignore_permissions=True)
        pe2.submit()
        print(f'Created & Submitted Payment Entry: {pe2.name} from Lahore Motors (PKR {pe2.paid_amount:,})')

    frappe.db.commit()
    print('--- Step 3 Finished Successfully! ---')
    return 'Step 3 Complete'
