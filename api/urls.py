from django.urls import path
from api.views import *

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('commit/', OrderCommitView.as_view(), name='commit'),
    path('delete/', OrderDeleteView.as_view(), name='delete'),
    path('check/', OrderCheckView.as_view(), name='check'),
]