from django.urls import path

from backend.Administration.adminviews import *

urlpatterns = [
    path('other-payment-setup-entry/',other_payment_setup,name='other_payment_setup'),

]