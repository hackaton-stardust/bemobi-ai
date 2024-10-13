from enum import IntEnum


class RequestErrorCode(IntEnum):
    def __new__(cls, code, message):
        obj = int.__new__(cls, code)
        obj._value_ = code
        obj.message = message

        return obj

    def __str__(self):
        return f"{self.__class__.__name__}.{self._name_}"

    METHOD_NOT_ALLOWED = 1000, 'Method not allowed.',
    CLIENT_NOT_FOUND = 1001, 'Client not found.',
    USER_NOT_FOUND = 1002, 'User not found.',
    MISSING_PARAMETER = 1003, 'Some parameters are missing.',
    INVALID_DATE = 1004, 'Invalid date.',
    CONTRACT_NOT_FOUND = 1005, 'Contract not found.',


class RequestError(Exception):
    def __init__(self, error):
        self.error = error
