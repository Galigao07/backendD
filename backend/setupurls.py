from django.urls import path
from backend.Reference.setupviews import Setup

urlpatterns = [
    path('setup/',Setup,name='Setup')
]