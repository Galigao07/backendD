
from django.urls import path
# from .views import (download_charge_receipt_pdf, user_login_api,get_csrf_token,verification_account,user_logout_api,user_endshift_api,call_onscreen_keyboard_windows,unlock_terminal,CheckTerminalLogIn,
#                     download_pdf,download_sales_order_pdf)
# from .Restaurant.restaurantviews import (get_product_data, get_productCategory_data,product_list_by_category,table_list_view,save_sales_order,
#                                          get_sales_order_list,get_sales_order_listing,get_add_order_view,save_cash_payment,get_customer_list,
#                                          get_waiter_list,cancel_sales_order,save_sales_order_payment,get_reprint_transaction,get_reprint_transaction_for_receipt
#                                          ,get_company_details,queing_list_view,pos_extended,pos_extended_delete_all,print_electron,
#                                          cash_breakdown,get_bank_card,get_bank_list,save_credit_card_payment,save_debit_card_payment,
#                                          save_multiple_payment,get_waiter_name,get_sales_order_list_cancelled,get_sales_order_listing_cancelled,
#                                          uncancelled_sales_order,transfer_table,get_customer_category,get_customer_with_category,save_charge_payment,
#                                          suspend_save_sales_order,get_sales_list_of_transaction,cleared_table_dinein_order_and_pay,Check_Que_No)


from ..views import *
from ..Restaurant.restaurantviews import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



    

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('check_access_token/', check_access_token, name='check_access_token'),
    
    path('onscreen-keyboard/',call_onscreen_keyboard_windows, name='call_onscreen_keyboard_windows'),
    # Other URL patterns
    path('login/', user_login_api, name='user_login_api'),
    path('check-login/',CheckTerminalLogIn,name='CheckTerminalLogIn'),
    path('logout/', user_logout_api, name='user_logout_api'),
    path('end-shift/', user_endshift_api, name='user_endshift_api'),
    path('verification/', verification_account, name='verification_account'),
    path('unlock-terminal/', unlock_terminal, name='unlock_terminal'),

    
    path('product/', get_product_data, name='get_product_data'),
    path('product-per-price-type/', get_product_per_price_name, name='get_product_per_price_name'),
    path('price-type-list/', get_price_type_list, name='get_price_type_list'),
    path('product/category/', get_productCategory_data, name='get_productCategory_data'),
    path('product-category/', product_list_by_category, name='product_list_by_category'),
    path('table/count/', table_list_view, name='table_list_view'),
    path('csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('add-sales-order/',save_sales_order,name='save_sales_order'),
    path('sales-order-list/',get_sales_order_list,name = 'get_sales_order_list'),
    path('print-bill/',PrintBill,name = 'PrintBill'),
    path('sales-order-listing/', get_sales_order_listing, name='get_sales_order_listing'),
    path('sales-order-list-cancelled/',get_sales_order_list_cancelled,name = 'get_sales_order_list_cancelled'),
    path('sales-order-listing-cancelled/', get_sales_order_listing_cancelled, name='get_sales_order_listing_cancelled'),
    path('update-item-discount/', update_item_discount, name='update_item_discount'),
    path('tmp-sc-discount/', tmp_sc_discount, name='tmp_sc_discount'),
    path('remove-discount/', remove_discount, name='remove_discount'),

    

    path('order/view/', get_add_order_view, name='get_add_order_view'),
    path('save-cash-payment/', save_cash_payment, name='save_cash_payment'),
    path('customer-list/', get_customer_list, name='get_customer_list'),
    path('waiter-list/', get_waiter_list, name='get_waiter_list'),
    path('cancel-sales-order/', cancel_sales_order, name='cancel_sales_order'),
    path('uncancel-sales-order/', uncancelled_sales_order, name='uncancelled_sales_order'),
    path('void-so-listing/', void_so_listing, name='void_so_listing'),
    path('void-so/',    void_so, name='void_so'),



    path('save-sales-order-payment/', save_sales_order_payment, name='save_sales_order_payment'),
    path('reprint-transaction/', get_reprint_transaction, name='get_reprint_transaction'),

    path('company-details/', get_company_details, name='get_company_details'),
    path('que-list/', queing_list_view, name='queing_list_view'),
    path('extended-data/', pos_extended, name='pos_extended'),
    path('extended-data-terminal/', pos_extended_delete_all, name='pos_extended_delete_all'),
    path('print/', print_electron, name='print_electron'),
    path('cash-breakdown/', cash_breakdown, name='cash_breakdown'),
    path('bank-company/', get_bank_list, name='get_bank_list'),
    path('bank-card/', get_bank_card, name='get_bank_card'),
    path('save-credit-card-payment/', save_credit_card_payment, name='save_credit_card_payment'),
    path('save-debit-card-payment/', save_debit_card_payment, name='save_debit_card_payment'),
    path('save-multiple-payment/', save_multiple_payment, name='save_multiple_payment'),
    path('save-charge-payment/', save_charge_payment, name='save_charge_payment'),
    path('save-gift-check-payment/', save_gift_check_payment, name='save_gift_check_payment'),
    path('save-online-payment/', save_online_payment, name='save_online_payment'),
    path('save-other-payment/', save_other_payment, name='save_other_payment'),

    path('waiter_name/', get_waiter_name, name='get_waiter_name'),
    path('transfer-table/', transfer_table, name='transfer_table'),
    path('customer-category/', get_customer_category, name='get_customer_category'), 
    path('customer-with-category/', get_customer_with_category, name='get_customer_with_category'), 
    path('susppend-sales-order/', suspend_save_sales_order, name='suspend_save_sales_order'), 
    path('sales-list-of-transaction/', get_sales_list_of_transaction, name='get_sales_list_of_transaction'), 
    path('cleared-table/', cleared_table_dinein_order_and_pay, name='cleared_table_dinein_order_and_pay'), 
    path('receipt-pdf/', download_pdf, name='download_pdf'),
    path('cash-count-pdf/', download_pdf_cash_count, name='download_pdf'),
    path('sales-order-pdf/', download_sales_order_pdf, name='download_sales_order_pdf'),
    path('charge-receipt-pdf/', download_charge_receipt_pdf, name='download_charge_receipt_pdf'),
    path('reprint-transacion-receipt/', get_reprint_transaction_for_receipt, name='get_reprint_transaction_for_receipt'),
    path('reprint-receipt-pdf/', download_Reprint_pdf, name='download_Reprint_pdf'),
   
    # path('xread-pdf/', download_xread_pdf, name='download_xread_pdf'),

    path('check-que-no/', Check_Que_No, name='Check_Que_No'),
    path('validate-gift-check/', validate_gift_check, name='validate_gift_check'),
    path('dinomination/', get_denomination, name='get_denomination'),
    path('acct-title/', get_acct_title, name='set_acct_title'),
    path('subsidiary-account/', getSLname, name='getSLname'),
    path('other-payment-setup/', get_other_payment_setup, name='get_other_payment_setup'),
  

    
    

    
]