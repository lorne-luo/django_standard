from importlib import import_module

from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = "apps.payment"

    def ready(self):
        import_module("apps.payment.receivers")
