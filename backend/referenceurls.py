from django.urls import path
from backend.Reference.referenceviews import (add_user,view_user,update_user,get_employee_list,delete_user,view_waiter,add_waiter,update_waiter,delete_waiter,
                                              view_table,add_table,delete_table,update_table,UploadVideo,terminal_setup,lead_setup,Client_setup,
                                              CustomerDetails,CustomerSearchResults,SupplierDetails,get_cahiers_login,get_cash_count_cash_breakdown,
                                              get_cahiers_login_for_xread,generate_data_xread,get_product_profile,product_printer_category,printer_list,
                                              get_product_Category_setup,Gift_Check_Denomination,Gift_Check_series)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Other URL patterns
    path('add-users/', add_user, name='add_user'),
    path('view-users/', view_user, name='view_user'),
    path('employee-list/', get_employee_list, name='get_employee_list'),
    path('update-users/', update_user, name='update_user'),
    path('delete-users/', delete_user, name='delete_user'),
    path('view-waiter/', view_waiter, name='view_waiter'),
    path('add-waiter/', add_waiter, name='add_waiter'),
    path('update-waiter/', update_waiter, name='update_waiter'),
    path('delete-waiter/', delete_waiter, name='delete_waiter'),
    path('view-table/', view_table, name='view_table'),
    path('add-table/', add_table, name='add_table'),
    path('update-table/', update_table, name='update_table'),
    path('delete-table/', delete_table, name='delete_table'),
    path('video-upload/', UploadVideo, name='UploadVideo'),
    path('terminal-setup/', terminal_setup, name='terminal_setup'),
    path('lead-setup/', lead_setup, name='lead_setup'),
    path('client-setup/', Client_setup, name='Client_setup'),
    path('customer-details/', CustomerDetails, name='CustomerDetails'),
    path('customer-search/', CustomerSearchResults, name='CustomerSearchResults'),
    path('supplier-details/', SupplierDetails.as_view(), name='SupplierDetails'),
    path('cashiers-login/', get_cahiers_login, name='get_cahiers_login'),
    path('cash-count-cash-breakdown/', get_cash_count_cash_breakdown, name='get_cash_count_cash_breakdown'),
    path('cashiers-login-xread/', get_cahiers_login_for_xread, name='get_cahiers_login_for_xread'),
    path('generate-sales-xread/', generate_data_xread, name='generate_data_xread'),
    path('product-profile/', get_product_profile, name='get_product_profile'),
    path('printer-categories/', product_printer_category, name='product_printer_category'),
    path('printer-list/', printer_list, name='printer_list'),
    path('product-category-setup/', get_product_Category_setup, name='get_product_Category_setup'),
    path('gift-check-series/', Gift_Check_series, name='Gift_Check_series'),
    path('gift-check-denomination/', Gift_Check_Denomination, name='Gift_Check_Denomination'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)