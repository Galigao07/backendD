from rest_framework import serializers
from .models import (Product, PosRestTable,PosSalesOrder,User,POS_Terminal,PosSalesTransDetails,PosSalesTrans,PosSalesInvoiceList,PosSalesInvoiceListing,
                     CompanySetup,Customer,PosWaiterList,PosPayor)



class CompanySetupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  CompanySetup
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
        fields = ['details_id','table_no','site_code']
        
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








