import calendar

from django.http import JsonResponse
from django.utils import timezone

from starburst.api.base import BaseApiIntegration
from starburst.error import RequestError, RequestErrorCode
from starburst.models.models import get_user


class Subscription(BaseApiIntegration):

    def mobile_data_analysis(self):
        data = self.request_data
        user_id = data.get('user_id')
        date = data.get('date')
        contrato_id = data.get('contract_id')

        if not user_id:
            raise RequestError(RequestErrorCode.MISSING_PARAMETER)

        if not date:
            date = timezone.now()
        else:
            try:
                date = timezone.datetime.fromisoformat(date)
            except ValueError:
                raise RequestError(RequestErrorCode.INVALID_DATE)

        year = date.year
        month = date.month

        user = get_user(user_id)
        if not user:
            raise RequestError(RequestErrorCode.USER_NOT_FOUND)

        contratos = user['contratos'].get(contrato_id)
        if not contratos:
            raise RequestError(RequestErrorCode.CONTRACT_NOT_FOUND)

        info_contratos = contratos.get('info')
        if not info_contratos:
            return JsonResponse({'status': 'Contrato sem atividade'})

        current_month_data = next(
            (info for info in info_contratos if info['ano'] == year and info['mes'] == month), None
        )

        previous_months = [
            {
                "month": info['mes'],
                "usage_mb": info['mb_usado'],
                "percentage_of_plan_used": (info['mb_usado'] / info['total_contratado']) * 100
            }
            for info in info_contratos if info['ano'] == year and info['mes'] < month
        ]

        return JsonResponse({
            "user_name": user_id,
            "report_period": {
                "start_date": f"{year}-{month}-01",
                "end_date": f"{year}-{month}-{calendar.monthrange(year, month)[1]}",
            },
            "data_usage": {
                "total_usage_mb": current_month_data['mb_usado'],
                "peak_usage": current_month_data['horario_de_pico'],
                "data_remaining_mb": current_month_data['total_contratado'] - current_month_data['mb_usado'],
                "plan_limit_mb": current_month_data['total_contratado'],
                "percentage_used": (current_month_data['mb_usado'] / current_month_data['total_contratado']) * 100,
            },
            "historical_usage": {
                "previous_months": previous_months
            }
        })