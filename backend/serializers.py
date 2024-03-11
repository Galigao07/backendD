from rest_framework import serializers
from .models import (Product, PosRestTable,PosSalesOrder,User,POS_Terminal,PosSalesTransDetails,PosSalesTrans,PosSalesInvoiceList,PosSalesInvoiceListing,
                     CompanySetup,Customer,PosWaiterList,PosPayor,Employee,SeniorCitizenDiscount,PosExtended,LeadSetup,PosClientSetup,
                     PosCashiersLogin,PosCashBreakdown,BankCompany,TSetup,OtherAccount,ProductCategorySetup,BankCard,SalesTransCreditCard,
                     SalesTransEPS)



class PosCashBreakdownSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PosCashBreakdown
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
        fields = ['bar_code', 'long_desc', 'reg_price','category']
        
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








