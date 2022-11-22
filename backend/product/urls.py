from django.contrib import admin
from django.urls import path


from . import views
import uuid

# api path for handling products and bidding
# check views.py for more info
urlpatterns=[
    path('<str:id>',views.product),
    path('',views.product),
    path('<str:id>/bid/place/<int:amount>',views.placeBid),
    path('<str:id>/sell/',views.sell)
]