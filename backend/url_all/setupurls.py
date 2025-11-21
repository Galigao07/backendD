from django.urls import path
from backend.Reference.setupviews import *
urlpatterns = [
    path('setup/',Setup,name='Setup'),
    path('product-price-type-list/',price_type_list,name='price_type_list'),
    path('account-title/',get_account_title,name='get_account_title'),
    path('sl-account/',get_SL_account,name='get_SL_account'),
    path('setup-configure/',setup_configure,name='setup_configure'),
    path('cost-of-sales/',get_cost_of_sales,name='get_cost_of_sales'), 
    path('allowed-price-type/',get_allowed_price_type,name='get_allowed_price_type') ,
    path('tagging-sales-category/',get_tagging_category_list,name='get_tagging_category_list'),
    path('tagging-per-terminal/',get_tagging_per_terminal,name='get_tagging_per_terminal'),


]