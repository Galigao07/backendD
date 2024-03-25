from django.urls import path
from backend.Reference.setupviews import Setup,get_account_title

urlpatterns = [
    path('setup/',Setup,name='Setup'),
    path('account-title/',get_account_title,name='get_account_title')

]