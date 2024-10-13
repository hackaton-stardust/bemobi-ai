from django.views.decorators.csrf import csrf_exempt

from starburst.api.payment import PaymentIntegration
from starburst.api.subscription import Subscription
from starburst.error import RequestError, RequestErrorCode


@csrf_exempt
def payment_analysis(request):
    if request.method != 'GET':
        raise RequestError(RequestErrorCode.METHOD_NOT_ALLOWED)

    return PaymentIntegration(request, request.GET.copy()).payment_analysis()

@csrf_exempt
def mobile_data_analysis(request):
    if request.method != 'GET':
        raise RequestError(RequestErrorCode.METHOD_NOT_ALLOWED)

    return Subscription(request, request.GET.copy()).mobile_data_analysis()