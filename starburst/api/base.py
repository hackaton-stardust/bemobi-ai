from abc import ABC

from starburst.error import RequestError, RequestErrorCode
from starburst.models.models import get_client


class BaseApiIntegration(ABC):
    def __init__(self, request, request_data):
        request.api_integration = self
        self.request = request
        self.request_data = request_data

        try:
            self.client = get_client(client_id=request_data.get('client'))
        except KeyError:
            raise RequestError(RequestErrorCode.CLIENT_NOT_FOUND)

