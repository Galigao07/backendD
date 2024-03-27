from django.urls import path
from backend.Reference.setupviews import( Setup,get_account_title,get_SL_account,setup_configure,get_cost_of_sales)

urlpatterns = [
    path('setup/',Setup,name='Setup'),
    path('account-title/',get_account_title,name='get_account_title'),
    path('sl-account/',get_SL_account,name='get_SL_account'),
    path('setup-configure/',setup_configure,name='setup_configure'),
    path('cost-of-sales/',get_cost_of_sales,name='get_cost_of_sales') 
]