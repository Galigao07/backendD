from django.db import models
from rest_framework import serializers


class CompanySetup(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    ul_code = models.IntegerField(default=1)
    company_logo = models.CharField(max_length=1, default='')
    company_type = models.CharField(max_length=25, default=' ')
    company_name = models.CharField(max_length=100, default=' ')
    company_initials = models.CharField(max_length=10, default='')
    company_address = models.CharField(max_length=150, default=' ')
    company_TIN = models.CharField(max_length=20, default='000-000-000-0000')
    company_zipcode = models.CharField(max_length=4, default='0000')
    begin_date = models.CharField(max_length=20)
    system_date_created = models.DateTimeField(default='2010-01-01 00:00:00')
    createInventory = models.CharField(max_length=1, default='N')
    autocreate_bc = models.CharField(max_length=1, default='N')
    standPurch = models.CharField(max_length=1, default='N')
    showallitem = models.CharField(max_length=1, default='N')
    no_rs = models.CharField(max_length=1, default='Y')
    allowin = models.CharField(max_length=1, default='N')
    autoin = models.CharField(max_length=1, default='N')
    defaultfind = models.CharField(max_length=1, default='I')
    method = models.CharField(max_length=2, default='PT')
    alter_code = models.CharField(max_length=1, default='N')
    allow_dup = models.CharField(max_length=1, default='N')
    allow_SIproofList = models.CharField(max_length=1, default='N')
    allow_multiAR = models.CharField(max_length=1, default='N')
    allow_UOMSum = models.CharField(max_length=1, default='N')
    allowCreatingCustomer = models.CharField(max_length=1, default='N')
    with_salesagent = models.CharField(max_length=1, default='Y')
    tagging_per_product = models.CharField(max_length=1, default='N')
    tagging_postprint = models.CharField(max_length=1, default='N')
    allowInvoiceCreation = models.CharField(max_length=1, default='N')
    allowStockTransferCreation = models.CharField(max_length=1, default='N')
    allowRRCreation = models.CharField(max_length=1, default='N')
    withVirtualSet = models.CharField(max_length=1, default='N')
    allow_custom_name = models.CharField(max_length=1, default='N')
    withConcessionare = models.CharField(max_length=1, default='N')
    allowFixingVAT = models.CharField(max_length=1, default='N')
    collectionOR = models.CharField(max_length=1, default='N')
    hide_ProofList = models.CharField(max_length=1, default='D')
    doc_type = models.CharField(max_length=1, default='N')
    unadj_sl = models.CharField(max_length=1, default='N')
    per_ul = models.CharField(max_length=1, default='N')
    business_unit = models.CharField(max_length=15, default='')
    per_logo = models.CharField(max_length=1, default='N')
    multipleTaxCustomer = models.CharField(max_length=1, default='N')
    AllowDRSI = models.CharField(max_length=1, default='N')
    auto_wht = models.CharField(max_length=1, default='N')
    auto_tax = models.CharField(max_length=1, default='N')
    sys_expire = models.CharField(max_length=1, default='')
    principal = models.CharField(max_length=1, default='N')
    inv_type = models.CharField(max_length=25, default='')
    cat_sales = models.CharField(max_length=1, default='N')
    comm_rep = models.CharField(max_length=1, default='N')
    nopo = models.CharField(max_length=1, default='N')
    rr_cost = models.CharField(max_length=1, default='N')
    inv_dup = models.CharField(max_length=1, default='N')
    edit_sell = models.CharField(max_length=1, default='N')
    with_journal = models.CharField(max_length=1, default='Y')
    with_delivered = models.CharField(max_length=1, default='N')
    with_POS_sales = models.CharField(max_length=1, default='N')
    banking = models.CharField(max_length=1, default='N')
    supp_rel = models.CharField(max_length=1, default='N')
    docpersite = models.CharField(max_length=1, default='N')
    zero_qty = models.CharField(max_length=1, default='Y')
    qty_cons_stock_ledger = models.CharField(max_length=1, default='N')
    qty_cons_pending_out = models.CharField(max_length=1, default='N')
    qty_cons_pending_request = models.CharField(max_length=1, default='N')
    qty_cons_pending_sto_request = models.CharField(max_length=1, default='N')
    blank_site = models.CharField(max_length=1, default='N')
    cash_ref = models.CharField(max_length=1, default='N')
    auto_pn = models.CharField(max_length=1, default='N')
    sales_disc = models.CharField(max_length=1, default='N')
    Section = models.CharField(max_length=1, default='N')
    Multiplepricetype = models.CharField(max_length=1, default='N')
    MultipleDiscountType = models.CharField(max_length=1, default='N')
    update_cost = models.CharField(max_length=1, default='N')
    prodJobLot = models.CharField(max_length=1, default='N')
    ProdINSite = models.CharField(max_length=1, default='N')
    POCurrency = models.CharField(max_length=1, default='N')
    without_logo = models.TextField(blank=True)
    logo_img = models.BinaryField(blank=True, null=True)
    default_decimal = models.IntegerField(default=2)
    default_PO_Validity = models.IntegerField(default=0)
    doctypeno = models.IntegerField(default=10)
    noofbook = models.IntegerField(default=10)
    cv_app = models.CharField(max_length=1, default='N')
    jv_app = models.CharField(max_length=1, default='N')
    or_app = models.CharField(max_length=1, default='N')
    apvRep = models.CharField(max_length=1, default='N')
    cvRep = models.CharField(max_length=1, default='N')
    orRep = models.CharField(max_length=1, default='N')
    ciRep = models.CharField(max_length=1, default='N')
    jvRep = models.CharField(max_length=1, default='N')
    PrintbeforeSave = models.CharField(max_length=1, default='Y')
    allowBackup = models.CharField(max_length=1, default='N')
    customized_configuration = models.CharField(max_length=1, default='N')
    bill_sequence = models.CharField(max_length=1, default='N')
    req_DRSI = models.CharField(max_length=1, default='N')
    allow_child_count = models.CharField(max_length=1, default='N')
    allow_viewing_per_terminal = models.CharField(max_length=1, default='N')
    allow_delete_module = models.CharField(max_length=1, default='Y')
    allow_custom_sl = models.CharField(max_length=1, default='N')
    allow_block_aging = models.CharField(max_length=1, default='N')
    posted_aging_only = models.CharField(max_length=1, default='N')
    restrict_checkin = models.CharField(max_length=1, default='N')
    dont_show_event_class = models.CharField(max_length=1, default='N')
    sl_change = models.CharField(max_length=1, default='N')
    field_change = models.CharField(max_length=1, default='N')
    item_trade = models.CharField(max_length=1, default='N')
    po_specs = models.CharField(max_length=1, default='N')
    so_specs = models.CharField(max_length=1, default='N')
    po_trans_discount = models.CharField(max_length=1, default='N')
    allow_post_cash = models.CharField(max_length=1, default='N')
    show_issue_prod = models.CharField(max_length=1, default='N')
    allow_issue_prod = models.CharField(max_length=1, default='N')
    allow_transfer_price = models.CharField(max_length=1, default='N')
    witholding_period = models.CharField(max_length=15, default='2020-08-01')
    sortingAvail = models.CharField(max_length=1, default='1')
    allow_tagging_bank = models.CharField(max_length=1, default='N')
    allow_payee_alter = models.CharField(max_length=1, default='N')
    allow_breakdown = models.CharField(max_length=1, default='N')
    customexport = models.CharField(max_length=1, default='N')
    allow_pcfslip = models.CharField(max_length=1, default='N')
    allow_doctag = models.CharField(max_length=1, default='N')
    allowBookAccount = models.CharField(max_length=1, default='N')
    withhold_tax = models.CharField(max_length=1, default='N')
    activate_credit_limit = models.CharField(max_length=1, default='N')
    hide_overpayment = models.CharField(max_length=1, default='Y')
    allow_rr_remarks_wtax = models.CharField(max_length=1, default='N')
    allow_multiple_wtax = models.CharField(max_length=1, default='N')
    prodsearchdefault = models.CharField(max_length=1, default='N')
    allow_uom_conversion = models.CharField(max_length=50, default='')
    ONOFCustomer = models.CharField(max_length=1, default='Y')
    AllowSOTime = models.CharField(max_length=1, default='N')
    POPrint = models.CharField(max_length=1, default='N')
    allowOtherPaymentDoctype = models.CharField(max_length=1, default='N')
    hideSo = models.CharField(max_length=1, default='Y')
    CustomizeHeader = models.CharField(max_length=1, default='N')
    max_reference_no = models.IntegerField(default=10)
    SeriesCheck = models.CharField(max_length=1, default='N')
    accessRestriction = models.CharField(max_length=1, default='N')
    autoFillCheckWithRemarks = models.CharField(max_length=1, default='N')
    allowNegSO = models.CharField(max_length=1, default='N')
    allowproceedSO = models.CharField(max_length=1, default='N')
    restricted_site = models.CharField(max_length=1, default='N')
    OverideULChange = models.CharField(max_length=1, default='N')
    Category_CccRcc = models.CharField(max_length=1, default='N')
    OneDRSI = models.CharField(max_length=1, default='N')
    penalty_cut_off = models.DecimalField(max_digits=21, decimal_places=9, default=30.000000000)
    hidePR = models.CharField(max_length=1, default='N')
    showCVAmount = models.CharField(max_length=1, default='N')
    BackupEnable = models.CharField(max_length=1, default='N')
    sortEnabled = models.CharField(max_length=1, default='N')
    enableBeginBalance = models.CharField(max_length=1, default='N')
    AllowPostedTrans = models.CharField(max_length=1, default='N')
    enableOtherTrans = models.CharField(max_length=1, default='N')
    ShowHide = models.CharField(max_length=1, default='N')
    showRequestPaymentInd = models.CharField(max_length=1, default='Y')
    showRequestPaymentIntegrated = models.CharField(max_length=1, default='N')
    allowChangeDocumentName = models.CharField(max_length=1, default='N')
    allowDocTypePerModule = models.CharField(max_length=1, default='N')
    show_farm_supply = models.CharField(max_length=1, default='N')
    show_req_farm_supply = models.CharField(max_length=1, default='N')
    allowMultipleResp = models.CharField(max_length=1, default='N')
    AllowPOTransType = models.CharField(max_length=1, default='N')
    AllowSOTransType = models.CharField(max_length=1, default='N')
    AllowPRTransType = models.CharField(max_length=1, default='N')
    RequiredSitePO = models.CharField(max_length=1, default='N')
    POValidityDefaultorTrans = models.CharField(max_length=1, default='Y')
    allowConsoPO = models.CharField(max_length=1, default='N')
    hidePO_RSNO = models.CharField(max_length=1, default='Y')
    hidePOTradeDisc = models.CharField(max_length=1, default='Y')
    AllowPOMultiplePR = models.CharField(max_length=1, default='N')
    ChangePOShipto = models.CharField(max_length=150, default='')
    hideRRTrade = models.CharField(max_length=1, default='Y')
    hideRRSB = models.CharField(max_length=1, default='Y')
    hideRRAdj = models.CharField(max_length=1, default='Y')
    hideJPL = models.CharField(max_length=1, default='Y')
    bypass_Subparcela_PLine = models.CharField(max_length=1, default='N')
    bypass_Activity = models.CharField(max_length=1, default='N')
    HideSLTentative = models.CharField(max_length=1, default='N')
    AllowAutoSTR = models.CharField(max_length=1, default='N')
    restrictULSite = models.CharField(max_length=1, default='N')
    product_line_as_basis_of_SL = models.CharField(max_length=1, default='N')
    main_activity_as_basis_of_SL = models.CharField(max_length=1, default='Y')
    allowRoundingDiff = models.CharField(max_length=1, default='N')
    PayeeCanDeleteNotAdd = models.CharField(max_length=1, default='N')
    EnableMemberSL = models.CharField(max_length=1, default='N')
    showSLConso = models.CharField(max_length=1, default='N')
    NoLoginUL = models.CharField(max_length=1, default='N')
    allowPaymentTypeGL = models.CharField(max_length=1, default='')
    allowMultiplePrinting = models.CharField(max_length=1, default='N')
    RestrictPriceAmount = models.CharField(max_length=1, default='N')
    RestrictVATField = models.CharField(max_length=1, default='N')
    withtaxPO = models.CharField(max_length=1, default='N')
    enableExportSet = models.CharField(max_length=1, default='N')
    hide_pr_type = models.CharField(max_length=1, default='N')
    EnabledcustomerSOTerms = models.CharField(max_length=1, default='N')
    PurchaseRequestSLType = models.CharField(max_length=25, default='')
    RRrequiredDRSI = models.CharField(max_length=1, default='N')
    oneSTRtoOneSTO = models.CharField(max_length=1, default='N')
    oneRRperPO = models.CharField(max_length=1, default='N')
    SIRestrictTerms = models.CharField(max_length=1, default='N')
    SORestrictTerms = models.CharField(max_length=1, default='N')
    AutonumSorting = models.CharField(max_length=1, default='N')
    OneIRtoOneISS = models.CharField(max_length=1, default='N')
    AllowRRPopupinPO = models.CharField(max_length=1, default='N')
    RequiredRemarksRR = models.CharField(max_length=1, default='N')
    RequiredRemarksPO = models.CharField(max_length=1, default='N')
    RequiredRemarksPR = models.CharField(max_length=1, default='N')
    RequiredRemarksSTR = models.CharField(max_length=1, default='N')
    RequiredRemarksSIS = models.CharField(max_length=1, default='N')
    RequiredRemarksSIR = models.CharField(max_length=1, default='N')
    AllowSTRPopupinSTO = models.CharField(max_length=1, default='N')
    disableCostingSalesandReturn = models.CharField(max_length=1, default='N')
    VatSalesPurchases = models.CharField(max_length=1, default='N')
    withOnlinePOApprove = models.CharField(max_length=1, default='N')
    allowHideGeneralSL = models.CharField(max_length=1, default='')
    disablePrinting = models.CharField(max_length=1, default='Y')
    RRprintAPV = models.CharField(max_length=1, default='N')

    class Meta:
        db_table = 'tbl_company_setup'


class PosSalesTransSeniorCitizenDiscount(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    sales_trans_id = models.IntegerField(null=True, default=None)
    terminal_no = models.CharField(max_length=21, default='0')
    cashier_id = models.CharField(max_length=21, default='')
    document_type = models.CharField(max_length=10, default=' ')
    details_id = models.IntegerField(default=0)
    id_no = models.CharField(max_length=100, null=True, default=None)
    senior_member_name = models.CharField(max_length=500, null=True, default=None)
    id = models.IntegerField(default=0)
    tin_no = models.CharField(max_length=100, default='0')
    so_no = models.CharField(max_length=50, default=' ')

    class Meta:
        db_table = 'tbl_pos_sales_trans_senior_citizen_discount'

class ProductCategorySetup(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    category_code = models.PositiveSmallIntegerField(default=0)
    category_desc = models.CharField(max_length=150, default=' ')
    acct_code = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    acct_title = models.CharField(max_length=150, default=' ')
    acct_code2 = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    acct_title2 = models.CharField(max_length=150, default=' ')
    iitem_code = models.PositiveIntegerField(default=0)
    iitem_desc = models.CharField(max_length=45, default='')
    pos_category = models.CharField(max_length=2, default='N')

    class Meta:
        db_table = 'tbl_product_category_setup'

class PosExtended(models.Model):
    autonum = models.AutoField(primary_key=True)
    barcode = models.CharField(max_length=50, default='0')
    qty = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    description = models.CharField(max_length=225, default='')
    price = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    amount = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    line_no = models.IntegerField(default=0)
    serial_no = models.CharField(max_length=50, default='')
    table_no = models.IntegerField(default=0)
    que_no = models.IntegerField(default=0)
    order_type = models.CharField(max_length=20, default='')
    entry_type = models.CharField(max_length=225, default='')

    class Meta:
        db_table = 'tbl_pos_extended'

class PosClientSetup(models.Model):
    autonum = models.AutoField(primary_key=True)
    company_code = models.IntegerField(default=0)
    company_name = models.CharField(max_length=225, default='')
    company_name2 = models.CharField(max_length=225, default='')
    company_address = models.CharField(max_length=225, default='')
    company_address2 = models.CharField(max_length=225, default='', blank=True)
    company_address3 = models.CharField(max_length=225, default='', blank=True)
    tel_no = models.CharField(max_length=50, default='', blank=True)
    tin = models.CharField(max_length=50, default='', blank=True)
    remarks = models.CharField(max_length=225, default='', blank=True)
    remarks2 = models.CharField(max_length=225, default='', blank=True)
    remarks3 = models.CharField(max_length=225, default='', blank=True)

    class Meta:
        db_table = 'tbl_pos_client_setup'

class LeadSetup(models.Model):
    autonum = models.AutoField(primary_key=True)
    company_code = models.IntegerField(default=0)
    company_name = models.CharField(max_length=225, default='')
    company_name2 = models.CharField(max_length=225, default='')
    company_address = models.CharField(max_length=225, default='')
    company_address2 = models.CharField(max_length=225, default='')
    tin = models.CharField(max_length=50, default='')
    accreditation_no = models.CharField(max_length=50, default='')
    date_issued = models.CharField(max_length=50, default='')
    date_valid = models.CharField(max_length=50, default='')

    class Meta:
        db_table = 'tbl_lead_setup'

class Employee(models.Model):
    autonum = models.AutoField(primary_key=True)
    id_code = models.SmallIntegerField(unique=True)
    Emp_ID = models.IntegerField(default=0)
    last_name = models.CharField(max_length=55, default=' ')
    first_name = models.CharField(max_length=55, default=' ')
    middle_name = models.CharField(max_length=55, default=' ')
    department = models.CharField(max_length=50, default=' ')
    designation = models.CharField(max_length=75, default=' ')
    home_phone_no = models.CharField(max_length=15, default=' ')
    mobile_no = models.CharField(max_length=25, default=' ')
    fax_no = models.CharField(max_length=15, default=' ')
    st_address = models.CharField(max_length=60, default=' ')
    city_address = models.CharField(max_length=30, default=' ')
    zip_code = models.IntegerField(default=0)
    date_of_birth = models.DateField(default='0000-00-00')
    place_of_birth = models.CharField(max_length=100, default='0.000')
    balance = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    date_as_of = models.DateField(default='0000-00-00')
    remarks = models.CharField(max_length=100, default=' ')
    active = models.CharField(max_length=1, default='Y')
    employee_image = models.BinaryField(null=True, blank=True)  # BinaryField for longblob
    date_entered = models.DateField(default='0000-00-00')
    ul_code = models.IntegerField(default=0)
    Manual_YN = models.CharField(max_length=1, default='')
    Release_type = models.CharField(max_length=10, default='CASH')
    FlexiBreak = models.CharField(max_length=5, default='N')
    SCHEDULE = models.IntegerField(default=0)
    Civil_stat = models.CharField(max_length=15, default=' ')
    Confidential = models.CharField(max_length=5, default='N')
    Finger_ID = models.CharField(max_length=20, default=' ')
    Auto_FillDTR = models.CharField(max_length=5, default=' ')
    Basic_Comp = models.CharField(max_length=1, default='Y')
    PerJob_Comp = models.CharField(max_length=1, default='N')
    Acct_no = models.CharField(max_length=20, default=' ')
    Paid_Lunch = models.CharField(max_length=5, default='N')
    SSS_chk = models.CharField(max_length=5, default='Y')
    PHIC_chk = models.CharField(max_length=5, default='Y')
    HDMF_chk = models.CharField(max_length=5, default='Y')
    Tax_chk = models.CharField(max_length=5, default='Y')
    sl_category = models.CharField(max_length=50, default='')

    class Meta:
        db_table = 'tbl_employee'

class PosPayor(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    id_code = models.IntegerField(default=0)
    tin = models.CharField(max_length=60, default=' ')
    payor_name = models.CharField(max_length=60, default=' ')
    address = models.CharField(max_length=150, default=' ')
    business_style = models.CharField(max_length=150, default=' ')
    contact_no = models.CharField(max_length=20, default=' ')
    ul_code = models.IntegerField(default=0)

    class Meta:
        db_table = 'tbl_pos_payor'

class BankCompany(models.Model):
    autonum = models.AutoField(primary_key=True)
    id_code = models.CharField(max_length=10, default='0')
    company_description = models.CharField(max_length=30, default=' ')
    active = models.CharField(max_length=1, default='Y')

    class Meta:
        db_table = 'tbl_bank_company'


class BankCard(models.Model):
    autonum = models.AutoField(primary_key=True)
    id_code = models.CharField(max_length=10, default='0')
    card_description = models.CharField(max_length=30, default=' ')
    active = models.CharField(max_length=1, default='Y')

    class Meta:
        db_table = 'tbl_bank_card'

class TSetup(models.Model):
    autonum = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=150, default=' ')
    acct_title = models.TextField()  # longtext is equivalent to TextField in Django
    sl_acct = models.CharField(max_length=900, default=' ')
    sl_id = models.IntegerField(default=0)
    sl_type = models.CharField(max_length=1, default='')
    acct_title2 = models.CharField(max_length=150, default=' ')
    sys_info = models.CharField(max_length=20, default='')
    terminal_no = models.CharField(max_length=21, default=' ')
    status = models.CharField(max_length=21, default=' ')
    module = models.CharField(max_length=100, default='')
    sl_acct2 = models.CharField(max_length=100, default='')
    sl_id2 = models.IntegerField(default=0)
    sl_type2 = models.CharField(max_length=1, default='')

    class Meta:
        db_table = 'tbl_setup'

class OtherAccount(models.Model):
    autonum = models.AutoField(primary_key=True)
    id_code = models.PositiveSmallIntegerField(default=0)
    sl_name = models.CharField(max_length=150, default=' ')
    trade_name = models.CharField(max_length=100, default=' ')
    abbr = models.CharField(max_length=10, default=' ')
    last_name = models.CharField(max_length=30, default=' ')
    first_name = models.CharField(max_length=30, default=' ')
    middle_name = models.CharField(max_length=30, default=' ')
    code = models.CharField(max_length=75, default='')
    acct_title = models.CharField(max_length=100, default=' ')
    balance = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    date_as_of = models.DateField(default='0000-00-00')
    calculation = models.BooleanField(default=False)
    ul_code = models.IntegerField(default=0)
    alter_code = models.CharField(max_length=50, default=' ')
    active = models.CharField(max_length=1, default='Y')

    class Meta:
        db_table = 'tbl_other_acct'

class PosCashBreakdown(models.Model):
    login_record = models.IntegerField(default=0)
    trans_id = models.BigAutoField(primary_key=True)
    date_stamp = models.CharField(max_length=20, default='')
    quantity = models.IntegerField(default=0)
    denomination = models.CharField(max_length=20, default='')
    total = models.DecimalField(max_digits=20, decimal_places=3, null=True, default=None)
    reviewed_by = models.IntegerField()
    parent_autonum_ref = models.CharField(max_length=50, default='')
    sync_created = models.CharField(max_length=50, default='')
    sync_status_server2 = models.CharField(max_length=4, default='NO')
    sync_status_server1 = models.CharField(max_length=4, default='NO')
    sync_status = models.CharField(max_length=4, default='NO')
    sync_terminal_no = models.IntegerField(default=0)
    sync_created_server1 = models.CharField(max_length=50, default='')
    sync_created_server2 = models.CharField(max_length=50, default='')

    class Meta:
        managed = False
        db_table = 'tbl_pos_cash_breakdown'


class SalesTransCreditCard(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    sales_trans_id = models.IntegerField()
    terminal_no = models.CharField(max_length=21, default='0')
    cashier_id = models.IntegerField(default=0)
    document_type = models.CharField(max_length=10, default=' ')
    details_id = models.IntegerField()
    card_no = models.CharField(max_length=20, null=True, blank=True)
    card_name = models.CharField(max_length=50, null=True, blank=True)
    bank = models.IntegerField(null=True, blank=True)
    card_holder = models.CharField(max_length=100, null=True, blank=True)
    approval_no = models.CharField(max_length=100, null=True, blank=True)
    expiry_date = models.CharField(max_length=30, null=True, blank=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'tbl_pos_sales_trans_creditcard'


class SalesTransEPS(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    sales_trans_id = models.IntegerField(default=0)
    terminal_no = models.CharField(max_length=21, default='0')
    cashier_id = models.IntegerField(default=0)
    document_type = models.CharField(max_length=10, default=' ')
    details_id = models.IntegerField(default=0)
    card_no = models.CharField(max_length=30, null=True, blank=True)
    bank = models.IntegerField(null=True, blank=True)
    card_holder = models.CharField(max_length=100, null=True, blank=True)
    approval_no = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)

    class Meta:
        managed = False  # This prevents Django from creating a new table, assuming it already exists in your database
        db_table = 'tbl_pos_sales_trans_eps'

class PosCashiersLogin(models.Model):
    fid = models.BigAutoField(primary_key=True)
    trans_id = models.IntegerField(unique=True)
    terminal_no = models.CharField(max_length=21, default='')
    site_code = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    id_code = models.IntegerField(null=True, default=None)
    name_stamp = models.CharField(max_length=100, null=True, default=None)
    date_stamp = models.CharField(max_length=30, null=True, default=None)
    change_fund = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    borrowed_fund = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    time_login = models.CharField(max_length=30, null=True, default=None)
    time_logout = models.CharField(max_length=30, null=True, default=None)
    islogout = models.CharField(max_length=3, default='NO')
    isshift_end = models.CharField(max_length=3, default='NO')
    isxread = models.CharField(max_length=3, default='NO')
    parent_autonum_ref = models.CharField(max_length=50, default='')
    sync_created = models.CharField(max_length=50, default='')
    sync_status_server2 = models.CharField(max_length=4, default='NO')
    sync_status_server1 = models.CharField(max_length=4, default='NO')
    sync_status = models.CharField(max_length=4, default='NO')
    sync_terminal_no = models.IntegerField(default=0)
    sync_created_server1 = models.CharField(max_length=50, default='')
    sync_created_server2 = models.CharField(max_length=50, default='')

    class Meta:
        managed = False
        db_table = 'tbl_pos_cashiers_login'

class Customer(models.Model):
    autonum = models.AutoField(primary_key=True)
    id_code = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    trade_name = models.CharField(max_length=150, default=' ')
    customer_class = models.CharField(max_length=15, default=' ')
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=20)
    business_phone_no = models.CharField(max_length=15, default=' ')
    business_style = models.CharField(max_length=150, default='')
    mobile_no = models.CharField(max_length=15, default=' ')
    fax_no = models.CharField(max_length=15, default=' ')
    st_address = models.CharField(max_length=60, default=' ')
    province = models.CharField(max_length=225, default=' ')
    city_address = models.CharField(max_length=30, default=' ')
    zip_code = models.IntegerField(default=0)
    vat = models.CharField(max_length=1, default='')
    bir_reg_no = models.CharField(max_length=25, default=' ')
    tax_id_no = models.CharField(max_length=25, default=' ')
    so_terms_id = models.IntegerField(default=0)
    so_terms = models.CharField(max_length=25, default='')
    credit_terms = models.SmallIntegerField(default=0)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    past_due_limit = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    past_due_days = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    date_as_of = models.DateField(default='1900-01-01')
    active = models.CharField(max_length=50, default='Y')
    group_id = models.IntegerField(default=0)
    group_name = models.CharField(max_length=150, default=' ')
    area_id = models.IntegerField(default=0)
    area_name = models.CharField(max_length=150, default=' ')
    sub_area_id = models.IntegerField(default=0)
    sub_area_name = models.CharField(max_length=150, default='')
    office_name = models.CharField(max_length=150, default=' ')
    agent_id = models.IntegerField(default=0)
    agent_name = models.CharField(max_length=150, default=' ')
    collector_id = models.IntegerField(default=0)
    collector_name = models.CharField(max_length=150, default=' ')
    kob_id = models.IntegerField(default=0)
    kob_name = models.CharField(max_length=150, default=' ')
    remarks = models.CharField(max_length=100, default=' ')
    customer_image = models.BinaryField(blank=True, null=True)
    date_entered = models.DateField(default='1900-01-01')
    ul_code = models.IntegerField(default=0)
    Concessionare = models.CharField(max_length=10, default='')
    sys_type = models.CharField(max_length=11, default='')
    joblot_no_ref = models.BigIntegerField(default=0)
    sl_category = models.CharField(max_length=50, default='')
    sl_sub_category_id = models.IntegerField(default=0)
    sl_sub_category_description = models.CharField(max_length=50, default='')
    class Meta:
        db_table = 'tbl_customer'

class PosWaiterList(models.Model):
    autonum = models.AutoField(primary_key=True)
    waiter_id = models.IntegerField()
    waiter_name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'tbl_pos_waiterlist'

class MainRefSlSupplier(models.Model):
    id = models.AutoField(primary_key=True)
    id_code = models.PositiveIntegerField(default=0)
    trade_name = models.CharField(max_length=150, default='')
    supplier_class = models.CharField(max_length=15, default=' ')
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=20)
    business_phone_no = models.CharField(max_length=15, default=' ')
    mobile_no = models.CharField(max_length=15, default=' ')
    fax_no = models.CharField(max_length=15, default=' ')
    address = models.CharField(max_length=150, default=' ')
    city_municipality = models.CharField(max_length=150, default=' ')
    province = models.CharField(max_length=150, default=' ')
    zip_code = models.PositiveIntegerField(default=0)
    trade = models.CharField(max_length=1, default='')
    vat_registration_type = models.CharField(max_length=1, default='')
    tax_id_no = models.CharField(max_length=25, default=' ')
    active_status = models.CharField(max_length=1, default='Y')
    group_id = models.PositiveIntegerField(default=0)
    group_name = models.CharField(max_length=150, default=' ')
    remarks = models.CharField(max_length=100, default=' ')
    supplier_image = models.BinaryField(null=True, blank=True)
    date_entered = models.DateField(default='1960-01-01')
    ul_code = models.PositiveIntegerField(default=0)
    sl_sub_category_id = models.PositiveIntegerField(default=0)
    sl_sub_category_description = models.CharField(max_length=50, default='')

    class Meta:
        db_table = 'tbl_main_ref_sl_supplier'

class MainRefCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    id_code = models.BigIntegerField(default=0)
    trade_name = models.CharField(max_length=150, default=' ')
    customer_class = models.CharField(max_length=15, default=' ')
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=20)
    business_phone_no = models.CharField(max_length=15, default=' ')
    mobile_no = models.CharField(max_length=15, default=' ')
    fax_no = models.CharField(max_length=15, default=' ')
    address = models.CharField(max_length=150, default=' ')
    city_municipality = models.CharField(max_length=150, default=' ')
    province = models.CharField(max_length=150, default=' ')
    zip_code = models.IntegerField(default=0)
    vat_registration_type = models.CharField(max_length=1, default='')
    tax_id_no = models.CharField(max_length=25, default=' ')
    active_status = models.CharField(max_length=1, default='Y')
    group_id = models.IntegerField(default=0)
    group_name = models.CharField(max_length=150, default=' ')
    area_id = models.IntegerField(default=0)
    area_name = models.CharField(max_length=150, default=' ')
    agent_id = models.IntegerField(default=0)
    agent_name = models.CharField(max_length=150, default=' ')
    collector_id = models.IntegerField(default=0)
    collector_name = models.CharField(max_length=150, default=' ')
    kob_id = models.IntegerField(default=0)
    kob_name = models.CharField(max_length=150, default=' ')
    remarks = models.CharField(max_length=100, default=' ')
    customer_image = models.BinaryField(null=True)
    date_entered = models.DateField(default='1900-01-01')
    ul_code = models.IntegerField(default=0)
    sl_sub_category_id = models.IntegerField(default=0)
    sl_sub_category_description = models.CharField(max_length=50, default='')

    class Meta:
        db_table = 'tbl_main_ref_sl_customer'

class SeniorCitizenDiscount(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    sales_trans_id = models.IntegerField(null=True, blank=True)
    terminal_no = models.CharField(max_length=21, default='0')
    cashier_id = models.CharField(max_length=21, default='')
    document_type = models.CharField(max_length=10, default=' ')
    details_id = models.IntegerField(default=0)
    id_no = models.CharField(max_length=100, null=True, blank=True)
    senior_member_name = models.CharField(max_length=500, null=True, blank=True)
    id = models.IntegerField(default=0)
    tin_no = models.CharField(max_length=100, default='0')
    so_no = models.CharField(max_length=50, default=' ')

    class Meta:
        db_table = 'tbl_pos_sales_trans_senior_citizen_discount'
        managed = False  # Set this to False if you don't want Django to manage this table

    def __str__(self):
        return f"SeniorCitizenDiscount - autonum: {self.autonum}, sales_trans_id: {self.sales_trans_id}"

class Product(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    company_code = models.CharField(max_length=10, default='')
    ul_code = models.IntegerField(default=0)
    pos_item = models.CharField(max_length=6, default='NO')
    weight_scale = models.CharField(max_length=1, default='N')
    pos_site_code = models.CharField(max_length=10, default='0')
    print_cat = models.IntegerField(default=0)
    item_type = models.CharField(max_length=20, default='')
    category_id = models.IntegerField(default=0)
    category = models.CharField(max_length=150, default=' ')
    principal_id = models.IntegerField(default=0)
    principal = models.CharField(max_length=100, default=' ')
    brand = models.CharField(max_length=50, default=' ')
    model = models.CharField(max_length=50, default=' ')
    style = models.CharField(max_length=50, default=' ')
    p_size = models.CharField(max_length=50, default=' ')
    color = models.CharField(max_length=50, default=' ')
    qty_onhand = models.FloatField(default=0.000)
    qty_avl = models.FloatField(default=0.000)
    uom = models.CharField(max_length=50, default=' ')
    item_code = models.CharField(max_length=20, default='')
    bar_code = models.CharField(max_length=20, default=' ')
    alternate_code = models.CharField(max_length=20, default=' ')
    long_desc = models.CharField(max_length=150, default=' ')
    short_desc = models.CharField(max_length=150, default=' ')
    reg_price = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    key_price = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    ws_price = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    ec_price = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    last_purch = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    po_qty_allowance = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    so_qty_allowance = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    standard_price = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    rm_cost = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    dl_cost = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    oh_cost = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    ave_cost = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    fifo_cost = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    tax_code = models.CharField(max_length=10, default='')
    prod_img = models.BinaryField(null=True, blank=True)
    active = models.CharField(max_length=1, default='Y')
    activity_id_code = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    activity_assigned_code = models.CharField(max_length=25, default='')
    activity_description = models.CharField(max_length=150, default='')
    with_serial = models.CharField(max_length=4, default='N')
    batch_code = models.CharField(max_length=4, default='N')
    rebates_amount = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    salesman_amount = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    trustor_name = models.CharField(max_length=250, default='')
    virtual_setup = models.CharField(max_length=10, default='')
    production_setup = models.CharField(max_length=1, default='N')
    charges_ar = models.CharField(max_length=1, default='N')
    vat_category_code = models.CharField(max_length=10, default='')
    back_flush = models.CharField(max_length=1, default='N')
    charcoal_item = models.CharField(max_length=1, default='N')
    trustor_flag = models.CharField(max_length=1, default='N')
    parent_autonum_ref = models.CharField(max_length=50, default='')
    sync_created = models.CharField(max_length=50, default='')
    sync_status = models.CharField(max_length=4, default='NO')

    class Meta:
        db_table = 'tbl_product'


class PosRestTable(models.Model):
    details_id = models.IntegerField(primary_key=True)
    table_no = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    table_start = models.IntegerField(default=0)
    pump_name = models.CharField(max_length=50, default=' ')
    gas_pump = models.BinaryField(blank=True, null=True)  # Assuming blob is used to store binary data
    site_code = models.CharField(max_length=50, default='')

    class Meta:
        db_table = 'tbl_pos_rest_table'
        
class PosSalesOrder(models.Model):
    autonum = models.AutoField(primary_key=True)
    SO_no = models.IntegerField()
    document_no = models.IntegerField()
    customer_type = models.CharField(max_length=1, default='W')
    customer_name = models.CharField(max_length=150, null=True, default=None)
    table_no = models.IntegerField(null=True, default=None)
    q_no = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    dinein_takeout = models.CharField(max_length=15, default=' ')
    guest_count = models.IntegerField(null=True, default=None)
    waiter_id = models.IntegerField(null=True, default=None)
    cashier_id = models.IntegerField(null=True, default=None)
    salesman_id = models.IntegerField(null=True, default=None)
    terminal_no = models.IntegerField(null=True, default=None)
    site_code = models.CharField(max_length=50, default='')
    date_trans = models.CharField(max_length=20, null=True, default=None)
    time_trans = models.CharField(max_length=20, null=True, default=None)
    paid = models.CharField(max_length=2, null=True, default=None)
    active = models.CharField(max_length=2, null=True, default=None)

    class Meta:
        # Define primary key constraints
        db_table = 'tbl_pos_sales_order'
        unique_together = (('autonum', 'SO_no', 'document_no'),)
    
        
class User(models.Model):
    autonum = models.AutoField(primary_key=True)
    id_code = models.PositiveSmallIntegerField(default=0)
    fullname = models.CharField(max_length=40, default=' ')
    department = models.CharField(max_length=30, default=' ')
    user_name = models.CharField(max_length=30, default=' ')
    password = models.CharField(max_length=100, default=' ')
    user_rank = models.CharField(max_length=15, default=' ')
    sys_type = models.CharField(max_length=5, default='')
    mod_access = models.CharField(max_length=2000, default=' ')
    acct_title = models.TextField()
    active = models.CharField(max_length=1, default='Y')
    emp_id = models.IntegerField(default=0)

    class Meta:
        db_table = 'tbl_user'  # Define the database table name
        ordering = ['fullname']  # Define the default ordering of results
        unique_together = [['user_name', 'department']]  # Define unique constraints



class POS_Terminal(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    terminal_no = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    site_no = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    Serial_no = models.CharField(max_length=100, default='')
    Machine_no = models.CharField(max_length=100, default='')
    Model_no = models.CharField(max_length=100, default='')
    PTU_no = models.CharField(max_length=100, default='')
    date_issue = models.CharField(max_length=30, default='0000-00-00')
    date_valid = models.CharField(max_length=30, default='0000-00-00')
    ul_code = models.IntegerField(default=0)
    class Meta:
        db_table = 'tbl_pos_terminal'


class PosSalesTransDetails(models.Model):
    
    autonum = models.BigAutoField(primary_key=True)
    sales_trans_id = models.IntegerField()
    datetime_stamp = models.CharField(max_length=22, default='')
    document_type = models.CharField(max_length=10, default=' ')
    terminal_no = models.CharField(max_length=21, default='0')
    site_code = models.CharField(max_length=50, default='')
    cashier_id = models.IntegerField(default=0)
    details_id = models.IntegerField(default=0)
    line_no = models.IntegerField(null=True, blank=True)
    barcode = models.CharField(max_length=20, null=True, blank=True)
    alternate_code = models.CharField(max_length=20, null=True, blank=True)
    itemcode = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=500, default=' ')
    price = models.DecimalField(max_digits=11, decimal_places=2,default=0.00)
    quantity = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    item_disc = models.DecimalField(max_digits=15, decimal_places=7, default=0.0000000)
    desc_rate = models.CharField(max_length=100, default='0.000')
    vat_ex = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    price_override = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    isnon_vat = models.CharField(max_length=4, null=True, blank=True)
    is_SC = models.CharField(max_length=4, default='NO')
    isvoid = models.CharField(max_length=3, null=True, blank=True)
    trans_type = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=1, default='')
    discounted_by = models.CharField(max_length=100, default='')
    class Meta:
        db_table = 'tbl_pos_sales_trans_details'
        managed = False  # Set managed to False to indicate that Django should not manage the table
        
        
class InvRefNo(models.Model):
    autonum = models.AutoField(primary_key=True)
    description = models.CharField(max_length=25, default=' ')
    terminalno = models.CharField(max_length=50, default='0')
    next_no = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    string_next_no = models.CharField(max_length=50, default='')
    reset_counter = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    start_no = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    end_no = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)

    class Meta:
        db_table = 'tbl_inv_ref_no' 



class PosSalesTrans(models.Model):
    autonum = models.IntegerField(primary_key=True)  # AutoField is not available in Django for composite primary keys
    login_record = models.IntegerField()
    sales_trans_id = models.IntegerField()
    terminal_no = models.CharField(max_length=21, default='0')
    site_code = models.CharField(max_length=50, default='')
    cashier_id = models.IntegerField(default=0)
    datetime_stamp = models.CharField(max_length=22, null=True, blank=True)
    bagger = models.CharField(max_length=100, null=True, blank=True)
    sales_man = models.CharField(max_length=100, null=True, blank=True)
    document_no = models.CharField(max_length=50, default=' ')
    document_type = models.CharField(max_length=15, default='')
    pricing = models.CharField(max_length=25, default='')
    amount_tendered = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    discount_type = models.CharField(max_length=20, default=' ')
    amount_disc = models.DecimalField(max_digits=15, decimal_places=7, default=0.0000000)
    lvl1_disc = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    lvl2_disc = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    lvl3_disc = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    lvl4_disc = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    lvl5_disc = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    vat_stamp = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    isvoid = models.CharField(max_length=3, null=True, blank=True)
    issuspend = models.CharField(max_length=3, null=True, blank=True)
    isclosed = models.CharField(max_length=3, null=True, blank=True)
    trans_type = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=1, default='')
    prepared_by = models.CharField(max_length=60, null=True, blank=True)
    approved_by = models.CharField(max_length=60, null=True, blank=True)
    approved_date = models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        managed = False  # To indicate that this model does not have a corresponding database table managed by Django
        db_table = 'tbl_pos_sales_trans'
        unique_together = (
            'autonum', 'sales_trans_id', 'terminal_no', 'cashier_id', 'document_no', 'document_type'
        )  # To represent composite primary key


class PosSalesInvoiceListing(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    company_code = models.CharField(max_length=10, default='')
    ul_code = models.PositiveIntegerField(default=0)
    site_code = models.IntegerField(default=0)
    doc_type = models.CharField(max_length=10, default='')
    doc_no = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    terminal_no = models.CharField(max_length=21, default='0')
    zread_no = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    cashier_id = models.IntegerField(default=0)
    doc_date = models.CharField(max_length=25, default=' ')
    line_number = models.PositiveIntegerField(default=0)
    bar_code = models.CharField(max_length=20, default=' ')
    alternate_code = models.CharField(max_length=20, default=' ')
    item_code = models.CharField(max_length=20, default=' ')
    rec_qty = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    rec_uom = models.CharField(max_length=30, default=' ')
    description = models.CharField(max_length=500, default=' ')
    unit_price = models.DecimalField(max_digits=15, decimal_places=3,  default=0.000)
    sub_total = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    pc_price = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    qtyperuom = models.FloatField(default=0.000)
    disc_amt = models.DecimalField(max_digits=15, decimal_places=7, null=True, default=None)
    desc_rate = models.CharField(max_length=100, default='0.000')
    vat_amt = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    vat_exempt = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    net_total = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    isvoid = models.CharField(max_length=3, null=True, default=None)
    unit_cost = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    vatable = models.CharField(max_length=2, default='')
    status = models.CharField(max_length=1, default='')
    so_no = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    so_doc_no = models.CharField(max_length=999, default='')
    sn_bc = models.CharField(max_length=10, default='')
    discounted_by = models.CharField(max_length=21, default='')

    class Meta:
        db_table = 'tbl_pos_sales_invoice_listing'


class PosSalesInvoiceList(models.Model):
    autonum = models.BigAutoField(primary_key=True)
    company_code = models.CharField(max_length=10, default='')
    ul_code = models.PositiveIntegerField(default=0)
    site_code = models.IntegerField(default=0)
    trans_type = models.CharField(max_length=100, default=' ')
    discount_type = models.CharField(max_length=4, default='')
    zread_no = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    doc_type = models.CharField(max_length=10, default='')
    doc_no = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    terminal_no = models.CharField(max_length=21, default='0')
    cashier_id = models.IntegerField(default=0)
    so_no = models.CharField(max_length=50, default=' ')
    so_doc_no = models.CharField(max_length=999, default='')
    doc_date = models.CharField(max_length=25, default=' ')
    customer_code = models.IntegerField(default=0)
    customer_name = models.CharField(max_length=100, default=' ')
    customer_address = models.CharField(max_length=250, default=' ')
    business_unit = models.CharField(max_length=100, default=' ')
    customer_type = models.CharField(max_length=1, default='')
    salesman_id = models.IntegerField(default=0)
    salesman = models.CharField(max_length=100, default=' ')
    collector_id = models.IntegerField(default=0)
    collector = models.CharField(max_length=100, default=' ')
    pricing = models.CharField(max_length=25, default=' ')
    terms = models.IntegerField(default=0)
    remarks = models.CharField(max_length=999, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    ServiceCharge_TotalAmount = models.DecimalField(max_digits=15, decimal_places=3, null=True, blank=True)
    total_cash = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    total_check = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    total_pdc = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    total_eps = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    total_credit_card = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    total_credit_sales = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    other_payment = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    total_adv = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    total_qty = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    discount = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    vat = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    vat_exempt = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    vat_exempted = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    net_vat = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    net_discount = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    sub_total = models.DecimalField(max_digits=21, decimal_places=9, default=0.000000000)
    lvl1_disc = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    lvl2_disc = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    lvl3_disc = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    lvl4_disc = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    lvl5_disc = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    HMO = models.CharField(max_length=150, default=' ')
    PHIC = models.CharField(max_length=1, default='')
    status = models.CharField(max_length=1, default='')
    prepared_id = models.IntegerField(default=0)
    prepared_by = models.CharField(max_length=60, default=' ')
    reviewed_by = models.CharField(max_length=60, null=True, default=None)
    approved_date = models.CharField(max_length=25, null=True, default=None)
    approved_by = models.CharField(max_length=60, null=True, default=None)
    reviewed_date = models.CharField(max_length=25, null=True, default=None)
    cancel_by = models.CharField(max_length=60, default=' ')
    cancel_date = models.CharField(max_length=25, default=' ')
    sys_type = models.CharField(max_length=11, default='')


    class Meta:
        db_table = 'tbl_pos_sales_invoice_list'




class AcctSubsidiary(models.Model):
    autonum = models.IntegerField(primary_key=True)  # AutoField is not available in Django for composite primary keys
    primary_code = models.FloatField(null=True, default=None)
    secondary_code = models.FloatField(null=True, default=None)
    acct_code = models.FloatField(null=True, default=None)
    subsidiary_code = models.FloatField(null=True, default=None)
    subsidiary_acct_title = models.CharField(max_length=255, null=True, default=None)
    subsidiary_acct_desc = models.CharField(max_length=1000, default=' ')
    SL = models.CharField(max_length=255, null=True, default=None)
    sl_type = models.CharField(max_length=255, null=True, default=None)
    calculation = models.FloatField(null=True, default=None)
    alter_code = models.CharField(max_length=255, null=True, default=None)
    alter_name = models.CharField(max_length=255, null=True, default=None)
    category = models.TextField(null=True, default=None)
    sub_category = models.TextField(null=True, default=None)
    status = models.CharField(max_length=1, default='Y')

    class Meta:
        db_table = 'tbl_acct_subsidiary'








