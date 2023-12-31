
from django.urls import path
from .views import user_login_api,get_csrf_token
from .Restaurant.restaurantviews import (get_product_data, get_productCategory_data,product_list_by_category,table_list_view,save_sales_order,
                                         get_sales_order_list,get_sales_order_listing,get_add_order_view,save_cash_payment,get_customer_list,
                                         get_waiter_list,cancel_sales_order,save_sales_order_takeout,get_reprint_transaction,get_reprint_transaction_for_receipt)

urlpatterns = [
    # Other URL patterns
    path('login/', user_login_api, name='user_login_api'),
    path('product/', get_product_data, name='get_product_data'),
    path('product/category/', get_productCategory_data, name='get_productCategory_data'),
    path('product/<str:category>/', product_list_by_category, name='product_list_by_category'),
    path('table/count/', table_list_view, name='table_list_view'),
    path('csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('add-sales-order/',save_sales_order,name='save_sales_order'),
    path('sales-order-list/',get_sales_order_list,name = 'get_sales_order_list'),
    path('sales-order-listing/', get_sales_order_listing, name='get_sales_order_listing'),
    path('order/view/', get_add_order_view, name='get_add_order_view'),
    path('save-cash-payment/', save_cash_payment, name='save_cash_payment'),
    path('customer-list/', get_customer_list, name='get_customer_list'),
    path('waiter-list/', get_waiter_list, name='get_waiter_list'),
    path('cancel-sales-order/', cancel_sales_order, name='cancel_sales_order'),
    path('save-sales-order-take-out/', save_sales_order_takeout, name='save_sales_order_takeout'),
    path('reprint-transaction/', get_reprint_transaction, name='get_reprint_transaction'),
    path('reprint-transacion-receipt/', get_reprint_transaction_for_receipt, name='get_reprint_transaction_for_receipt'),
    
    
]