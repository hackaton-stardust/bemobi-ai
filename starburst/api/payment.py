from django.contrib.auth.models import User
from django.http import JsonResponse

from chatbot.views import payment_analysis_response
from starburst.api.base import BaseApiIntegration
from starburst.error import RequestError, RequestErrorCode
from starburst.models.models import get_user


class PaymentIntegration(BaseApiIntegration):

    def payment_analysis(self):
        data = self.request_data
        client = self.client
        user_id = data.get('user_id')

        if not user_id:
            raise RequestError(RequestErrorCode.MISSING_PARAMETER)

        user = get_user(user_id)
        if not user:
            raise RequestError(RequestErrorCode.USER_NOT_FOUND)

        txn_sequence = []
        txn_set = user['transactions']
        txn_delayed = [txn for txn in txn_set if txn['delayed']]

        for txn in txn_set:
            if not txn['delayed']:
                txn_sequence.append(txn)
            else:
                break

        total_invoices = len(txn_set)
        total_delays = len(txn_delayed)
        percentage_of_delays = (total_delays / total_invoices) * 100 if total_invoices > 0 else 0
        is_debtor = total_delays > 0
        eligible_for_bonuses = client['max_delays'] < total_delays and len(txn_sequence) > client['min_sequence']

        bot_data = {
            'user': user['name'],
            'client': client['name'],
            'payment_sequence': len(txn_sequence),
            'total_delays': total_delays,
            'total_invoices': total_invoices,
            'percentage_of_delays': percentage_of_delays,
            'is_debtor': is_debtor,
            'eligible_for_bonuses': eligible_for_bonuses
        }

        return payment_analysis_response(bot_data)
