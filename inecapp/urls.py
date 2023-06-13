from django.urls import path, include
from .views import *

urlpatterns = [  
    path('', index, name='index'),
    path('results/<uniqueid>', view_result, name='view_result'),
    path('lga-results/', sum_total_result, name='sum_total_result'),
    path('add-results/', PollResultCreate.as_view(), name='add_result'),
]
