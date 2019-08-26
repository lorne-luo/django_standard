import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.encoding import smart_str
from django.views.generic import DetailView
from pinax.stripe.actions.customers import set_default_source
from pinax.stripe.actions.sources import create_card, delete_card
from pinax.stripe.mixins import LoginRequiredMixin, CustomerMixin
from pinax.stripe.models import Card
from pinax.stripe.views import PaymentMethodCreateView
from rest_framework.response import Response
from rest_framework.views import APIView
from stripe.error import StripeError

from apps.payment.stripe import verify_coupon

logger = logging.getLogger(__name__)


class PaymentMethodDetailView(LoginRequiredMixin, CustomerMixin, DetailView):
    model = Card
    context_object_name = "object"
    template_name = "pinax/stripe/paymentmethod_detail.html"

    def get_object(self, queryset=None):
        return Card.objects.filter(customer=self.customer).first()


class CreditCardUpdateView(PaymentMethodCreateView):
    template_name = "pinax/stripe/paymentmethod_update.html"

    def get_success_url(self):
        return reverse_lazy('payment_detail')

    def replace_card(self, stripe_token):
        exist_card_ids = [c.stripe_id for c in self.customer.card_set.all()]
        card = create_card(self.customer, token=stripe_token)
        set_default_source(self.customer, card.stripe_id)

        # clean other card
        for stripe_id in exist_card_ids:
            delete_card(self.customer, stripe_id)
        return card

    def post(self, request, *args, **kwargs):
        cardToken = request.POST.get("cardToken")
        if not cardToken:
            msg = 'Can\'t get card token, please try again'
            messages.error(request, msg)
            return self.render_to_response(self.get_context_data(errors=msg))

        try:
            card = self.replace_card(cardToken)
            return HttpResponseRedirect(self.get_success_url())
        except StripeError as e:
            logger.error("Card binding error: %s" % e)
            messages.error(request, e.user_message)
            return self.render_to_response(self.get_context_data(errors=e.user_message))
        except Exception as e:
            logger.error("Card binding error: %s" % e)
            messages.error(request, smart_str(e))
            return self.render_to_response(self.get_context_data(errors=smart_str(e)))


class VerifyCouponAPIView(APIView):

    def post(self, request):
        code = request.POST.get('code')
        if not code:
            return Response({'success': False, 'detail': 'Please provide code parameter.'}, status=400)

        try:
            coupon = verify_coupon(code)
        except StripeError as ex:
            return Response({'success': False, 'detail': ex.user_message}, status=404)
        except Exception as ex:
            return Response({'success': False, 'detail': str(ex)}, status=500)

        if coupon:
            coupon['success'] = True
            return Response(coupon)
        else:
            return Response({'success': False, 'detail': f'{code} is not a valid discount code.'})
