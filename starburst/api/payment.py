from django.contrib.auth.models import User
from django.http import JsonResponse

from starburst.api.base import BaseApiIntegration
from starburst.error import RequestError, RequestErrorCode


class PaymentIntegration(BaseApiIntegration):

    def payment_analysis(self):
        data = self.request_data
        client = self.client
        user_id = data.get('user_id')

        if not user_id:
            raise RequestError(RequestErrorCode.MISSING_PARAMETER)

        try:
            user = User.objects.get(pk=user_id) #FIXME
        except User.DoesNotExist:
            raise RequestError(RequestErrorCode.USER_NOT_FOUND)

        txn_sequence = []
        txn_set = user.transactions_set.all().order_by('expiration_date')
        txn_delayed = txn_set.filter(delayed=True)

        for txn in txn_set:
            if not txn.delayed:
                txn_sequence.append(txn)
            else:
                break

        return JsonResponse({
            'user': user.name,
            'client': client.name,
            'payment_sequence': len(txn_sequence),
            'total_delays': txn_delayed.count(),
            'total_invoices': txn_set.count(),
            'percentage_of_delays': txn_delayed.count() / txn_set.count() * 100,
            'is_debtor': txn_delayed.count() > 0,
            'eligible_for_bonuses': client.max_delays < txn_delayed.count() and txn_sequence > client.min_sequence
        })
