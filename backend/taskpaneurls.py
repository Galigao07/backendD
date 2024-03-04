from django.urls import path
from backend.Taskpane.taskpaneviews import (add_user,view_user,update_user,get_employee_list,delete_user,view_waiter,add_waiter,update_waiter,delete_waiter)


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
]