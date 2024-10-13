from abc import ABC

from starburst.error import RequestError, RequestErrorCode
from starburst.models.Client import Client


class BaseApiIntegration(ABC):
    def __init__(self, request, request_data):
        request.api_integration = self
        self.request = request
        self.request_data = request_data

        try:
            self.client = Client.objects.get(str_id=request_data['client'])
        except RequestError:
            raise RequestError(RequestErrorCode.CLIENT_NOT_FOUND)

