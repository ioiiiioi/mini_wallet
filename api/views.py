"""
    View classes and functions for API. 
    basically this is the API gateway. Whenever the payload
    is not match with the logic side, it will raised here, so 
    the logic side can perform for logic calculations.
"""

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from api.models import Wallets
from utils.abstract import ResponseAbstract
from utils.authenticator import CustomAuthentication, decoder
from utils.exceptions import BaseExceptionError
from .main import WalletBase

@api_view(["POST"])
def init_wallet(request):
    customer_xid = request.data.get("customer_xid")
    if not customer_xid:
        raise BaseExceptionError(key="customer_xid", message="Required customer_xid.", code=400)
    wallet = WalletBase(customer_xid=customer_xid).create
    data = {
        "token":wallet
    }
    return ResponseAbstract(data).created


class WalletAPI(APIView):

    authentication_classes = [CustomAuthentication,]

    def post(self, request):
        """Enabled wallet"""
        wallet = request.wallet
        wallet = WalletBase(wallet=wallet).activate
        data = {
            "wallet":wallet
        }
        return ResponseAbstract(data).ok

    def get(self, request):
        """View wallet"""
        wallet = request.wallet
        wallet = WalletBase(wallet=wallet).read
        data = {
            "wallet":wallet
        }
        return ResponseAbstract(data).ok

    def patch(self, request):
        """Disabled wallet"""
        wallet = request.wallet
        is_disabled = request.data.get("is_disabled", None)
        if not is_disabled:
            raise BaseExceptionError(key="is_disabled", message="Required is_disabled value.", code=400)

        wallet = WalletBase(wallet=wallet, is_active=is_disabled).delete
        data = {
            "wallet":wallet
        }
        return ResponseAbstract(data).ok


@api_view(["POST"])
@authentication_classes([CustomAuthentication])
def deposit(request):
    amount = request.data.get("amount", None)
    reference_id = request.data.get("reference_id", None)
    if not amount or amount == 0:
        raise BaseExceptionError(key="message", message="Amount cannot be null or 0.", code=400)
    
    if not reference_id:
        raise BaseExceptionError(key="message", message="Reference id cannot be null or empty.", code=400)

    payload = {
        "wallet":request.wallet,
        "creator":request.user,
        "amount":amount,
        "reference_id":reference_id,
    }
    transaction = WalletBase(**payload).deposit
    data = {
        "deposit":transaction
    }
    return ResponseAbstract(data).ok

@api_view(["POST"])
@authentication_classes([CustomAuthentication])
def withdraw(request):
    amount = request.data.get("amount", None)
    reference_id = request.data.get("reference_id", None)
    if not amount or amount == 0:
        raise BaseExceptionError(key="message", message="Amount cannot be null or 0.", code=400)
    
    if not reference_id:
        raise BaseExceptionError(key="message", message="Reference id cannot be null or empty.", code=400)

    payload = {
        "wallet":request.wallet,
        "creator":request.user,
        "amount":amount,
        "reference_id":reference_id,
    }
    transaction = WalletBase(**payload).withdraw
    data = {
        "deposit":transaction
    }
    return ResponseAbstract(data).ok