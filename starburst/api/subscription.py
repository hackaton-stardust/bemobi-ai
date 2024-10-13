import calendar

from django.http import JsonResponse
from django.utils import timezone

from starburst.api.base import BaseApiIntegration
from starburst.error import RequestError, RequestErrorCode


class Subscription(BaseApiIntegration):

    def mobile_data_analysis(self):
        data = self.request_data
        user_id = data.get('user_id')
        date = data.get('date')
        contract_id = data.get('contract_id')

        if not user_id:
            raise RequestError(RequestErrorCode.MISSING_PARAMETER)

        if not date:
            date = timezone.now()
        else:
            try:
                date = timezone.make_aware(timezone.datetime.fromisoformat(date))
            except ValueError:
                raise RequestError(RequestErrorCode.INVALID_DATE)

        year = date.year
        month = date.month

        try:
            user = User.objects.get(pk=user_id) #FIXME
        except User.DoesNotExist:
            raise RequestError(RequestErrorCode.USER_NOT_FOUND)

        recent_subscriptions = ContractsInfo.objects.filter(
            contract_id=contract_id,
            contract__type='mobile',
            year=date.year
        )

        subscription_info = recent_subscriptions.filter(month=date.month)

        if not subscription_info:
            raise RequestError(RequestErrorCode.CONTRACT_NOT_FOUND)

        return JsonResponse({
            "user_name": user.name,
            "report_period": {
                "start_date": f"{year}-{month}-01",
                "end_date": f"{year}-{month}-{calendar.monthrange(year, month)[1]}",
            },
            "data_usage": {
                "total_usage_mb": subscription_info.mb_used,
                "peak_usage": subscription_info.peak_used,
                "data_remaining_mb": subscription_info.data_remaining(),
                "plan_limit_mb": subscription_info.limit_mb,
                "percentage_used": (subscription_info.mb_used / subscription_info.limit_mb) * 100,
        "historical_usage": {
        },
            "previous_months": [{
                "month": month,
                "usage_mb": subs.mb_used,
                "percentage_of_plan_used": (subs.mb_used / subs.limit_mb) * 100
            } for subs in recent_subscriptions]
        }})