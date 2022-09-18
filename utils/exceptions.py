from typing import Any
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class BaseExceptionError(APIException):
    """
        Use to replace basic exception. so we can raise an exception as json response
    """
    default_detail = {
        "status":"error",
        "data":{
            "detail":"A server error occurred."
        }
    }
    status_code = 500

    def __init__(self, key=None, message=None, code=None):
        detail = self.default_detail
        if key and message:
            detail = {
                "status":"fail",
                "data":{
                    key:message
                }
            }

        if code is not None:
            self.status_code = code
        
        super().__init__(detail, self.default_code)
