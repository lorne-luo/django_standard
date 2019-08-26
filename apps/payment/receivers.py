import logging

from django.dispatch import receiver
from pinax.stripe.actions.subscriptions import sync_subscription_from_stripe_data
from pinax.stripe.models import Customer as StripeCustomer
from pinax.stripe.signals import WEBHOOK_SIGNALS

from apps.customer.models import Customer
from apps.subscription.models import ParcelSubscription

logger = logging.getLogger(__name__)


def subscription_webhook_callback(event):
    customer = StripeCustomer.objects.filter(stripe_id=event.message['data']['object']['customer']).first()
    if not customer:
        logger.warning(
            'Event#customer.subscription.updated, customer %s not found.' % event.message['data']['object']['customer'])
        return

    # sync with stripe subscription
    sub = sync_subscription_from_stripe_data(customer, event.message['data']['object'])

    # sync parcel subscription
    parcel_subscription = ParcelSubscription.objects.filter(stripe_id=sub.stripe_id).first()
    if parcel_subscription:
        parcel_subscription.unsubscribe_callback(sub)


@receiver(WEBHOOK_SIGNALS["customer.subscription.updated"])
def handle_subscription_updated(sender, event, **kwargs):
    subscription_webhook_callback(event)


@receiver(WEBHOOK_SIGNALS["customer.subscription.deleted"])
def handle_subscription_deleted(sender, event, **kwargs):
    subscription_webhook_callback(event)


@receiver(WEBHOOK_SIGNALS["customer.updated"])
def handle_customer_updated(sender, event, **kwargs):
    customer_data = event.message['data']['object']

    customer = Customer.objects.filter(stripe_customer__stripe_id=customer_data['id']).first()
    if not customer:
        return

    customer.phone_number = customer_data.get('phone', '')
    names = customer_data.get('name', '').split(' ', 1)
    customer.first_name = names[0]
    if len(names) > 1:
        customer.last_name = names[1]
    customer.save()

    if customer_data['address']:
        address_data = customer_data['address']

        billing_address = customer.billing_address
        billing_address.street_number_name = '%s %s' % (address_data['line1'], address_data['line2'])
        billing_address.street_number_name = billing_address.street_number_name.strip()
        billing_address.suburb = address_data['city']
        billing_address.postcode = address_data['postal_code']
        billing_address.state = address_data['state']
        billing_address.country = address_data['country']
        billing_address.save()

    if customer_data['shipping'] and customer_data['shipping']['address']:
        address_data = customer_data['shipping']['address']

        shipping_address = customer.shipping_address
        shipping_address.street_number_name = '%s %s' % (
            address_data['line1'], address_data['line2'])
        shipping_address.street_number_name = shipping_address.street_number_name.strip()
        shipping_address.suburb = address_data['city']
        shipping_address.postcode = address_data['postal_code']
        shipping_address.state = address_data['state']
        shipping_address.country = address_data['country']
        shipping_address.save()
