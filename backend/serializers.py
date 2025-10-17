from rest_framework import serializers
from .models import *


class POSSalesTransGiftCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model =  POSSalesTransGiftCheck
        fields = '__all__'

class POSGiftCheckSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model =  POSGiftCheckSeries
        fields = '__all__'

class POSGiftCheckDenominationSerializer(serializers.ModelSerializer):
    class Meta:
        model =  POSGiftCheckDenomination
        fields = '__all__'




class PosCashPulloutDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosCashPulloutDetails
        fields = '__all__'

class POSProductPrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model =  POSProductPrinter
        fields = '__all__'

class PosVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosVideo
        fields = '__all__'


class PosCashPulloutSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosCashPullout
        fields = '__all__'

class PosCashBreakdownSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosCashBreakdown
        fields = '__all__'

class PosSuspendListSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosSuspendList
        fields = '__all__'


class PosSuspendListingSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosSuspendListing
        fields = '__all__'

class PosSalesTransCreditSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosSalesTransCreditSale
        fields = '__all__'

class SLCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  SLCategory
        fields = '__all__'

class POSSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model =  POSSettings
        fields = '__all__'


class AcctListSerializer(serializers.ModelSerializer):
    class Meta:
        model =  AcctList
        fields = '__all__'

class AcctSubsidiaryTitleSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    acct_title = serializers.SerializerMethodField()

    class Meta:
        model = AcctSubsidiary
        fields = ['code', 'acct_title', 'sl_type']  # only include these 3

    def _get_acctlist(self, obj):
        """Helper to fetch matching AcctList record."""
        return AcctList.objects.filter(
            primary_code=obj.primary_code,
            secondary_code=obj.secondary_code,
            acct_code=obj.acct_code,
            subsidiary_code=obj.subsidiary_code
        ).first()

    def get_code(self, obj):
        acct = self._get_acctlist(obj)
        return acct.code if acct else None

    def get_acct_title(self, obj):
        acct = self._get_acctlist(obj)
        return acct.acct_title if acct else None

class AcctSubsidiarySerializer(serializers.ModelSerializer):

    class Meta:
        model = AcctSubsidiary
        fields = '__all__'  # includes model fields
        # You can also explicitly list them:
        # fields = ['autonum', 'primary_code', 'secondary_code', 'acct_code', 'subsidiary_code', 'acct_title', 'under', 'acct_code_from_list']

class PosSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosSetup
        fields = '__all__'

class ProductCategorySalesSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProductCategorySales
        fields = '__all__'

class PosMultiplePriceTypeSiteSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosMultiplePriceTypeSiteSetup
        fields = '__all__'


class ProductSiteSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProductSiteSetup
        fields = '__all__'

class PosPriceTypeSiteSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosPriceTypeSiteSetup
        fields = '__all__'

class RCCDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =  RCCDetails
        fields = '__all__'

class CCCDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =  CCCDetails
        fields = '__all__'




class PosSalesTransSeniorCitizenDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosSalesTransSeniorCitizenDiscount
        fields = '__all__'

class SalesTransEPSSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SalesTransEPS
        fields = '__all__'


class SalesTransCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SalesTransCreditCard
        fields = '__all__'

class ProductCategorySetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProductCategorySetup
        fields = '__all__'

class OtherAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model =  OtherAccount
        fields = '__all__'

class TSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  TSetup
        fields = '__all__'

class CompanySetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  CompanySetup
        fields = '__all__'

class BankCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model =  BankCompany
        fields = '__all__'
     
class BankCardSerializer(serializers.ModelSerializer):
    class Meta:
        model =  BankCard
        fields = '__all__'


class PosCashiersLoginpSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosCashiersLogin
        fields = '__all__'

class PosClientSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosClientSetup
        fields = '__all__'


class LeadSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  LeadSetup
        fields = '__all__'
        
class PosExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosExtended
        fields = '__all__'

class SeniorCitizenDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SeniorCitizenDiscount
        fields = '__all__'

class EmployeeSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Employee
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PosPayorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosPayor
        fields = '__all__'

class PosWaiterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosWaiterList
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['bar_code', 'long_desc', 'reg_price','category','prod_img']

class Product2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['autonum','category']
        
class PosRestTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosRestTable
        fields = ['details_id','table_no','site_code','table_start']
        
class PosSalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosSalesOrder
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class POS_TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS_Terminal
        fields = '__all__'

class PosSalesTransDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosSalesTransDetails
        fields = '__all__'
        
class PosSalesTransSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosSalesTrans
        fields = '__all__'

class PosSalesInvoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosSalesInvoiceList
        fields = '__all__'
class PosSalesInvoiceListingSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosSalesInvoiceListing
        fields = '__all__'


class PosOtherPmtSetupSerialize(serializers.ModelSerializer):
    class Meta:
        model = PosOtherPmtSetup
        fields = '__all__'

class PosOtherPmtSetupPaymentSerializer(serializers.ModelSerializer):
    sl_type = serializers.SerializerMethodField()

    class Meta:
        model = PosOtherPmtSetup
        fields = ['pmt_desc','acct_code', 'acct_title', 'sl_type','remarks']

    def get_sl_type(self, obj):
        """
        Step 1: Get matching AcctList to retrieve codes
        Step 2: Use those codes to find matching AcctSubsidiary
        """
        acct_list = AcctList.objects.filter(code=int(float(obj.acct_code))).first()
        if not acct_list:
            return None

        acct_sub = AcctSubsidiary.objects.filter(
            primary_code=acct_list.primary_code,
            secondary_code=acct_list.secondary_code,
            acct_code=acct_list.acct_code,
            subsidiary_code=acct_list.subsidiary_code
        ).first()

        return acct_sub.sl_type if acct_sub else None







