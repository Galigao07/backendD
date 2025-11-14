from django.urls import path
from backend.Taskpane.taskpaneviews import *

urlpatterns = [
    # Other URL patterns
   

    path('cashiers-login/', get_cahiers_login, name='get_cahiers_login'),
    path('cash-count-cash-breakdown/', get_cash_count_cash_breakdown, name='get_cash_count_cash_breakdown'),
    path('cashiers-login-isxread/', get_cahiers_login_for_xread, name='get_cahiers_login_for_xread'),
    path('generate-sales-xread/', generate_data_xread, name='generate_data_xread'),
    path('cashiers-login-done-all-xread/', get_cahiers_login_done_xread, name='get_cahiers_login_done_xread'),

    path('approves-cash-breakdown/', approved_cash_breakdown, name='approved_cash_breakdown'),
    path('download-pdf-cash-breakdown-approved/',download_pdf_cash_breakdown_approved,name='download_pdf_cash_breakdown_approved'),
    path('z-read-summary/', PrintZread, name='PrintZread'),
    path('xread-pdf/', download_xread_pdf, name='download_xread_pdf'),
    path('zread-pdf/', download_zread_pdf, name='download_zread_pdf'),
    path('latest-z-read/',latest_zread,name='latest_zread'),
    path('get-zread-no/',get_zread_no,name='get_zread_no'),
    path('get-cashier-per-zread-no/',get_cashier_zread_no,name='get_cashier_zread_no'),

    path('reprint-xread-pdf/', RePrint_Xread, name='RePrint_Xread'),
    path('reprint-zread-pdf/', Reprint_Zread, name='Reprint_Zread'),

    


]