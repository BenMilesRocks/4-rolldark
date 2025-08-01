'''Checkout apps.py'''
from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    '''Config for checkout app'''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        import checkout.signals #pylint: disable= W0611, C0415
