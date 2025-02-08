from django.urls import path
from .views import NewPay, GetPayments, GetOnePayment

urlpatterns = [
    path('paid/', NewPay.as_view(), name='create-payment'),
    path('paid-all/<str:uid>/',GetPayments.as_view(), name='get-all-payments'),
    path('paid/<str:uid>/<str:id>/',GetOnePayment.as_view(), name='get-one-payment'),
]