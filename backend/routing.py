from django.urls import re_path
from backend.consumer import *

websocket_urlpatterns = [
    re_path(r'ws/select-table-que/(?P<SERIALNO>[\w-]+)/$', CountConsumer.as_asgi()),
    re_path(r'ws/group_name/$', POSextended.as_asgi()),
    re_path(r'ws/change/$', POSextendedChange.as_asgi()),
    re_path(r'ws/extended-monitor/(?P<SERIALNO>[\w-]+)/$', PosExtendedMonitor.as_asgi()),

    re_path(r'ws/login/(?P<SERIALNO>[\w-]+)/$', LoginSocket.as_asgi()),
    re_path(r'ws/logout/(?P<SERIALNO>[\w-]+)/$', LogoutSocket.as_asgi()),
    #  re_path(r'ws/group_name/(?P<extended_group>[^/]+)/$', POSextended.as_asgi()),
]

