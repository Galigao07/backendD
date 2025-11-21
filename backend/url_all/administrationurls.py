from django.urls import path

from backend.Administration.adminviews import *

urlpatterns = [
    path('add-users/', add_user, name='add_user'),
    path('view-users/', view_user, name='view_user'),
    path('employee-list/', get_employee_list, name='get_employee_list'),
    path('update-users/', update_user, name='update_user'),
    path('delete-users/', delete_user, name='delete_user'),
    path('other-payment-setup-entry/',other_payment_setup,name='other_payment_setup'),
    path('system-settings/',systemSettings,name='systemSettings'), 
    path('lead-setup/', lead_setup, name='lead_setup'),
    path('client-setup/', Client_setup, name='Client_setup'),
    path('terminal-setup/', terminal_setup, name='terminal_setup'),
]