from typing import Any, Union, Dict
from rest_framework.response import Response
from datetime import datetime
from api.models import Wallets

from utils.exceptions import BaseExceptionError


class AbstractMain:
    """
        Abstract class for main logic class, it will assign 
        keyword arguments as 'keyword_args' so the child classes
        can fetch from 'keyword_args'
    """

    def __init__(self, *args, **kwargs):
        self.arguments = args
        self.keyword_args = kwargs


class ResponseAbstract:
    """
        Build response if the code are 200 or 201, which means  OK and CREATED.
    """

    def __init__(self, data:Union[Dict, str]) -> None:
        if isinstance(data, str):
            data = {
                "message":data
            }
        self.data = data
        self.response = {
            "status":None,
            "data":self.data
        }
        
    @property
    def ok(self):
        self.response['status'] = "success"
        return Response(data=self.response, status=200)
    
    @property
    def created(self):
        self.response['status'] = "success"
        return Response(data=self.response, status=201)


def timezone_to_str(time_value:datetime):
    """Convert DateTime value to String."""
    return time_value.strftime("%Y-%m-%dT%H:%M%S%z")

def integer_checker(value:Any):
    """Check if value is valid in integer type."""
    if not isinstance(value, int):
        try:
            amount = int(value)
        except Exception as e:
            raise BaseExceptionError(key="amount", message=e, code=400)
    return amount

def wallet_state(value:Wallets) -> None:
    """Check the wallet status."""
    if not value.is_active and value.disabled_at != None:
        raise BaseExceptionError(key="message", message="Wallet already disabled.", code=404)

    if not value.is_active and value.disabled_at == None:
        raise BaseExceptionError(key="message", message="Please enabled wallet first.", code=400)
