import datetime
import logging
import time

import stripe
from dateutil.relativedelta import relativedelta
from pinax.stripe import hooks
from pinax.stripe.actions.subscriptions import sync_subscription_from_stripe_data
from stripe.error import InvalidRequestError, StripeError

logger = logging.getLogger(__name__)


def verify_coupon(code):
    coupon = stripe.Coupon.retrieve(code)
    if not coupon['valid']:
        raise StripeError(f'{code} is not a valid discount code.')
    return coupon


def create_stripe_subscription(customer, plan, quantity=None, trial_days=None, token=None, coupon=None,
                               tax_percent=None):
    # init from pinax.stripe.actions.subscriptions.create
    quantity = hooks.hookset.adjust_subscription_quantity(customer=customer, plan=plan, quantity=quantity)

    # relocate subscription date to 1st and 15th
    # now = datetime.datetime.now()
    # day = now.day
    # period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) if day < 15 else now.replace(
    #     day=15, hour=0, minute=0, second=0, microsecond=0)
    # current_period_end = period_start + relativedelta(months=1)

    subscription_params = {}
    if trial_days == 'now':
        subscription_params["trial_end"] = 'now'
    elif trial_days:
        subscription_params["trial_end"] = datetime.datetime.now() + datetime.timedelta(days=trial_days)
    if token:
        subscription_params["source"] = token

    subscription_params["stripe_account"] = customer.stripe_account_stripe_id
    subscription_params["customer"] = customer.stripe_id
    subscription_params["plan"] = plan
    subscription_params["quantity"] = quantity
    subscription_params["coupon"] = coupon
    subscription_params["tax_percent"] = tax_percent
    # subscription_params["payment_behavior"] = 'allow_incomplete'

    # relocate subscription date to 1st and 15th
    # subscription_params["backdate_start_date"] = int(time.mktime(period_start.timetuple()))
    # subscription_params["billing_cycle_anchor"] = int(time.mktime(current_period_end.timetuple()))
    resp = stripe.Subscription.create(**subscription_params)

    return sync_subscription_from_stripe_data(customer, resp)


def cancel_subscription(customer, subscription_stripe_id, at_period_end=True):
    sub = stripe.Subscription(
        subscription_stripe_id,
        stripe_account=customer.stripe_account_stripe_id,
    ).delete(
        at_period_end=at_period_end,
    )
    return sync_subscription_from_stripe_data(customer, sub)
