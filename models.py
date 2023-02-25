# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'))


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'))


class AuthUser(models.Model):
    password = models.CharField(max_length=256)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'))


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'))


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'))


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TickAppAnalysistools(models.Model):
    tools = models.CharField(max_length=234)
    super_category = models.CharField(max_length=234)
    category = models.CharField(max_length=234)
    subcategory = models.CharField(max_length=234)
    metrics = models.CharField(max_length=234)
    description = models.CharField(max_length=234)
    code = models.CharField(max_length=54)
    source = models.CharField(max_length=54)
    nominator = models.CharField(max_length=234)
    denominator = models.CharField(max_length=234)
    reference = models.FloatField()

    class Meta:
        managed = False
        db_table = 'tick_app_analysistools'


class TickAppBsheet(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_id = models.CharField(max_length=200, blank=True, null=True)
    year = models.CharField(max_length=200, blank=True, null=True)
    cashandcashequivalents = models.FloatField(db_column='cashAndCashEquivalents', blank=True, null=True)  # Field name made lowercase.
    shortterminvestments = models.FloatField(db_column='shortTermInvestments', blank=True, null=True)  # Field name made lowercase.
    cashandshortterminvestments = models.FloatField(db_column='cashAndShortTermInvestments', blank=True, null=True)  # Field name made lowercase.
    netreceivables = models.FloatField(db_column='netReceivables', blank=True, null=True)  # Field name made lowercase.
    inventory = models.FloatField(blank=True, null=True)
    othercurrentassets = models.FloatField(db_column='otherCurrentAssets', blank=True, null=True)  # Field name made lowercase.
    totalcurrentassets = models.FloatField(db_column='totalCurrentAssets', blank=True, null=True)  # Field name made lowercase.
    propertyplantequipmentnet = models.FloatField(db_column='propertyPlantEquipmentNet', blank=True, null=True)  # Field name made lowercase.
    goodwill = models.FloatField(blank=True, null=True)
    intangibleassets = models.FloatField(db_column='intangibleAssets', blank=True, null=True)  # Field name made lowercase.
    goodwillandintangibleassets = models.FloatField(db_column='goodwillAndIntangibleAssets', blank=True, null=True)  # Field name made lowercase.
    longterminvestments = models.FloatField(db_column='longTermInvestments', blank=True, null=True)  # Field name made lowercase.
    taxassets = models.FloatField(db_column='taxAssets', blank=True, null=True)  # Field name made lowercase.
    othernoncurrentassets = models.FloatField(db_column='otherNonCurrentAssets', blank=True, null=True)  # Field name made lowercase.
    totalnoncurrentassets = models.FloatField(db_column='totalNonCurrentAssets', blank=True, null=True)  # Field name made lowercase.
    otherassets = models.FloatField(db_column='otherAssets', blank=True, null=True)  # Field name made lowercase.
    totalassets = models.FloatField(db_column='totalAssets', blank=True, null=True)  # Field name made lowercase.
    accountpayables = models.FloatField(db_column='accountPayables', blank=True, null=True)  # Field name made lowercase.
    shorttermdebt = models.FloatField(db_column='shortTermDebt', blank=True, null=True)  # Field name made lowercase.
    taxpayables = models.FloatField(db_column='taxPayables', blank=True, null=True)  # Field name made lowercase.
    deferredrevenue = models.FloatField(db_column='deferredRevenue', blank=True, null=True)  # Field name made lowercase.
    othercurrentliabilities = models.FloatField(db_column='otherCurrentLiabilities', blank=True, null=True)  # Field name made lowercase.
    totalcurrentliabilities = models.FloatField(db_column='totalCurrentLiabilities', blank=True, null=True)  # Field name made lowercase.
    longtermdebt = models.FloatField(db_column='longTermDebt', blank=True, null=True)  # Field name made lowercase.
    deferredrevenuenoncurrent = models.FloatField(db_column='deferredRevenueNonCurrent', blank=True, null=True)  # Field name made lowercase.
    deferredtaxliabilitiesnoncurrent = models.FloatField(db_column='deferredTaxLiabilitiesNonCurrent', blank=True, null=True)  # Field name made lowercase.
    othernoncurrentliabilities = models.FloatField(db_column='otherNonCurrentLiabilities', blank=True, null=True)  # Field name made lowercase.
    totalnoncurrentliabilities = models.FloatField(db_column='totalNonCurrentLiabilities', blank=True, null=True)  # Field name made lowercase.
    otherliabilities = models.FloatField(db_column='otherLiabilities', blank=True, null=True)  # Field name made lowercase.
    totalliabilities = models.FloatField(db_column='totalLiabilities', blank=True, null=True)  # Field name made lowercase.
    commonstock = models.FloatField(db_column='commonStock', blank=True, null=True)  # Field name made lowercase.
    retainedearnings = models.FloatField(db_column='retainedEarnings', blank=True, null=True)  # Field name made lowercase.
    accumulatedothercomprehensiveincomeloss = models.FloatField(db_column='accumulatedOtherComprehensiveIncomeLoss', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_bsheet'


class TickAppBsheetgrowth(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    period = models.CharField(max_length=200, blank=True, null=True)
    growthcashandcashequivalents = models.FloatField(db_column='growthCashAndCashEquivalents', blank=True, null=True)  # Field name made lowercase.
    growthshortterminvestments = models.FloatField(db_column='growthShortTermInvestments', blank=True, null=True)  # Field name made lowercase.
    growthcashandshortterminvestments = models.FloatField(db_column='growthCashAndShortTermInvestments', blank=True, null=True)  # Field name made lowercase.
    growthnetreceivables = models.FloatField(db_column='growthNetReceivables', blank=True, null=True)  # Field name made lowercase.
    growthinventory = models.FloatField(db_column='growthInventory', blank=True, null=True)  # Field name made lowercase.
    growthothercurrentassets = models.FloatField(db_column='growthOtherCurrentAssets', blank=True, null=True)  # Field name made lowercase.
    growthtotalcurrentassets = models.FloatField(db_column='growthTotalCurrentAssets', blank=True, null=True)  # Field name made lowercase.
    growthpropertyplantequipmentnet = models.FloatField(db_column='growthPropertyPlantEquipmentNet', blank=True, null=True)  # Field name made lowercase.
    growthgoodwill = models.FloatField(db_column='growthGoodwill', blank=True, null=True)  # Field name made lowercase.
    growthintangibleassets = models.FloatField(db_column='growthIntangibleAssets', blank=True, null=True)  # Field name made lowercase.
    growthgoodwillandintangibleassets = models.FloatField(db_column='growthGoodwillAndIntangibleAssets', blank=True, null=True)  # Field name made lowercase.
    growthlongterminvestments = models.FloatField(db_column='growthLongTermInvestments', blank=True, null=True)  # Field name made lowercase.
    growthtaxassets = models.FloatField(db_column='growthTaxAssets', blank=True, null=True)  # Field name made lowercase.
    growthothernoncurrentassets = models.FloatField(db_column='growthOtherNonCurrentAssets', blank=True, null=True)  # Field name made lowercase.
    growthtotalnoncurrentassets = models.FloatField(db_column='growthTotalNonCurrentAssets', blank=True, null=True)  # Field name made lowercase.
    growthotherassets = models.FloatField(db_column='growthOtherAssets', blank=True, null=True)  # Field name made lowercase.
    growthtotalassets = models.FloatField(db_column='growthTotalAssets', blank=True, null=True)  # Field name made lowercase.
    growthaccountpayables = models.FloatField(db_column='growthAccountPayables', blank=True, null=True)  # Field name made lowercase.
    growthshorttermdebt = models.FloatField(db_column='growthShortTermDebt', blank=True, null=True)  # Field name made lowercase.
    growthtaxpayables = models.FloatField(db_column='growthTaxPayables', blank=True, null=True)  # Field name made lowercase.
    growthdeferredrevenue = models.FloatField(db_column='growthDeferredRevenue', blank=True, null=True)  # Field name made lowercase.
    growthothercurrentliabilities = models.FloatField(db_column='growthOtherCurrentLiabilities', blank=True, null=True)  # Field name made lowercase.
    growthtotalcurrentliabilities = models.FloatField(db_column='growthTotalCurrentLiabilities', blank=True, null=True)  # Field name made lowercase.
    growthlongtermdebt = models.FloatField(db_column='growthLongTermDebt', blank=True, null=True)  # Field name made lowercase.
    growthdeferredrevenuenoncurrent = models.FloatField(db_column='growthDeferredRevenueNonCurrent', blank=True, null=True)  # Field name made lowercase.
    growthdeferrredtaxliabilitiesnoncurrent = models.FloatField(db_column='growthDeferrredTaxLiabilitiesNonCurrent', blank=True, null=True)  # Field name made lowercase.
    growthothernoncurrentliabilities = models.FloatField(db_column='growthOtherNonCurrentLiabilities', blank=True, null=True)  # Field name made lowercase.
    growthtotalnoncurrentliabilities = models.FloatField(db_column='growthTotalNonCurrentLiabilities', blank=True, null=True)  # Field name made lowercase.
    growthotherliabilities = models.FloatField(db_column='growthOtherLiabilities', blank=True, null=True)  # Field name made lowercase.
    growthtotalliabilities = models.FloatField(db_column='growthTotalLiabilities', blank=True, null=True)  # Field name made lowercase.
    growthcommonstock = models.FloatField(db_column='growthCommonStock', blank=True, null=True)  # Field name made lowercase.
    growthretainedearnings = models.FloatField(db_column='growthRetainedEarnings', blank=True, null=True)  # Field name made lowercase.
    growthaccumulatedothercomprehensiveincomeloss = models.FloatField(db_column='growthAccumulatedOtherComprehensiveIncomeLoss', blank=True, null=True)  # Field name made lowercase.
    growthothertotalstockholdersequity = models.FloatField(db_column='growthOthertotalStockholdersEquity', blank=True, null=True)  # Field name made lowercase.
    growthtotalstockholdersequity = models.FloatField(db_column='growthTotalStockholdersEquity', blank=True, null=True)  # Field name made lowercase.
    growthtotalliabilitiesandstockholdersequity = models.FloatField(db_column='growthTotalLiabilitiesAndStockholdersEquity', blank=True, null=True)  # Field name made lowercase.
    growthtotalinvestments = models.FloatField(db_column='growthTotalInvestments', blank=True, null=True)  # Field name made lowercase.
    growthtotaldebt = models.FloatField(db_column='growthTotalDebt', blank=True, null=True)  # Field name made lowercase.
    growthnetdebt = models.FloatField(db_column='growthNetDebt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_bsheetgrowth'


class TickAppCflow(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_id = models.CharField(max_length=200, blank=True, null=True)
    year = models.CharField(max_length=200, blank=True, null=True)
    netincome = models.FloatField(db_column='netIncome', blank=True, null=True)  # Field name made lowercase.
    inventory = models.FloatField(blank=True, null=True)
    accountspayables = models.FloatField(db_column='accountsPayables', blank=True, null=True)  # Field name made lowercase.
    accountsreceivables = models.FloatField(db_column='accountsReceivables', blank=True, null=True)  # Field name made lowercase.
    acquisitionsnet = models.FloatField(db_column='acquisitionsNet', blank=True, null=True)  # Field name made lowercase.
    capitalexpenditure = models.FloatField(db_column='capitalExpenditure', blank=True, null=True)  # Field name made lowercase.
    cashatbeginningofperiod = models.FloatField(db_column='cashAtBeginningOfPeriod', blank=True, null=True)  # Field name made lowercase.
    cashatendofperiod = models.FloatField(db_column='cashAtEndOfPeriod', blank=True, null=True)  # Field name made lowercase.
    changeinworkingcapital = models.FloatField(db_column='changeInWorkingCapital', blank=True, null=True)  # Field name made lowercase.
    commonstockissued = models.FloatField(db_column='commonStockIssued', blank=True, null=True)  # Field name made lowercase.
    commonstockrepurchased = models.FloatField(db_column='commonStockRepurchased', blank=True, null=True)  # Field name made lowercase.
    debtrepayment = models.FloatField(db_column='debtRepayment', blank=True, null=True)  # Field name made lowercase.
    deferredincometax = models.FloatField(db_column='deferredIncomeTax', blank=True, null=True)  # Field name made lowercase.
    depreciationandamortization = models.FloatField(db_column='depreciationAndAmortization', blank=True, null=True)  # Field name made lowercase.
    dividendspaid = models.FloatField(db_column='dividendsPaid', blank=True, null=True)  # Field name made lowercase.
    effectofforexchangesoncash = models.FloatField(db_column='effectOfForexChangesOnCash', blank=True, null=True)  # Field name made lowercase.
    freecashflow = models.FloatField(db_column='freeCashFlow', blank=True, null=True)  # Field name made lowercase.
    investmentsinpropertyplantandequipment = models.FloatField(db_column='investmentsInPropertyPlantAndEquipment', blank=True, null=True)  # Field name made lowercase.
    netcashprovidedbyoperatingactivities = models.FloatField(db_column='netCashProvidedByOperatingActivities', blank=True, null=True)  # Field name made lowercase.
    netcashusedforinvestingactivites = models.FloatField(db_column='netCashUsedForInvestingActivites', blank=True, null=True)  # Field name made lowercase.
    netcashusedprovidedbyfinancingactivities = models.FloatField(db_column='netCashUsedProvidedByFinancingActivities', blank=True, null=True)  # Field name made lowercase.
    netchangeincash = models.FloatField(db_column='netChangeInCash', blank=True, null=True)  # Field name made lowercase.
    operatingcashflow = models.FloatField(db_column='operatingCashFlow', blank=True, null=True)  # Field name made lowercase.
    otherfinancingactivites = models.FloatField(db_column='otherFinancingActivites', blank=True, null=True)  # Field name made lowercase.
    otherinvestingactivites = models.FloatField(db_column='otherInvestingActivites', blank=True, null=True)  # Field name made lowercase.
    othernoncashitems = models.FloatField(db_column='otherNonCashItems', blank=True, null=True)  # Field name made lowercase.
    otherworkingcapital = models.FloatField(db_column='otherWorkingCapital', blank=True, null=True)  # Field name made lowercase.
    purchasesofinvestments = models.FloatField(db_column='purchasesOfInvestments', blank=True, null=True)  # Field name made lowercase.
    salesmaturitiesofinvestments = models.FloatField(db_column='salesMaturitiesOfInvestments', blank=True, null=True)  # Field name made lowercase.
    stockbasedcompensation = models.FloatField(db_column='stockBasedCompensation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_cflow'


class TickAppCflowgrowth(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    period = models.CharField(max_length=200, blank=True, null=True)
    growthnetincome = models.FloatField(db_column='growthNetIncome', blank=True, null=True)  # Field name made lowercase.
    growthdepreciationandamortization = models.FloatField(db_column='growthDepreciationAndAmortization', blank=True, null=True)  # Field name made lowercase.
    growthdeferredincometax = models.FloatField(db_column='growthDeferredIncomeTax', blank=True, null=True)  # Field name made lowercase.
    growthstockbasedcompensation = models.FloatField(db_column='growthStockBasedCompensation', blank=True, null=True)  # Field name made lowercase.
    growthchangeinworkingcapital = models.FloatField(db_column='growthChangeInWorkingCapital', blank=True, null=True)  # Field name made lowercase.
    growthaccountsreceivables = models.FloatField(db_column='growthAccountsReceivables', blank=True, null=True)  # Field name made lowercase.
    growthinventory = models.FloatField(db_column='growthInventory', blank=True, null=True)  # Field name made lowercase.
    growthaccountspayables = models.FloatField(db_column='growthAccountsPayables', blank=True, null=True)  # Field name made lowercase.
    growthotherworkingcapital = models.FloatField(db_column='growthOtherWorkingCapital', blank=True, null=True)  # Field name made lowercase.
    growthothernoncashitems = models.FloatField(db_column='growthOtherNonCashItems', blank=True, null=True)  # Field name made lowercase.
    growthnetcashprovidedbyoperatingactivites = models.FloatField(db_column='growthNetCashProvidedByOperatingActivites', blank=True, null=True)  # Field name made lowercase.
    growthinvestmentsinpropertyplantandequipment = models.FloatField(db_column='growthInvestmentsInPropertyPlantAndEquipment', blank=True, null=True)  # Field name made lowercase.
    growthacquisitionsnet = models.FloatField(db_column='growthAcquisitionsNet', blank=True, null=True)  # Field name made lowercase.
    growthpurchasesofinvestments = models.FloatField(db_column='growthPurchasesOfInvestments', blank=True, null=True)  # Field name made lowercase.
    growthsalesmaturitiesofinvestments = models.FloatField(db_column='growthSalesMaturitiesOfInvestments', blank=True, null=True)  # Field name made lowercase.
    growthotherinvestingactivites = models.FloatField(db_column='growthOtherInvestingActivites', blank=True, null=True)  # Field name made lowercase.
    growthnetcashusedforinvestingactivites = models.FloatField(db_column='growthNetCashUsedForInvestingActivites', blank=True, null=True)  # Field name made lowercase.
    growthdebtrepayment = models.FloatField(db_column='growthDebtRepayment', blank=True, null=True)  # Field name made lowercase.
    growthcommonstockissued = models.FloatField(db_column='growthCommonStockIssued', blank=True, null=True)  # Field name made lowercase.
    growthcommonstockrepurchased = models.FloatField(db_column='growthCommonStockRepurchased', blank=True, null=True)  # Field name made lowercase.
    growthdividendspaid = models.FloatField(db_column='growthDividendsPaid', blank=True, null=True)  # Field name made lowercase.
    growthotherfinancingactivites = models.FloatField(db_column='growthOtherFinancingActivites', blank=True, null=True)  # Field name made lowercase.
    growthnetcashusedprovidedbyfinancingactivities = models.FloatField(db_column='growthNetCashUsedProvidedByFinancingActivities', blank=True, null=True)  # Field name made lowercase.
    growtheffectofforexchangesoncash = models.FloatField(db_column='growthEffectOfForexChangesOnCash', blank=True, null=True)  # Field name made lowercase.
    growthnetchangeincash = models.FloatField(db_column='growthNetChangeInCash', blank=True, null=True)  # Field name made lowercase.
    growthcashatendofperiod = models.FloatField(db_column='growthCashAtEndOfPeriod', blank=True, null=True)  # Field name made lowercase.
    growthcashatbeginningofperiod = models.FloatField(db_column='growthCashAtBeginningOfPeriod', blank=True, null=True)  # Field name made lowercase.
    growthoperatingcashflow = models.FloatField(db_column='growthOperatingCashFlow', blank=True, null=True)  # Field name made lowercase.
    growthcapitalexpenditure = models.FloatField(db_column='growthCapitalExpenditure', blank=True, null=True)  # Field name made lowercase.
    growthfreecashflow = models.FloatField(db_column='growthFreeCashFlow', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_cflowgrowth'


class TickAppCompany(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    isin = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    industry = models.CharField(max_length=200, blank=True, null=True)
    sector = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    market = models.CharField(max_length=200, blank=True, null=True)
    indexes = models.CharField(max_length=200, blank=True, null=True)
    ipo_date = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    delisted = models.IntegerField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'tick_app_company'


class TickAppDatatype(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    target_table = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'tick_app_datatype'


class TickAppDividend(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    label = models.CharField(max_length=200, blank=True, null=True)
    adjdividend = models.FloatField(db_column='adjDividend', blank=True, null=True)  # Field name made lowercase.
    dividend = models.FloatField(blank=True, null=True)
    recorddate = models.CharField(db_column='recordDate', max_length=200, blank=True, null=True)  # Field name made lowercase.
    paymentdate = models.CharField(db_column='paymentDate', max_length=200, blank=True, null=True)  # Field name made lowercase.
    declarationdate = models.CharField(db_column='declarationDate', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_dividend'


class TickAppEv(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    stockprice = models.FloatField(db_column='stockPrice', blank=True, null=True)  # Field name made lowercase.
    numberofshares = models.FloatField(db_column='numberOfShares', blank=True, null=True)  # Field name made lowercase.
    marketcapitalization = models.FloatField(db_column='marketCapitalization', blank=True, null=True)  # Field name made lowercase.
    minuscashandcashequivalents = models.FloatField(db_column='minusCashAndCashEquivalents', blank=True, null=True)  # Field name made lowercase.
    addtotaldebt = models.FloatField(db_column='addTotalDebt', blank=True, null=True)  # Field name made lowercase.
    enterprisevalue = models.FloatField(db_column='enterpriseValue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_ev'


class TickAppFingrowth(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    period = models.CharField(max_length=200, blank=True, null=True)
    revenuegrowth = models.FloatField(db_column='revenueGrowth', blank=True, null=True)  # Field name made lowercase.
    grossprofitgrowth = models.FloatField(db_column='grossProfitGrowth', blank=True, null=True)  # Field name made lowercase.
    ebitgrowth = models.FloatField(blank=True, null=True)
    operatingincomegrowth = models.FloatField(db_column='operatingIncomeGrowth', blank=True, null=True)  # Field name made lowercase.
    netincomegrowth = models.FloatField(db_column='netIncomeGrowth', blank=True, null=True)  # Field name made lowercase.
    epsgrowth = models.FloatField(blank=True, null=True)
    epsdilutedgrowth = models.FloatField(db_column='epsdilutedGrowth', blank=True, null=True)  # Field name made lowercase.
    weightedaveragesharesgrowth = models.FloatField(db_column='weightedAverageSharesGrowth', blank=True, null=True)  # Field name made lowercase.
    weightedaveragesharesdilutedgrowth = models.FloatField(db_column='weightedAverageSharesDilutedGrowth', blank=True, null=True)  # Field name made lowercase.
    dividendspersharegrowth = models.FloatField(db_column='dividendsperShareGrowth', blank=True, null=True)  # Field name made lowercase.
    operatingcashflowgrowth = models.FloatField(db_column='operatingCashFlowGrowth', blank=True, null=True)  # Field name made lowercase.
    freecashflowgrowth = models.FloatField(db_column='freeCashFlowGrowth', blank=True, null=True)  # Field name made lowercase.
    tenyrevenuegrowthpershare = models.FloatField(db_column='tenYRevenueGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    fiveyrevenuegrowthpershare = models.FloatField(db_column='fiveYRevenueGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    threeyrevenuegrowthpershare = models.FloatField(db_column='threeYRevenueGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    tenyoperatingcfgrowthpershare = models.FloatField(db_column='tenYOperatingCFGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    fiveyoperatingcfgrowthpershare = models.FloatField(db_column='fiveYOperatingCFGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    threeyoperatingcfgrowthpershare = models.FloatField(db_column='threeYOperatingCFGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    tenynetincomegrowthpershare = models.FloatField(db_column='tenYNetIncomeGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    fiveynetincomegrowthpershare = models.FloatField(db_column='fiveYNetIncomeGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    threeynetincomegrowthpershare = models.FloatField(db_column='threeYNetIncomeGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    tenyshareholdersequitygrowthpershare = models.FloatField(db_column='tenYShareholdersEquityGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    fiveyshareholdersequitygrowthpershare = models.FloatField(db_column='fiveYShareholdersEquityGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    threeyshareholdersequitygrowthpershare = models.FloatField(db_column='threeYShareholdersEquityGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    tenydividendpersharegrowthpershare = models.FloatField(db_column='tenYDividendperShareGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    fiveydividendpersharegrowthpershare = models.FloatField(db_column='fiveYDividendperShareGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    threeydividendpersharegrowthpershare = models.FloatField(db_column='threeYDividendperShareGrowthPerShare', blank=True, null=True)  # Field name made lowercase.
    receivablesgrowth = models.FloatField(db_column='receivablesGrowth', blank=True, null=True)  # Field name made lowercase.
    inventorygrowth = models.FloatField(db_column='inventoryGrowth', blank=True, null=True)  # Field name made lowercase.
    assetgrowth = models.FloatField(db_column='assetGrowth', blank=True, null=True)  # Field name made lowercase.
    bookvaluepersharegrowth = models.FloatField(db_column='bookValueperShareGrowth', blank=True, null=True)  # Field name made lowercase.
    debtgrowth = models.FloatField(db_column='debtGrowth', blank=True, null=True)  # Field name made lowercase.
    rdexpensegrowth = models.FloatField(db_column='rdexpenseGrowth', blank=True, null=True)  # Field name made lowercase.
    sgaexpensesgrowth = models.FloatField(db_column='sgaexpensesGrowth', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_fingrowth'


class TickAppIncome(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_id = models.CharField(max_length=200, blank=True, null=True)
    year = models.CharField(max_length=200, blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    costofrevenue = models.FloatField(db_column='costOfRevenue', blank=True, null=True)  # Field name made lowercase.
    grossprofit = models.FloatField(db_column='grossProfit', blank=True, null=True)  # Field name made lowercase.
    grossprofitratio = models.FloatField(db_column='grossProfitRatio', blank=True, null=True)  # Field name made lowercase.
    researchanddevelopmentexpenses = models.FloatField(db_column='researchAndDevelopmentExpenses', blank=True, null=True)  # Field name made lowercase.
    generalandadministrativeexpenses = models.FloatField(db_column='generalAndAdministrativeExpenses', blank=True, null=True)  # Field name made lowercase.
    sellingandmarketingexpenses = models.FloatField(db_column='sellingAndMarketingExpenses', blank=True, null=True)  # Field name made lowercase.
    otherexpenses = models.FloatField(db_column='otherExpenses', blank=True, null=True)  # Field name made lowercase.
    operatingexpenses = models.FloatField(db_column='operatingExpenses', blank=True, null=True)  # Field name made lowercase.
    costandexpenses = models.FloatField(db_column='costAndExpenses', blank=True, null=True)  # Field name made lowercase.
    interestexpense = models.FloatField(db_column='interestExpense', blank=True, null=True)  # Field name made lowercase.
    depreciationandamortization = models.FloatField(db_column='depreciationAndAmortization', blank=True, null=True)  # Field name made lowercase.
    ebitda = models.FloatField(blank=True, null=True)
    ebitdaratio = models.FloatField(blank=True, null=True)
    operatingincome = models.FloatField(db_column='operatingIncome', blank=True, null=True)  # Field name made lowercase.
    operatingincomeratio = models.FloatField(db_column='operatingIncomeRatio', blank=True, null=True)  # Field name made lowercase.
    totalotherincomeexpensesnet = models.FloatField(db_column='totalOtherIncomeExpensesNet', blank=True, null=True)  # Field name made lowercase.
    incomebeforetax = models.FloatField(db_column='incomeBeforeTax', blank=True, null=True)  # Field name made lowercase.
    incomebeforetaxratio = models.FloatField(db_column='incomeBeforeTaxRatio', blank=True, null=True)  # Field name made lowercase.
    incometaxexpense = models.FloatField(db_column='incomeTaxExpense', blank=True, null=True)  # Field name made lowercase.
    netincome = models.FloatField(db_column='netIncome', blank=True, null=True)  # Field name made lowercase.
    netincomeratio = models.FloatField(db_column='netIncomeRatio', blank=True, null=True)  # Field name made lowercase.
    eps = models.FloatField(blank=True, null=True)
    epsdiluted = models.FloatField(blank=True, null=True)
    weightedaverageshsout = models.FloatField(db_column='weightedAverageShsOut', blank=True, null=True)  # Field name made lowercase.
    weightedaverageshsoutdil = models.FloatField(db_column='weightedAverageShsOutDil', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_income'


class TickAppIncomegrowth(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    period = models.CharField(max_length=200, blank=True, null=True)
    growthrevenue = models.FloatField(db_column='growthRevenue', blank=True, null=True)  # Field name made lowercase.
    growthcostofrevenue = models.FloatField(db_column='growthCostOfRevenue', blank=True, null=True)  # Field name made lowercase.
    growthgrossprofit = models.FloatField(db_column='growthGrossProfit', blank=True, null=True)  # Field name made lowercase.
    growthgrossprofitratio = models.FloatField(db_column='growthGrossProfitRatio', blank=True, null=True)  # Field name made lowercase.
    growthresearchanddevelopmentexpenses = models.FloatField(db_column='growthResearchAndDevelopmentExpenses', blank=True, null=True)  # Field name made lowercase.
    growthgeneralandadministrativeexpenses = models.FloatField(db_column='growthGeneralAndAdministrativeExpenses', blank=True, null=True)  # Field name made lowercase.
    growthsellingandmarketingexpenses = models.FloatField(db_column='growthSellingAndMarketingExpenses', blank=True, null=True)  # Field name made lowercase.
    growthotherexpenses = models.FloatField(db_column='growthOtherExpenses', blank=True, null=True)  # Field name made lowercase.
    growthoperatingexpenses = models.FloatField(db_column='growthOperatingExpenses', blank=True, null=True)  # Field name made lowercase.
    growthcostandexpenses = models.FloatField(db_column='growthCostAndExpenses', blank=True, null=True)  # Field name made lowercase.
    growthinterestexpense = models.FloatField(db_column='growthInterestExpense', blank=True, null=True)  # Field name made lowercase.
    growthdepreciationandamortization = models.FloatField(db_column='growthDepreciationAndAmortization', blank=True, null=True)  # Field name made lowercase.
    growthebitda = models.FloatField(db_column='growthEBITDA', blank=True, null=True)  # Field name made lowercase.
    growthebitdaratio = models.FloatField(db_column='growthEBITDARatio', blank=True, null=True)  # Field name made lowercase.
    growthoperatingincome = models.FloatField(db_column='growthOperatingIncome', blank=True, null=True)  # Field name made lowercase.
    growthoperatingincomeratio = models.FloatField(db_column='growthOperatingIncomeRatio', blank=True, null=True)  # Field name made lowercase.
    growthtotalotherincomeexpensesnet = models.FloatField(db_column='growthTotalOtherIncomeExpensesNet', blank=True, null=True)  # Field name made lowercase.
    growthincomebeforetax = models.FloatField(db_column='growthIncomeBeforeTax', blank=True, null=True)  # Field name made lowercase.
    growthincomebeforetaxratio = models.FloatField(db_column='growthIncomeBeforeTaxRatio', blank=True, null=True)  # Field name made lowercase.
    growthincometaxexpense = models.FloatField(db_column='growthIncomeTaxExpense', blank=True, null=True)  # Field name made lowercase.
    growthnetincome = models.FloatField(db_column='growthNetIncome', blank=True, null=True)  # Field name made lowercase.
    growthnetincomeratio = models.FloatField(db_column='growthNetIncomeRatio', blank=True, null=True)  # Field name made lowercase.
    growtheps = models.FloatField(db_column='growthEPS', blank=True, null=True)  # Field name made lowercase.
    growthepsdiluted = models.FloatField(db_column='growthEPSDiluted', blank=True, null=True)  # Field name made lowercase.
    growthweightedaverageshsout = models.FloatField(db_column='growthWeightedAverageShsOut', blank=True, null=True)  # Field name made lowercase.
    growthweightedaverageshsoutdil = models.FloatField(db_column='growthWeightedAverageShsOutDil', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_incomegrowth'


class TickAppInstitutional(models.Model):
    id = models.BigAutoField(primary_key=True)
    holder = models.CharField(max_length=200, blank=True, null=True)
    shares = models.FloatField(blank=True, null=True)
    datereported = models.CharField(db_column='dateReported', max_length=200, blank=True, null=True)  # Field name made lowercase.
    change = models.FloatField(blank=True, null=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tick_app_institutional'


class TickAppKeyexecutives(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    pay = models.FloatField(blank=True, null=True)
    currencypay = models.CharField(db_column='currencyPay', max_length=200, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=200, blank=True, null=True)
    yearborn = models.CharField(db_column='yearBorn', max_length=200, blank=True, null=True)  # Field name made lowercase.
    titlesince = models.CharField(db_column='titleSince', max_length=200, blank=True, null=True)  # Field name made lowercase.
    symbol = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tick_app_keyexecutives'


class TickAppKeymetrics(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    period = models.CharField(max_length=200, blank=True, null=True)
    revenuepershare = models.FloatField(db_column='revenuePerShare', blank=True, null=True)  # Field name made lowercase.
    netincomepershare = models.FloatField(db_column='netIncomePerShare', blank=True, null=True)  # Field name made lowercase.
    operatingcashflowpershare = models.FloatField(db_column='operatingCashFlowPerShare', blank=True, null=True)  # Field name made lowercase.
    freecashflowpershare = models.FloatField(db_column='freeCashFlowPerShare', blank=True, null=True)  # Field name made lowercase.
    cashpershare = models.FloatField(db_column='cashPerShare', blank=True, null=True)  # Field name made lowercase.
    bookvaluepershare = models.FloatField(db_column='bookValuePerShare', blank=True, null=True)  # Field name made lowercase.
    tangiblebookvaluepershare = models.FloatField(db_column='tangibleBookValuePerShare', blank=True, null=True)  # Field name made lowercase.
    shareholdersequitypershare = models.FloatField(db_column='shareholdersEquityPerShare', blank=True, null=True)  # Field name made lowercase.
    interestdebtpershare = models.FloatField(db_column='interestDebtPerShare', blank=True, null=True)  # Field name made lowercase.
    marketcap = models.FloatField(db_column='marketCap', blank=True, null=True)  # Field name made lowercase.
    enterprisevalue = models.FloatField(db_column='enterpriseValue', blank=True, null=True)  # Field name made lowercase.
    peratio = models.FloatField(db_column='peRatio', blank=True, null=True)  # Field name made lowercase.
    pricetosalesratio = models.FloatField(db_column='priceToSalesRatio', blank=True, null=True)  # Field name made lowercase.
    pocfratio = models.FloatField(blank=True, null=True)
    pfcfratio = models.FloatField(db_column='pfcfRatio', blank=True, null=True)  # Field name made lowercase.
    pbratio = models.FloatField(db_column='pbRatio', blank=True, null=True)  # Field name made lowercase.
    ptbratio = models.FloatField(db_column='ptbRatio', blank=True, null=True)  # Field name made lowercase.
    evtosales = models.FloatField(db_column='evToSales', blank=True, null=True)  # Field name made lowercase.
    enterprisevalueoverebitda = models.FloatField(db_column='enterpriseValueOverEBITDA', blank=True, null=True)  # Field name made lowercase.
    evtooperatingcashflow = models.FloatField(db_column='evToOperatingCashFlow', blank=True, null=True)  # Field name made lowercase.
    evtofreecashflow = models.FloatField(db_column='evToFreeCashFlow', blank=True, null=True)  # Field name made lowercase.
    earningsyield = models.FloatField(db_column='earningsYield', blank=True, null=True)  # Field name made lowercase.
    freecashflowyield = models.FloatField(db_column='freeCashFlowYield', blank=True, null=True)  # Field name made lowercase.
    debttoequity = models.FloatField(db_column='debtToEquity', blank=True, null=True)  # Field name made lowercase.
    debttoassets = models.FloatField(db_column='debtToAssets', blank=True, null=True)  # Field name made lowercase.
    netdebttoebitda = models.FloatField(db_column='netDebtToEBITDA', blank=True, null=True)  # Field name made lowercase.
    currentratio = models.FloatField(db_column='currentRatio', blank=True, null=True)  # Field name made lowercase.
    interestcoverage = models.FloatField(db_column='interestCoverage', blank=True, null=True)  # Field name made lowercase.
    incomequality = models.FloatField(db_column='incomeQuality', blank=True, null=True)  # Field name made lowercase.
    dividendyield = models.FloatField(db_column='dividendYield', blank=True, null=True)  # Field name made lowercase.
    payoutratio = models.FloatField(db_column='payoutRatio', blank=True, null=True)  # Field name made lowercase.
    salesgeneralandadministrativetorevenue = models.FloatField(db_column='salesGeneralAndAdministrativeToRevenue', blank=True, null=True)  # Field name made lowercase.
    researchandddevelopementtorevenue = models.FloatField(db_column='researchAndDdevelopementToRevenue', blank=True, null=True)  # Field name made lowercase.
    intangiblestototalassets = models.FloatField(db_column='intangiblesToTotalAssets', blank=True, null=True)  # Field name made lowercase.
    capextooperatingcashflow = models.FloatField(db_column='capexToOperatingCashFlow', blank=True, null=True)  # Field name made lowercase.
    capextorevenue = models.FloatField(db_column='capexToRevenue', blank=True, null=True)  # Field name made lowercase.
    capextodepreciation = models.FloatField(db_column='capexToDepreciation', blank=True, null=True)  # Field name made lowercase.
    stockbasedcompensationtorevenue = models.FloatField(db_column='stockBasedCompensationToRevenue', blank=True, null=True)  # Field name made lowercase.
    grahamnumber = models.FloatField(db_column='grahamNumber', blank=True, null=True)  # Field name made lowercase.
    roic = models.FloatField(blank=True, null=True)
    returnontangibleassets = models.FloatField(db_column='returnOnTangibleAssets', blank=True, null=True)  # Field name made lowercase.
    grahamnetnet = models.FloatField(db_column='grahamNetNet', blank=True, null=True)  # Field name made lowercase.
    workingcapital = models.FloatField(db_column='workingCapital', blank=True, null=True)  # Field name made lowercase.
    tangibleassetvalue = models.FloatField(db_column='tangibleAssetValue', blank=True, null=True)  # Field name made lowercase.
    netcurrentassetvalue = models.FloatField(db_column='netCurrentAssetValue', blank=True, null=True)  # Field name made lowercase.
    investedcapital = models.FloatField(db_column='investedCapital', blank=True, null=True)  # Field name made lowercase.
    averagereceivables = models.FloatField(db_column='averageReceivables', blank=True, null=True)  # Field name made lowercase.
    averagepayables = models.FloatField(db_column='averagePayables', blank=True, null=True)  # Field name made lowercase.
    averageinventory = models.FloatField(db_column='averageInventory', blank=True, null=True)  # Field name made lowercase.
    dayssalesoutstanding = models.FloatField(db_column='daysSalesOutstanding', blank=True, null=True)  # Field name made lowercase.
    dayspayablesoutstanding = models.FloatField(db_column='daysPayablesOutstanding', blank=True, null=True)  # Field name made lowercase.
    daysofinventoryonhand = models.FloatField(db_column='daysOfInventoryOnHand', blank=True, null=True)  # Field name made lowercase.
    receivablesturnover = models.FloatField(db_column='receivablesTurnover', blank=True, null=True)  # Field name made lowercase.
    payablesturnover = models.FloatField(db_column='payablesTurnover', blank=True, null=True)  # Field name made lowercase.
    inventoryturnover = models.FloatField(db_column='inventoryTurnover', blank=True, null=True)  # Field name made lowercase.
    roe = models.FloatField(blank=True, null=True)
    capexpershare = models.FloatField(db_column='capexPerShare', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_keymetrics'


class TickAppKeymetricsttm(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    revenuepersharettm = models.FloatField(db_column='revenuePerShareTTM', blank=True, null=True)  # Field name made lowercase.
    netincomepersharettm = models.FloatField(db_column='netIncomePerShareTTM', blank=True, null=True)  # Field name made lowercase.
    operatingcashflowpersharettm = models.FloatField(db_column='operatingCashFlowPerShareTTM', blank=True, null=True)  # Field name made lowercase.
    freecashflowpersharettm = models.FloatField(db_column='freeCashFlowPerShareTTM', blank=True, null=True)  # Field name made lowercase.
    cashpersharettm = models.FloatField(db_column='cashPerShareTTM', blank=True, null=True)  # Field name made lowercase.
    bookvaluepersharettm = models.FloatField(db_column='bookValuePerShareTTM', blank=True, null=True)  # Field name made lowercase.
    tangiblebookvaluepersharettm = models.FloatField(db_column='tangibleBookValuePerShareTTM', blank=True, null=True)  # Field name made lowercase.
    shareholdersequitypersharettm = models.FloatField(db_column='shareholdersEquityPerShareTTM', blank=True, null=True)  # Field name made lowercase.
    interestdebtpersharettm = models.FloatField(db_column='interestDebtPerShareTTM', blank=True, null=True)  # Field name made lowercase.
    marketcapttm = models.FloatField(db_column='marketCapTTM', blank=True, null=True)  # Field name made lowercase.
    enterprisevaluettm = models.FloatField(db_column='enterpriseValueTTM', blank=True, null=True)  # Field name made lowercase.
    peratiottm = models.FloatField(db_column='peRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pricetosalesratiottm = models.FloatField(db_column='priceToSalesRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pocfratiottm = models.FloatField(db_column='pocfratioTTM', blank=True, null=True)  # Field name made lowercase.
    pfcfratiottm = models.FloatField(db_column='pfcfRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pbratiottm = models.FloatField(db_column='pbRatioTTM', blank=True, null=True)  # Field name made lowercase.
    ptbratiottm = models.FloatField(db_column='ptbRatioTTM', blank=True, null=True)  # Field name made lowercase.
    evtosalesttm = models.FloatField(db_column='evToSalesTTM', blank=True, null=True)  # Field name made lowercase.
    enterprisevalueoverebitdattm = models.FloatField(db_column='enterpriseValueOverEBITDATTM', blank=True, null=True)  # Field name made lowercase.
    evtooperatingcashflowttm = models.FloatField(db_column='evToOperatingCashFlowTTM', blank=True, null=True)  # Field name made lowercase.
    evtofreecashflowttm = models.FloatField(db_column='evToFreeCashFlowTTM', blank=True, null=True)  # Field name made lowercase.
    earningsyieldttm = models.FloatField(db_column='earningsYieldTTM', blank=True, null=True)  # Field name made lowercase.
    freecashflowyieldttm = models.FloatField(db_column='freeCashFlowYieldTTM', blank=True, null=True)  # Field name made lowercase.
    debttoequityttm = models.FloatField(db_column='debtToEquityTTM', blank=True, null=True)  # Field name made lowercase.
    debttoassetsttm = models.FloatField(db_column='debtToAssetsTTM', blank=True, null=True)  # Field name made lowercase.
    netdebttoebitdattm = models.FloatField(db_column='netDebtToEBITDATTM', blank=True, null=True)  # Field name made lowercase.
    currentratiottm = models.FloatField(db_column='currentRatioTTM', blank=True, null=True)  # Field name made lowercase.
    interestcoveragettm = models.FloatField(db_column='interestCoverageTTM', blank=True, null=True)  # Field name made lowercase.
    incomequalityttm = models.FloatField(db_column='incomeQualityTTM', blank=True, null=True)  # Field name made lowercase.
    dividendyieldttm = models.FloatField(db_column='dividendYieldTTM', blank=True, null=True)  # Field name made lowercase.
    dividendyieldpercentagettm = models.FloatField(db_column='dividendYieldPercentageTTM', blank=True, null=True)  # Field name made lowercase.
    payoutratiottm = models.FloatField(db_column='payoutRatioTTM', blank=True, null=True)  # Field name made lowercase.
    salesgeneralandadministrativetorevenuettm = models.FloatField(db_column='salesGeneralAndAdministrativeToRevenueTTM', blank=True, null=True)  # Field name made lowercase.
    researchanddevelopementtorevenuettm = models.FloatField(db_column='researchAndDevelopementToRevenueTTM', blank=True, null=True)  # Field name made lowercase.
    intangiblestototalassetsttm = models.FloatField(db_column='intangiblesToTotalAssetsTTM', blank=True, null=True)  # Field name made lowercase.
    capextooperatingcashflowttm = models.FloatField(db_column='capexToOperatingCashFlowTTM', blank=True, null=True)  # Field name made lowercase.
    capextorevenuettm = models.FloatField(db_column='capexToRevenueTTM', blank=True, null=True)  # Field name made lowercase.
    capextodepreciationttm = models.FloatField(db_column='capexToDepreciationTTM', blank=True, null=True)  # Field name made lowercase.
    stockbasedcompensationtorevenuettm = models.FloatField(db_column='stockBasedCompensationToRevenueTTM', blank=True, null=True)  # Field name made lowercase.
    grahamnumberttm = models.FloatField(db_column='grahamNumberTTM', blank=True, null=True)  # Field name made lowercase.
    roicttm = models.FloatField(db_column='roicTTM', blank=True, null=True)  # Field name made lowercase.
    returnontangibleassetsttm = models.FloatField(db_column='returnOnTangibleAssetsTTM', blank=True, null=True)  # Field name made lowercase.
    grahamnetnetttm = models.FloatField(db_column='grahamNetNetTTM', blank=True, null=True)  # Field name made lowercase.
    workingcapitalttm = models.FloatField(db_column='workingCapitalTTM', blank=True, null=True)  # Field name made lowercase.
    tangibleassetvaluettm = models.FloatField(db_column='tangibleAssetValueTTM', blank=True, null=True)  # Field name made lowercase.
    netcurrentassetvaluettm = models.FloatField(db_column='netCurrentAssetValueTTM', blank=True, null=True)  # Field name made lowercase.
    investedcapitalttm = models.FloatField(db_column='investedCapitalTTM', blank=True, null=True)  # Field name made lowercase.
    averagereceivablesttm = models.FloatField(db_column='averageReceivablesTTM', blank=True, null=True)  # Field name made lowercase.
    averagepayablesttm = models.FloatField(db_column='averagePayablesTTM', blank=True, null=True)  # Field name made lowercase.
    averageinventoryttm = models.FloatField(db_column='averageInventoryTTM', blank=True, null=True)  # Field name made lowercase.
    dayssalesoutstandingttm = models.FloatField(db_column='daysSalesOutstandingTTM', blank=True, null=True)  # Field name made lowercase.
    dayspayablesoutstandingttm = models.FloatField(db_column='daysPayablesOutstandingTTM', blank=True, null=True)  # Field name made lowercase.
    daysofinventoryonhandttm = models.FloatField(db_column='daysOfInventoryOnHandTTM', blank=True, null=True)  # Field name made lowercase.
    receivablesturnoverttm = models.FloatField(db_column='receivablesTurnoverTTM', blank=True, null=True)  # Field name made lowercase.
    payablesturnoverttm = models.FloatField(db_column='payablesTurnoverTTM', blank=True, null=True)  # Field name made lowercase.
    inventoryturnoverttm = models.FloatField(db_column='inventoryTurnoverTTM', blank=True, null=True)  # Field name made lowercase.
    roettm = models.FloatField(db_column='roeTTM', blank=True, null=True)  # Field name made lowercase.
    capexpersharettm = models.FloatField(db_column='capexPerShareTTM', blank=True, null=True)  # Field name made lowercase.
    dividendpersharettm = models.FloatField(db_column='dividendPerShareTTM', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_keymetricsttm'


class TickAppMutualfund(models.Model):
    id = models.BigAutoField(primary_key=True)
    holder = models.CharField(max_length=200, blank=True, null=True)
    shares = models.FloatField(blank=True, null=True)
    datereported = models.CharField(db_column='dateReported', max_length=200, blank=True, null=True)  # Field name made lowercase.
    change = models.FloatField(blank=True, null=True)
    weightpercent = models.FloatField(db_column='weightPercent', blank=True, null=True)  # Field name made lowercase.
    symbol = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tick_app_mutualfund'


class TickAppPeers(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    peerslist = models.CharField(db_column='peersList', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_peers'


class TickAppPrice(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    adjclose = models.FloatField(db_column='adjClose', blank=True, null=True)  # Field name made lowercase.
    volume = models.FloatField(blank=True, null=True)
    unadjustedvolume = models.FloatField(db_column='unadjustedVolume', blank=True, null=True)  # Field name made lowercase.
    change = models.FloatField(blank=True, null=True)
    changepercent = models.FloatField(db_column='changePercent', blank=True, null=True)  # Field name made lowercase.
    vwap = models.FloatField(blank=True, null=True)
    label = models.CharField(max_length=200, blank=True, null=True)
    changeovertime = models.FloatField(db_column='changeOverTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_price'


class TickAppProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    beta = models.FloatField(blank=True, null=True)
    volavg = models.FloatField(db_column='volAvg', blank=True, null=True)  # Field name made lowercase.
    mktcap = models.FloatField(db_column='mktCap', blank=True, null=True)  # Field name made lowercase.
    lastdiv = models.FloatField(db_column='lastDiv', blank=True, null=True)  # Field name made lowercase.
    range = models.CharField(max_length=200, blank=True, null=True)
    changes = models.FloatField(blank=True, null=True)
    companyname = models.CharField(db_column='companyName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    currency = models.CharField(max_length=200, blank=True, null=True)
    cik = models.CharField(max_length=200, blank=True, null=True)
    isin = models.CharField(max_length=200, blank=True, null=True)
    cusip = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    exchangeshortname = models.CharField(db_column='exchangeShortName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    industry = models.CharField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    ceo = models.CharField(max_length=200, blank=True, null=True)
    sector = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    fulltimeemployees = models.FloatField(db_column='fullTimeEmployees', blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    zip = models.CharField(max_length=200, blank=True, null=True)
    dcfdiff = models.FloatField(db_column='dcfDiff', blank=True, null=True)  # Field name made lowercase.
    dcf = models.FloatField(blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    ipodate = models.CharField(db_column='ipoDate', max_length=200, blank=True, null=True)  # Field name made lowercase.
    defaultimage = models.CharField(db_column='defaultImage', max_length=200, blank=True, null=True)  # Field name made lowercase.
    isetf = models.CharField(db_column='isEtf', max_length=200, blank=True, null=True)  # Field name made lowercase.
    isactivelytrading = models.CharField(db_column='isActivelyTrading', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_profile'


class TickAppRatios(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    period = models.CharField(max_length=200, blank=True, null=True)
    currentratio = models.FloatField(db_column='currentRatio', blank=True, null=True)  # Field name made lowercase.
    quickratio = models.FloatField(db_column='quickRatio', blank=True, null=True)  # Field name made lowercase.
    cashratio = models.FloatField(db_column='cashRatio', blank=True, null=True)  # Field name made lowercase.
    daysofsalesoutstanding = models.FloatField(db_column='daysOfSalesOutstanding', blank=True, null=True)  # Field name made lowercase.
    daysofinventoryoutstanding = models.FloatField(db_column='daysOfInventoryOutstanding', blank=True, null=True)  # Field name made lowercase.
    operatingcycle = models.FloatField(db_column='operatingCycle', blank=True, null=True)  # Field name made lowercase.
    daysofpayablesoutstanding = models.FloatField(db_column='daysOfPayablesOutstanding', blank=True, null=True)  # Field name made lowercase.
    cashconversioncycle = models.FloatField(db_column='cashConversionCycle', blank=True, null=True)  # Field name made lowercase.
    grossprofitmargin = models.FloatField(db_column='grossProfitMargin', blank=True, null=True)  # Field name made lowercase.
    operatingprofitmargin = models.FloatField(db_column='operatingProfitMargin', blank=True, null=True)  # Field name made lowercase.
    pretaxprofitmargin = models.FloatField(db_column='pretaxProfitMargin', blank=True, null=True)  # Field name made lowercase.
    netprofitmargin = models.FloatField(db_column='netProfitMargin', blank=True, null=True)  # Field name made lowercase.
    effectivetaxrate = models.FloatField(db_column='effectiveTaxRate', blank=True, null=True)  # Field name made lowercase.
    returnonassets = models.FloatField(db_column='returnOnAssets', blank=True, null=True)  # Field name made lowercase.
    returnonequity = models.FloatField(db_column='returnOnEquity', blank=True, null=True)  # Field name made lowercase.
    returnoncapitalemployed = models.FloatField(db_column='returnOnCapitalEmployed', blank=True, null=True)  # Field name made lowercase.
    netincomeperebt = models.FloatField(db_column='netIncomePerEBT', blank=True, null=True)  # Field name made lowercase.
    ebtperebit = models.FloatField(db_column='ebtPerEbit', blank=True, null=True)  # Field name made lowercase.
    ebitperrevenue = models.FloatField(db_column='ebitPerRevenue', blank=True, null=True)  # Field name made lowercase.
    debtratio = models.FloatField(db_column='debtRatio', blank=True, null=True)  # Field name made lowercase.
    debtequityratio = models.FloatField(db_column='debtEquityRatio', blank=True, null=True)  # Field name made lowercase.
    longtermdebttocapitalization = models.FloatField(db_column='longTermDebtToCapitalization', blank=True, null=True)  # Field name made lowercase.
    totaldebttocapitalization = models.FloatField(db_column='totalDebtToCapitalization', blank=True, null=True)  # Field name made lowercase.
    interestcoverage = models.FloatField(db_column='interestCoverage', blank=True, null=True)  # Field name made lowercase.
    cashflowtodebtratio = models.FloatField(db_column='cashFlowToDebtRatio', blank=True, null=True)  # Field name made lowercase.
    companyequitymultiplier = models.FloatField(db_column='companyEquityMultiplier', blank=True, null=True)  # Field name made lowercase.
    receivablesturnover = models.FloatField(db_column='receivablesTurnover', blank=True, null=True)  # Field name made lowercase.
    payablesturnover = models.FloatField(db_column='payablesTurnover', blank=True, null=True)  # Field name made lowercase.
    inventoryturnover = models.FloatField(db_column='inventoryTurnover', blank=True, null=True)  # Field name made lowercase.
    fixedassetturnover = models.FloatField(db_column='fixedAssetTurnover', blank=True, null=True)  # Field name made lowercase.
    assetturnover = models.FloatField(db_column='assetTurnover', blank=True, null=True)  # Field name made lowercase.
    operatingcashflowpershare = models.FloatField(db_column='operatingCashFlowPerShare', blank=True, null=True)  # Field name made lowercase.
    freecashflowpershare = models.FloatField(db_column='freeCashFlowPerShare', blank=True, null=True)  # Field name made lowercase.
    cashpershare = models.FloatField(db_column='cashPerShare', blank=True, null=True)  # Field name made lowercase.
    payoutratio = models.FloatField(db_column='payoutRatio', blank=True, null=True)  # Field name made lowercase.
    operatingcashflowsalesratio = models.FloatField(db_column='operatingCashFlowSalesRatio', blank=True, null=True)  # Field name made lowercase.
    freecashflowoperatingcashflowratio = models.FloatField(db_column='freeCashFlowOperatingCashFlowRatio', blank=True, null=True)  # Field name made lowercase.
    cashflowcoverageratios = models.FloatField(db_column='cashFlowCoverageRatios', blank=True, null=True)  # Field name made lowercase.
    shorttermcoverageratios = models.FloatField(db_column='shortTermCoverageRatios', blank=True, null=True)  # Field name made lowercase.
    capitalexpenditurecoverageratio = models.FloatField(db_column='capitalExpenditureCoverageRatio', blank=True, null=True)  # Field name made lowercase.
    dividendpaidandcapexcoverageratio = models.FloatField(db_column='dividendPaidAndCapexCoverageRatio', blank=True, null=True)  # Field name made lowercase.
    dividendpayoutratio = models.FloatField(db_column='dividendPayoutRatio', blank=True, null=True)  # Field name made lowercase.
    pricebookvalueratio = models.FloatField(db_column='priceBookValueRatio', blank=True, null=True)  # Field name made lowercase.
    pricetobookratio = models.FloatField(db_column='priceToBookRatio', blank=True, null=True)  # Field name made lowercase.
    pricetosalesratio = models.FloatField(db_column='priceToSalesRatio', blank=True, null=True)  # Field name made lowercase.
    priceearningsratio = models.FloatField(db_column='priceEarningsRatio', blank=True, null=True)  # Field name made lowercase.
    pricetofreecashflowsratio = models.FloatField(db_column='priceToFreeCashFlowsRatio', blank=True, null=True)  # Field name made lowercase.
    pricetooperatingcashflowsratio = models.FloatField(db_column='priceToOperatingCashFlowsRatio', blank=True, null=True)  # Field name made lowercase.
    pricecashflowratio = models.FloatField(db_column='priceCashFlowRatio', blank=True, null=True)  # Field name made lowercase.
    priceearningstogrowthratio = models.FloatField(db_column='priceEarningsToGrowthRatio', blank=True, null=True)  # Field name made lowercase.
    pricesalesratio = models.FloatField(db_column='priceSalesRatio', blank=True, null=True)  # Field name made lowercase.
    dividendyield = models.FloatField(db_column='dividendYield', blank=True, null=True)  # Field name made lowercase.
    enterprisevaluemultiple = models.FloatField(db_column='enterpriseValueMultiple', blank=True, null=True)  # Field name made lowercase.
    pricefairvalue = models.FloatField(db_column='priceFairValue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_ratios'


class TickAppRatiosttm(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=200, blank=True, null=True)
    dividendyielttm = models.FloatField(db_column='dividendYielTTM', blank=True, null=True)  # Field name made lowercase.
    dividendyielpercentagettm = models.FloatField(db_column='dividendYielPercentageTTM', blank=True, null=True)  # Field name made lowercase.
    peratiottm = models.FloatField(db_column='peRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pegratiottm = models.FloatField(db_column='pegRatioTTM', blank=True, null=True)  # Field name made lowercase.
    payoutratiottm = models.FloatField(db_column='payoutRatioTTM', blank=True, null=True)  # Field name made lowercase.
    currentratiottm = models.FloatField(db_column='currentRatioTTM', blank=True, null=True)  # Field name made lowercase.
    quickratiottm = models.FloatField(db_column='quickRatioTTM', blank=True, null=True)  # Field name made lowercase.
    cashratiottm = models.FloatField(db_column='cashRatioTTM', blank=True, null=True)  # Field name made lowercase.
    daysofsalesoutstandingttm = models.FloatField(db_column='daysOfSalesOutstandingTTM', blank=True, null=True)  # Field name made lowercase.
    daysofinventoryoutstandingttm = models.FloatField(db_column='daysOfInventoryOutstandingTTM', blank=True, null=True)  # Field name made lowercase.
    operatingcyclettm = models.FloatField(db_column='operatingCycleTTM', blank=True, null=True)  # Field name made lowercase.
    daysofpayablesoutstandingttm = models.FloatField(db_column='daysOfPayablesOutstandingTTM', blank=True, null=True)  # Field name made lowercase.
    cashconversioncyclettm = models.FloatField(db_column='cashConversionCycleTTM', blank=True, null=True)  # Field name made lowercase.
    grossprofitmarginttm = models.FloatField(db_column='grossProfitMarginTTM', blank=True, null=True)  # Field name made lowercase.
    operatingprofitmarginttm = models.FloatField(db_column='operatingProfitMarginTTM', blank=True, null=True)  # Field name made lowercase.
    pretaxprofitmarginttm = models.FloatField(db_column='pretaxProfitMarginTTM', blank=True, null=True)  # Field name made lowercase.
    netprofitmarginttm = models.FloatField(db_column='netProfitMarginTTM', blank=True, null=True)  # Field name made lowercase.
    effectivetaxratettm = models.FloatField(db_column='effectiveTaxRateTTM', blank=True, null=True)  # Field name made lowercase.
    returnonassetsttm = models.FloatField(db_column='returnOnAssetsTTM', blank=True, null=True)  # Field name made lowercase.
    returnonequityttm = models.FloatField(db_column='returnOnEquityTTM', blank=True, null=True)  # Field name made lowercase.
    returnoncapitalemployedttm = models.FloatField(db_column='returnOnCapitalEmployedTTM', blank=True, null=True)  # Field name made lowercase.
    netincomeperebtttm = models.FloatField(db_column='netIncomePerEBTTTM', blank=True, null=True)  # Field name made lowercase.
    ebtperebitttm = models.FloatField(db_column='ebtPerEbitTTM', blank=True, null=True)  # Field name made lowercase.
    ebitperrevenuettm = models.FloatField(db_column='ebitPerRevenueTTM', blank=True, null=True)  # Field name made lowercase.
    debtratiottm = models.FloatField(db_column='debtRatioTTM', blank=True, null=True)  # Field name made lowercase.
    debtequityratiottm = models.FloatField(db_column='debtEquityRatioTTM', blank=True, null=True)  # Field name made lowercase.
    longtermdebttocapitalizationttm = models.FloatField(db_column='longTermDebtToCapitalizationTTM', blank=True, null=True)  # Field name made lowercase.
    totaldebttocapitalizationttm = models.FloatField(db_column='totalDebtToCapitalizationTTM', blank=True, null=True)  # Field name made lowercase.
    interestcoveragettm = models.FloatField(db_column='interestCoverageTTM', blank=True, null=True)  # Field name made lowercase.
    cashflowtodebtratiottm = models.FloatField(db_column='cashFlowToDebtRatioTTM', blank=True, null=True)  # Field name made lowercase.
    companyequitymultiplierttm = models.FloatField(db_column='companyEquityMultiplierTTM', blank=True, null=True)  # Field name made lowercase.
    receivablesturnoverttm = models.FloatField(db_column='receivablesTurnoverTTM', blank=True, null=True)  # Field name made lowercase.
    payablesturnoverttm = models.FloatField(db_column='payablesTurnoverTTM', blank=True, null=True)  # Field name made lowercase.
    inventoryturnoverttm = models.FloatField(db_column='inventoryTurnoverTTM', blank=True, null=True)  # Field name made lowercase.
    fixedassetturnoverttm = models.FloatField(db_column='fixedAssetTurnoverTTM', blank=True, null=True)  # Field name made lowercase.
    assetturnoverttm = models.FloatField(db_column='assetTurnoverTTM', blank=True, null=True)  # Field name made lowercase.
    operatingcashflowpersharettm = models.FloatField(db_column='operatingCashFlowPerShareTTM', blank=True, null=True)  # Field name made lowercase.
    freecashflowpersharettm = models.FloatField(db_column='freeCashFlowPerShareTTM', blank=True, null=True)  # Field name made lowercase.
    cashpersharettm = models.FloatField(db_column='cashPerShareTTM', blank=True, null=True)  # Field name made lowercase.
    operatingcashflowsalesratiottm = models.FloatField(db_column='operatingCashFlowSalesRatioTTM', blank=True, null=True)  # Field name made lowercase.
    freecashflowoperatingcashflowratiottm = models.FloatField(db_column='freeCashFlowOperatingCashFlowRatioTTM', blank=True, null=True)  # Field name made lowercase.
    cashflowcoverageratiosttm = models.FloatField(db_column='cashFlowCoverageRatiosTTM', blank=True, null=True)  # Field name made lowercase.
    shorttermcoverageratiosttm = models.FloatField(db_column='shortTermCoverageRatiosTTM', blank=True, null=True)  # Field name made lowercase.
    capitalexpenditurecoverageratiottm = models.FloatField(db_column='capitalExpenditureCoverageRatioTTM', blank=True, null=True)  # Field name made lowercase.
    dividendpaidandcapexcoverageratiottm = models.FloatField(db_column='dividendPaidAndCapexCoverageRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pricebookvalueratiottm = models.FloatField(db_column='priceBookValueRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pricetobookratiottm = models.FloatField(db_column='priceToBookRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pricetosalesratiottm = models.FloatField(db_column='priceToSalesRatioTTM', blank=True, null=True)  # Field name made lowercase.
    priceearningsratiottm = models.FloatField(db_column='priceEarningsRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pricetofreecashflowsratiottm = models.FloatField(db_column='priceToFreeCashFlowsRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pricetooperatingcashflowsratiottm = models.FloatField(db_column='priceToOperatingCashFlowsRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pricecashflowratiottm = models.FloatField(db_column='priceCashFlowRatioTTM', blank=True, null=True)  # Field name made lowercase.
    priceearningstogrowthratiottm = models.FloatField(db_column='priceEarningsToGrowthRatioTTM', blank=True, null=True)  # Field name made lowercase.
    pricesalesratiottm = models.FloatField(db_column='priceSalesRatioTTM', blank=True, null=True)  # Field name made lowercase.
    dividendyieldttm = models.FloatField(db_column='dividendYieldTTM', blank=True, null=True)  # Field name made lowercase.
    enterprisevaluemultiplettm = models.FloatField(db_column='enterpriseValueMultipleTTM', blank=True, null=True)  # Field name made lowercase.
    pricefairvaluettm = models.FloatField(db_column='priceFairValueTTM', blank=True, null=True)  # Field name made lowercase.
    dividendpersharettm = models.FloatField(db_column='dividendPerShareTTM', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tick_app_ratiosttm'


class TickAppYearlimit(models.Model):
    id = models.BigAutoField(primary_key=True)
    limit = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'tick_app_yearlimit'

class TickAppMetricsList(models.Model):
    id = models.BigAutoField(primary_key=True)
    metric = models.CharField(max_length=64)
    source = models.CharField(max_length=64)
    tool = models.CharField(max_length=64)
    measure = models.CharField(max_length=64)
    category = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'tick_app_metricslist'

class TickAppForgotPassword(models.Model):
    id = models.BigAutoField(primary_key=True)
    userId = models.IntegerField(null=False)
    token = models.CharField(max_length=256, null=True)
    used = models.BooleanField(default=False)
    generated_time = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = 'tick_app_forgotpassword'


class TickAppContactMailInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(null=False)
    name = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    message = models.CharField(max_length=512)
    timestamp = models.DateTimeField()
    responded = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'tick_app_contactmailinfo'


class TickAppQueries(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.CharField(max_length=256, null=False)
    description = models.CharField(max_length=256, null=True)
    userId = models.IntegerField(null=False)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tick_app_queries'

class TickAppQueryComments(models.Model):
    id = models.BigAutoField( primary_key=True)
    queryId = models.BigIntegerField(null=False)
    comment = models.CharField(max_length=512, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tick_app_query_comments'

class TickAppDcf(models.Model):
    id = models.BigAutoField( primary_key=True)
    year = models.CharField(max_length=10,blank=True, null=True)
    symbol = models.CharField(max_length=64,blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    revenuepercentage = models.FloatField(db_column='revenuePercentage',blank=True, null=True)
    ebitda = models.FloatField(blank=True, null=True)
    ebitdapercentage = models.FloatField(db_column='ebitdaPercentage',blank=True, null=True)
    ebit = models.FloatField(blank=True, null=True)
    ebitpercentage = models.FloatField(db_column='ebitPercentage',blank=True, null=True)
    depreciation = models.FloatField(blank=True, null=True)
    depreciationpercentage = models.FloatField(db_column='depreciationPercentage',blank=True, null=True)
    totalcash = models.FloatField(db_column='totalCash',blank=True, null=True)
    totalcashpercentage= models.FloatField(db_column='totalCashPercentage',blank=True, null=True)
    receivables = models.FloatField(blank=True, null=True)
    receivablespercentage = models.FloatField(db_column='receivablesPercentage',blank=True, null=True)
    inventories = models.FloatField(blank=True, null=True)
    inventoriespercentage = models.FloatField(db_column='inventoriesPercentage',blank=True, null=True)
    payable = models.FloatField(blank=True, null=True)
    payablepercentage = models.FloatField(db_column='payablePercentage',blank=True, null=True)
    capitalexpenditure = models.FloatField(db_column='capitalExpenditure',blank=True, null=True)
    capitalexpenditurepercentage = models.FloatField(db_column='capitalExpenditurePercentage',blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    beta = models.FloatField(blank=True, null=True)
    dilutedsharesoutstanding = models.FloatField(db_column='dilutedSharesOutstanding',blank=True, null=True)
    costofdebt = models.FloatField(db_column='costofDebt',blank=True, null=True)
    taxrate = models.FloatField(db_column='taxRate',blank=True, null=True)
    aftertaxcostofdebt = models.FloatField(db_column='afterTaxCostOfDebt',blank=True, null=True)
    riskfreerate = models.FloatField(db_column='riskFreeRate',blank=True, null=True)
    marketriskpremium = models.FloatField(db_column='marketRiskPremium',blank=True, null=True)
    costofequity = models.FloatField(db_column='costOfEquity',blank=True, null=True)
    totaldebt = models.FloatField(db_column='totalDebt',blank=True, null=True)
    totalequity = models.FloatField(db_column='totalEquity',blank=True, null=True)
    totalcapital = models.FloatField(db_column='totalCapital',blank=True, null=True)
    debtweighting = models.FloatField(db_column='debtWeighting',blank=True, null=True)
    equityweighting = models.FloatField(db_column='equityWeighting',blank=True, null=True)
    wacc = models.FloatField(blank=True, null=True)
    taxratecash = models.FloatField(db_column='taxRateCash',blank=True, null=True)
    ebiat = models.FloatField(blank=True, null=True)
    ufcf = models.FloatField(blank=True, null=True)
    sumpvufcf = models.FloatField(db_column='sumPvUfcf',blank=True, null=True)
    longtermgrowthrate = models.FloatField(db_column='longTermGrowthRate',blank=True, null=True)
    terminalvalue = models.FloatField(db_column='terminalValue',blank=True, null=True)
    presentterminalvalue = models.FloatField(db_column='presentTerminalValue',blank=True, null=True)
    enterprisevalue = models.FloatField(db_column='enterpriseValue',blank=True, null=True)
    netdebt = models.FloatField(db_column='netDebt',blank=True, null=True)
    equityvalue = models.FloatField(db_column='equityValue',blank=True, null=True)
    equityvaluepershare = models.FloatField(db_column='equityValuePerShare',blank=True, null=True)
    freecashflowt1 = models.FloatField(db_column='freeCashFlowT1',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tick_app_dcf'

class TickAppLevereddcf(models.Model):
    id = models.BigAutoField( primary_key=True)
    year = models.CharField(max_length=10,blank=True, null=True)
    symbol = models.CharField(max_length=64,blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    revenuepercentage = models.FloatField(db_column='revenuePercentage',blank=True, null=True)
    capitalexpenditure = models.FloatField(db_column='capitalExpenditure',blank=True, null=True)
    capitalexpenditurepercentage = models.FloatField(db_column='capitalExpenditurePercentage',blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    beta = models.FloatField(blank=True, null=True)
    dilutedsharesoutstanding = models.FloatField(db_column='dilutedSharesOutstanding',blank=True, null=True)
    costofdebt = models.FloatField(db_column='costofDebt',blank=True, null=True)
    taxrate = models.FloatField(db_column='taxRate',blank=True, null=True)
    aftertaxcostofdebt = models.FloatField(db_column='afterTaxCostOfDebt',blank=True, null=True)
    riskfreerate = models.FloatField(db_column='riskFreeRate',blank=True, null=True)
    marketriskpremium = models.FloatField(db_column='marketRiskPremium',blank=True, null=True)
    costofequity = models.FloatField(db_column='costOfEquity',blank=True, null=True)
    totaldebt = models.FloatField(db_column='totalDebt',blank=True, null=True)
    totalequity = models.FloatField(db_column='totalEquity',blank=True, null=True)
    totalcapital = models.FloatField(db_column='totalCapital',blank=True, null=True)
    debtweighting = models.FloatField(db_column='debtWeighting',blank=True, null=True)
    equityweighting = models.FloatField(db_column='equityWeighting',blank=True, null=True)
    wacc = models.FloatField(blank=True, null=True)
    operatingcashflow = models.FloatField(db_column='operatingCashFlow',blank=True, null=True)
    pvlfcf = models.FloatField(db_column='pvLfcf',blank=True, null=True)
    sumpvlfcf = models.FloatField(db_column='sumPvLfcf',blank=True, null=True)
    longtermgrowthrate = models.FloatField(db_column='longTermGrowthRate',blank=True, null=True)
    freecashflow = models.FloatField(db_column='freeCashFlow',blank=True, null=True)
    terminalvalue = models.FloatField(db_column='terminalValue',blank=True, null=True)
    presentterminalvalue = models.FloatField(db_column='presentTerminalValue',blank=True, null=True)
    enterprisevalue = models.FloatField(db_column='enterpriseValue',blank=True, null=True)
    netdebt = models.FloatField(db_column='netDebt',blank=True, null=True)
    equityvalue = models.FloatField(db_column='equityValue',blank=True, null=True)
    equityvaluepershare = models.FloatField(db_column='equityValuePerShare',blank=True, null=True)
    freecashflowt1 = models.FloatField(db_column='freeCashFlowT1',blank=True, null=True)
    operatingcashflowpercentage = models.FloatField(db_column='operatingCashFlowPercentage',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tick_app_levereddcf'

class TickAppRiskpremium(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.CharField(max_length=254,blank=True, null=True)
    continent = models.CharField(max_length=254,blank=True, null=True)
    totalequityriskpremium = models.FloatField(db_column='totalEquityRiskPremium',blank=True, null=True)
    countryriskpremium = models.FloatField(db_column='countryRiskPremium',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tick_app_riskpremium'

class TickAppFmpcompanies(models.Model):
    id = models.BigAutoField( primary_key=True)
    symbol = models.CharField(max_length=64,blank=True, null=True)
    name = models.CharField(max_length=512,blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    exchange = models.CharField(max_length=256,blank=True, null=True)
    exchangeshortname = models.CharField(db_column='exchangeShortName',max_length=64,blank=True, null=True)
    type = models.CharField(max_length=64,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tick_app_fmpcompanies'
