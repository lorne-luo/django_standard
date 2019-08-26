from django.urls import path, include
from django.conf.urls import include, url
from pinax.stripe.views import (InvoiceListView,
    PaymentMethodDeleteView,
    PaymentMethodListView,
    PaymentMethodUpdateView,
    Webhook)

from apps.payment.views import CreditCardUpdateView, PaymentMethodDetailView, VerifyCouponAPIView
from . import views

urlpatterns = [
    url(r"^dashboard/payment/$", PaymentMethodDetailView.as_view(), name="payment_detail"),
    # url(r"^payments/payment-methods/(?P<pk>\d+)/delete/$", PaymentMethodDeleteView.as_view(), name="pinax_stripe_payment_method_delete"),
    url(r"^dashboard/payment/update/$", CreditCardUpdateView.as_view(), name="payment_update"),
    url(r"^payments/invoices/$", InvoiceListView.as_view(), name="pinax_stripe_invoice_list"),

    url(r"^payments/webhook/$", Webhook.as_view(), name="pinax_stripe_webhook"),
    url(r"^payments/verify_coupon/$", VerifyCouponAPIView.as_view(), name="payment_verify_coupon"),
]
