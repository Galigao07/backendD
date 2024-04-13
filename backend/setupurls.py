from django.urls import path
from backend.Reference.systemsettingsviews import systemSettings
from backend.Reference.setupviews import( Setup,get_account_title,get_SL_account,setup_configure,get_cost_of_sales,
                                         get_allowed_price_type,get_tagging_category_list,get_tagging_per_terminal)

urlpatterns = [
    path('setup/',Setup,name='Setup'),
    path('account-title/',get_account_title,name='get_account_title'),
    path('sl-account/',get_SL_account,name='get_SL_account'),
    path('setup-configure/',setup_configure,name='setup_configure'),
    path('cost-of-sales/',get_cost_of_sales,name='get_cost_of_sales'), 
    path('allowed-price-type/',get_allowed_price_type,name='get_allowed_price_type') ,
    path('tagging-sales-category/',get_tagging_category_list,name='get_tagging_category_list'),
    path('tagging-per-terminal/',get_tagging_per_terminal,name='get_tagging_per_terminal'),
    path('system-settings/',systemSettings,name='systemSettings'), 

]