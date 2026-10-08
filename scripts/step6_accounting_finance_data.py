import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

COMPANY = 'Orbis Car Manufacturing (Pvt.) Ltd.'
ABBR = 'OCM'
CURRENCY = 'PKR'

def run():
    frappe.set_user('Administrator')
    print('====================================================================')
    print('   STEP 6: DETAILED ACCOUNTING & FINANCE DEMO DATA SETUP             ')
    print('====================================================================\n')

    # -------------------------------------------------------------------------
    # 1. PREREQUISITES: ITEM & MASTER VERIFICATION
    # -------------------------------------------------------------------------
    print('--- 1. Ensuring Items & Masters for Accounting Transactions ---')
    if not frappe.db.exists('Item', 'Tyres'):
        tyre_item = frappe.new_doc('Item')
        tyre_item.item_code = 'Tyres'
        tyre_item.item_name = 'Prime Automobile Tyres'
        tyre_item.item_group = 'Rubber Components'
        tyre_item.stock_uom = 'Nos'
        tyre_item.is_stock_item = 1
        tyre_item.valuation_rate = 18000
        tyre_item.default_warehouse = f'Components Warehouse - {ABBR}'
        tyre_item.insert(ignore_permissions=True)
        print('Created Item: Tyres')

        # Add price in standard buying
        if not frappe.db.exists('Item Price', {'item_code': 'Tyres', 'price_list': 'Standard Buying'}):
            ip = frappe.new_doc('Item Price')
            ip.item_code = 'Tyres'
            ip.price_list = 'Standard Buying'
            ip.price_list_rate = 18000
            ip.currency = CURRENCY
            ip.insert(ignore_permissions=True)
    else:
        print('Item exists: Tyres')

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 2. SALES INVOICES (Section 44)
    # -------------------------------------------------------------------------
    print('\n--- 2. Creating Connected Sales Invoices ---')
    sales_invoices_config = [
        {
            'key': 'SINV-AHMED-MOTORS',
            'customer': 'Ahmed Motors',
            'posting_date': '2026-10-02',
            'items': [
                ('Orbis O1 Sedan', 2, 6500000),
                ('Orbis X1 SUV', 1, 11500000)
            ],
            'expected_status': 'Partially Paid',
            'partial_pay_amount': 18665000.0  # Leaves 10,000,000 outstanding (24.5M + 17% tax = 28.665M)
        },
        {
            'key': 'SINV-LAHORE-MOTORS',
            'customer': 'Lahore Motors',
            'posting_date': '2026-10-03',
            'items': [
                ('Orbis X1 SUV', 2, 11500000)
            ],
            'expected_status': 'Paid',
            'partial_pay_amount': None  # Full payment
        },
        {
            'key': 'SINV-ISLAMABAD-AG',
            'customer': 'Islamabad Auto Gallery',
            'posting_date': '2026-10-04',
            'items': [
                ('Orbis E1 Electric', 1, 14000000)
            ],
            'expected_status': 'Unpaid',
            'partial_pay_amount': 0  # Unpaid
        }
    ]

    created_sales_invoices = {}

    for cfg in sales_invoices_config:
        cust = cfg['customer']
        # Check if a matching sales invoice already exists for this customer and item combination
        existing_sinv = None
        candidates = frappe.get_all('Sales Invoice', filters={'company': COMPANY, 'customer': cust, 'docstatus': 1}, fields=['name'])
        for cand in candidates:
            doc = frappe.get_doc('Sales Invoice', cand.name)
            doc_items = [(it.item_code, int(it.qty)) for it in doc.items]
            cfg_items = [(it[0], it[1]) for it in cfg['items']]
            if doc_items == cfg_items:
                existing_sinv = doc
                break

        if not existing_sinv:
            sinv = frappe.new_doc('Sales Invoice')
            sinv.customer = cust
            sinv.company = COMPANY
            sinv.posting_date = cfg['posting_date']
            sinv.due_date = '2026-11-04'
            sinv.currency = CURRENCY
            sinv.debit_to = f'Debtors - {ABBR}'
            sinv.taxes_and_charges = f'Pakistan Tax - {ABBR}'

            for item_code, qty, rate in cfg['items']:
                sinv.append('items', {
                    'item_code': item_code,
                    'qty': qty,
                    'rate': rate,
                    'income_account': f'Sales - {ABBR}',
                    'cost_center': f'Main - {ABBR}'
                })

            sinv.set_taxes()
            sinv.insert(ignore_permissions=True)
            sinv.submit()
            print(f'Created & Submitted Sales Invoice: {sinv.name} for {cust} (Total: PKR {sinv.grand_total:,.2f})')
            created_sales_invoices[cfg['key']] = sinv
        else:
            print(f'Sales Invoice exists: {existing_sinv.name} for {cust}')
            created_sales_invoices[cfg['key']] = existing_sinv

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 3. PURCHASE INVOICES (Section 44)
    # -------------------------------------------------------------------------
    print('\n--- 3. Creating Connected Purchase Invoices ---')
    purchase_invoices_config = [
        {
            'key': 'PINV-PAK-STEEL',
            'supplier': 'Pakistan Steel Suppliers',
            'posting_date': '2026-10-02',
            'items': [
                ('Steel Sheet', 500, 15000)
            ],
            'expected_status': 'Paid',
            'partial_pay_amount': None  # Full payment
        },
        {
            'key': 'PINV-PRIME-TYRES',
            'supplier': 'Prime Tyres Pakistan',
            'posting_date': '2026-10-03',
            'items': [
                ('Tyres', 200, 18000)
            ],
            'expected_status': 'Partially Paid',
            'partial_pay_amount': 2212000.0  # Leaves 2,000,000 outstanding (3.6M + 17% tax = 4.212M)
        },
        {
            'key': 'PINV-NATIONAL-GLASS',
            'supplier': 'National Glass Components',
            'posting_date': '2026-10-04',
            'items': [
                ('Windshield Glass', 100, 25000)
            ],
            'expected_status': 'Unpaid',
            'partial_pay_amount': 0  # Unpaid
        }
    ]

    created_purchase_invoices = {}

    for cfg in purchase_invoices_config:
        supp = cfg['supplier']
        existing_pinv = None
        candidates = frappe.get_all('Purchase Invoice', filters={'company': COMPANY, 'supplier': supp, 'docstatus': 1}, fields=['name'])
        for cand in candidates:
            doc = frappe.get_doc('Purchase Invoice', cand.name)
            doc_items = [(it.item_code, int(it.qty)) for it in doc.items]
            cfg_items = [(it[0], it[1]) for it in cfg['items']]
            if doc_items == cfg_items:
                existing_pinv = doc
                break

        if not existing_pinv:
            pinv = frappe.new_doc('Purchase Invoice')
            pinv.supplier = supp
            pinv.company = COMPANY
            pinv.posting_date = cfg['posting_date']
            pinv.due_date = '2026-11-04'
            pinv.currency = CURRENCY
            pinv.credit_to = f'Creditors - {ABBR}'
            pinv.taxes_and_charges = f'Pakistan Tax - {ABBR}'

            for item_code, qty, rate in cfg['items']:
                pinv.append('items', {
                    'item_code': item_code,
                    'qty': qty,
                    'rate': rate,
                    'expense_account': f'Cost of Goods Sold - {ABBR}',
                    'cost_center': f'Main - {ABBR}'
                })

            pinv.set_taxes()
            pinv.insert(ignore_permissions=True)
            pinv.submit()
            print(f'Created & Submitted Purchase Invoice: {pinv.name} for {supp} (Total: PKR {pinv.grand_total:,.2f})')
            created_purchase_invoices[cfg['key']] = pinv
        else:
            print(f'Purchase Invoice exists: {existing_pinv.name} for {supp}')
            created_purchase_invoices[cfg['key']] = existing_pinv

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 4. PAYMENT ENTRIES (Section 44)
    # -------------------------------------------------------------------------
    print('\n--- 4. Creating Connected Payment Entries ---')

    # 4.1 Customer Payment 1: Partial payment for Sales Invoice 1 (Ahmed Motors)
    sinv1 = created_sales_invoices.get('SINV-AHMED-MOTORS')
    if sinv1 and sinv1.outstanding_amount > 10000000:
        pay_amt = 18665000.0
        pe1 = get_payment_entry('Sales Invoice', sinv1.name, party_amount=pay_amt)
        pe1.posting_date = '2026-10-04'
        pe1.reference_no = f'PAY-REC-AHMED-001'
        pe1.reference_date = '2026-10-04'
        pe1.insert(ignore_permissions=True)
        pe1.submit()
        print(f'Created & Submitted Customer Payment 1: {pe1.name} (PKR {pay_amt:,.2f}) -> Ahmed Motors Partial')

    # 4.2 Customer Payment 2: Full payment for Sales Invoice 2 (Lahore Motors)
    sinv2 = created_sales_invoices.get('SINV-LAHORE-MOTORS')
    if sinv2 and sinv2.outstanding_amount > 0:
        pay_amt = sinv2.outstanding_amount
        pe2 = get_payment_entry('Sales Invoice', sinv2.name, party_amount=pay_amt)
        pe2.posting_date = '2026-10-04'
        pe2.reference_no = f'PAY-REC-LAHORE-001'
        pe2.reference_date = '2026-10-04'
        pe2.insert(ignore_permissions=True)
        pe2.submit()
        print(f'Created & Submitted Customer Payment 2: {pe2.name} (PKR {pay_amt:,.2f}) -> Lahore Motors Full')

    # 4.3 Supplier Payment 1: Full payment for Purchase Invoice 1 (Pakistan Steel)
    pinv1 = created_purchase_invoices.get('PINV-PAK-STEEL')
    if pinv1 and pinv1.outstanding_amount > 0:
        pay_amt = pinv1.outstanding_amount
        spe1 = get_payment_entry('Purchase Invoice', pinv1.name, party_amount=pay_amt)
        spe1.posting_date = '2026-10-04'
        spe1.reference_no = f'PAY-SUPP-STEEL-001'
        spe1.reference_date = '2026-10-04'
        spe1.insert(ignore_permissions=True)
        spe1.submit()
        print(f'Created & Submitted Supplier Payment 1: {spe1.name} (PKR {pay_amt:,.2f}) -> Pak Steel Full')

    # 4.4 Supplier Payment 2: Partial payment for Purchase Invoice 2 (Prime Tyres)
    pinv2 = created_purchase_invoices.get('PINV-PRIME-TYRES')
    if pinv2 and pinv2.outstanding_amount > 2000000:
        pay_amt = 2212000.0
        spe2 = get_payment_entry('Purchase Invoice', pinv2.name, party_amount=pay_amt)
        spe2.posting_date = '2026-10-04'
        spe2.reference_no = f'PAY-SUPP-TYRES-001'
        spe2.reference_date = '2026-10-04'
        spe2.insert(ignore_permissions=True)
        spe2.submit()
        print(f'Created & Submitted Supplier Payment 2: {spe2.name} (PKR {pay_amt:,.2f}) -> Prime Tyres Partial')

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 5. JOURNAL ENTRIES (Section 44)
    # -------------------------------------------------------------------------
    print('\n--- 5. Creating Realistic OCM Journal Entries ---')
    bank_account = frappe.db.get_value('Account', {'company': COMPANY, 'account_type': 'Bank'}, 'name')

    capital_stock_acc = f'Capital Stock - {ABBR}'
    journal_entries_config = [
        {
            'voucher_type': 'Bank Entry',
            'posting_date': '2026-10-01',
            'cheque_no': 'CHQ-CAP-2026-000',
            'debit_account': bank_account,
            'credit_account': capital_stock_acc,
            'amount': 150000000,
            'remark': 'Initial paid-up shareholder equity capital injection into Habib Bank Limited for OCM automotive plant'
        },
        {
            'voucher_type': 'Bank Entry',
            'posting_date': '2026-10-03',
            'cheque_no': 'CHQ-ELEC-2026-001',
            'debit_account': f'Utility Expenses - {ABBR}',
            'credit_account': bank_account,
            'amount': 550000,
            'remark': 'Factory electricity bill payment to K-Electric for production assembly lines'
        },
        {
            'voucher_type': 'Bank Entry',
            'posting_date': '2026-10-03',
            'cheque_no': 'CHQ-MAINT-2026-002',
            'debit_account': f'Office Maintenance Expenses - {ABBR}',
            'credit_account': bank_account,
            'amount': 320000,
            'remark': 'Routine preventative maintenance and servicing of robotic welding and paint shop equipment'
        },
        {
            'voucher_type': 'Bank Entry',
            'posting_date': '2026-10-04',
            'cheque_no': 'CHQ-ADMIN-2026-003',
            'debit_account': f'Administrative Expenses - {ABBR}',
            'credit_account': bank_account,
            'amount': 180000,
            'remark': 'Head office IT software licenses and administrative supplies'
        },
        {
            'voucher_type': 'Bank Entry',
            'posting_date': '2026-10-04',
            'cheque_no': 'CHQ-PROD-2026-004',
            'debit_account': f'Stock Adjustment - {ABBR}',
            'credit_account': bank_account,
            'amount': 140000,
            'remark': 'Factory floor consumable tooling adjustment for pilot production run'
        }
    ]

    for jc in journal_entries_config:
        rem = jc['remark']
        if not frappe.db.exists('Journal Entry', {'company': COMPANY, 'user_remark': rem, 'docstatus': 1}):
            je = frappe.new_doc('Journal Entry')
            je.company = COMPANY
            je.voucher_type = jc['voucher_type']
            je.posting_date = jc['posting_date']
            je.cheque_no = jc['cheque_no']
            je.cheque_date = jc['posting_date']
            je.user_remark = rem
            je.append('accounts', {
                'account': jc['debit_account'],
                'debit_in_account_currency': jc['amount'],
                'credit_in_account_currency': 0,
                'cost_center': f'Main - {ABBR}'
            })
            je.append('accounts', {
                'account': jc['credit_account'],
                'debit_in_account_currency': 0,
                'credit_in_account_currency': jc['amount'],
                'cost_center': f'Main - {ABBR}' if 'Expenses' in jc['credit_account'] else None
            })
            je.insert(ignore_permissions=True)
            je.submit()
            print(f'Created & Submitted Journal Entry: {je.name} -> {jc["debit_account"]} (PKR {jc["amount"]:,})')
        else:
            print(f'Journal Entry exists: {rem[:45]}...')

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 6. ANNUAL BUDGET DEMO DATA (Section 44)
    # -------------------------------------------------------------------------
    print('\n--- 6. Configuring OCM Annual Budget ---')
    budget_accounts_config = [
        (f'Cost of Goods Sold - {ABBR}', 150000000),  # Raw Materials & Manufacturing
        (f'Utility Expenses - {ABBR}', 12000000),     # Factory Electricity
        (f'Office Maintenance Expenses - {ABBR}', 8000000), # Factory Maintenance
        (f'Administrative Expenses - {ABBR}', 6000000),    # Administration
        (f'Marketing Expenses - {ABBR}', 5000000),         # Marketing & Sales
        (f'Travel Expenses - {ABBR}', 4000000)             # Logistics & Distribution
    ]

    for acc_name, b_amt in budget_accounts_config:
        existing_b = frappe.db.get_value('Budget', {'company': COMPANY, 'account': acc_name, 'from_fiscal_year': '2026-2027'}, 'name')
        if not existing_b:
            b = frappe.new_doc('Budget')
            b.budget_against = 'Cost Center'
            b.company = COMPANY
            b.cost_center = f'Main - {ABBR}'
            b.account = acc_name
            b.from_fiscal_year = '2026-2027'
            b.to_fiscal_year = '2026-2027'
            b.distribution_frequency = 'Monthly'
            b.budget_amount = b_amt
            b.distribute_equally = 1
            b.insert(ignore_permissions=True)
            print(f'Created Budget: {b.name} for {acc_name} (Annual: PKR {b_amt:,.2f})')
        else:
            print(f'Budget exists: {existing_b} for {acc_name}')

    frappe.db.commit()

    # -------------------------------------------------------------------------
    # 7. FINANCIAL REPORT DATA VERIFICATION
    # -------------------------------------------------------------------------
    print('\n====================================================================')
    print('   --- 7. FINANCIAL REPORTS DATA VERIFICATION ---                    ')
    print('====================================================================')

    # 1. General Ledger
    gl_count = frappe.db.count('GL Entry', {'company': COMPANY})
    print(f'[✓] General Ledger: {gl_count} GL Entries recorded -> ACTIVE')

    # 2. Accounts Receivable
    total_receivable = frappe.db.sql("""
        SELECT SUM(outstanding_amount) as total FROM `tabSales Invoice`
        WHERE company = %s AND docstatus = 1
    """, (COMPANY,), as_dict=True)[0].total or 0.0
    print(f'[✓] Accounts Receivable: PKR {total_receivable:,.2f} outstanding -> ACTIVE')

    # 3. Accounts Payable
    total_payable = frappe.db.sql("""
        SELECT SUM(outstanding_amount) as total FROM `tabPurchase Invoice`
        WHERE company = %s AND docstatus = 1
    """, (COMPANY,), as_dict=True)[0].total or 0.0
    print(f'[✓] Accounts Payable: PKR {total_payable:,.2f} outstanding -> ACTIVE')

    # 4. Trial Balance (Debit == Credit balance check)
    tb_totals = frappe.db.sql("""
        SELECT SUM(debit) as debits, SUM(credit) as credits FROM `tabGL Entry`
        WHERE company = %s
    """, (COMPANY,), as_dict=True)[0]
    total_debits = tb_totals.debits or 0.0
    total_credits = tb_totals.credits or 0.0
    diff = abs(total_debits - total_credits)
    tb_status = 'BALANCED' if diff < 0.01 else 'UNBALANCED'
    print(f'[✓] Trial Balance: Debits = PKR {total_debits:,.2f} | Credits = PKR {total_credits:,.2f} -> {tb_status}')

    # 5. Profit and Loss
    income_total = frappe.db.sql("""
        SELECT SUM(credit - debit) as net_income FROM `tabGL Entry` gl
        JOIN `tabAccount` acc ON gl.account = acc.name
        WHERE gl.company = %s AND acc.root_type = 'Income'
    """, (COMPANY,), as_dict=True)[0].net_income or 0.0

    expense_total = frappe.db.sql("""
        SELECT SUM(debit - credit) as net_expense FROM `tabGL Entry` gl
        JOIN `tabAccount` acc ON gl.account = acc.name
        WHERE gl.company = %s AND acc.root_type = 'Expense'
    """, (COMPANY,), as_dict=True)[0].net_expense or 0.0

    net_profit = income_total - expense_total
    print(f'[✓] Profit & Loss: Revenue = PKR {income_total:,.2f} | Expenses = PKR {expense_total:,.2f} | Net Profit = PKR {net_profit:,.2f} -> ACTIVE')

    # 6. Balance Sheet
    asset_total = frappe.db.sql("""
        SELECT SUM(debit - credit) as net_asset FROM `tabGL Entry` gl
        JOIN `tabAccount` acc ON gl.account = acc.name
        WHERE gl.company = %s AND acc.root_type = 'Asset'
    """, (COMPANY,), as_dict=True)[0].net_asset or 0.0

    liab_total = frappe.db.sql("""
        SELECT SUM(credit - debit) as net_liab FROM `tabGL Entry` gl
        JOIN `tabAccount` acc ON gl.account = acc.name
        WHERE gl.company = %s AND acc.root_type = 'Liability'
    """, (COMPANY,), as_dict=True)[0].net_liab or 0.0
    print(f'[✓] Balance Sheet: Assets = PKR {asset_total:,.2f} | Liabilities = PKR {liab_total:,.2f} -> ACTIVE')

    # 7. Cash Flow (Bank Movements)
    bank_balance = frappe.db.sql("""
        SELECT SUM(debit - credit) as balance FROM `tabGL Entry`
        WHERE company = %s AND account = %s
    """, (COMPANY, bank_account), as_dict=True)[0].balance or 0.0
    print(f'[✓] Cash Flow / Bank Account: {bank_account} Balance = PKR {bank_balance:,.2f} -> ACTIVE')

    # 8. Sales Register
    sales_invoices_count = frappe.db.count('Sales Invoice', {'company': COMPANY, 'docstatus': 1})
    print(f'[✓] Sales Register: {sales_invoices_count} submitted Sales Invoices -> ACTIVE')

    # 9. Purchase Register
    purchase_invoices_count = frappe.db.count('Purchase Invoice', {'company': COMPANY, 'docstatus': 1})
    print(f'[✓] Purchase Register: {purchase_invoices_count} submitted Purchase Invoices -> ACTIVE')

    print('====================================================================')
    print('--- Step 6 Finished Successfully! ---')

    return {
        'gl_entries': gl_count,
        'sales_invoices': sales_invoices_count,
        'purchase_invoices': purchase_invoices_count,
        'customer_payments': frappe.db.count('Payment Entry', {'company': COMPANY, 'payment_type': 'Receive', 'docstatus': 1}),
        'supplier_payments': frappe.db.count('Payment Entry', {'company': COMPANY, 'payment_type': 'Pay', 'docstatus': 1}),
        'journal_entries': frappe.db.count('Journal Entry', {'company': COMPANY, 'docstatus': 1}),
        'budgets': frappe.db.count('Budget', {'company': COMPANY}),
        'trial_balance_status': tb_status
    }
