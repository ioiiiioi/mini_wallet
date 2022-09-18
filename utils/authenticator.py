import uuid
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from api.models import Wallets
from utils.exceptions import BaseExceptionError


def encoder(key:uuid.UUID):
    """Basic encoder from HEX to UUID, it's only adding the '-' value to its place """
    key = key.hex
    return key

def decoder(key:str):
    """Basic decoder for UUID to HEX, it's only remove the '-' value from UUID"""
    try:
        key = uuid.UUID(hex=key)
        return key
    except ValueError:
        data = {
            "Token":"Invalid token."
        }
        raise BaseExceptionError(key="message", message="Invalid Token.", code=401)


class CustomAuthentication(BaseAuthentication):
    """
        Create authentication schema based on BaseAuthentication.
        im changing user filter with wallet filter and then fetch the user 
        from wallet's attribute.

        Also im put user queryset and wallet queryset into the request, so
        my main logic does not have to query the wallet again.
    """
    def authenticate(self, request):
        raw_token = request.META.get('HTTP_AUTHORIZATION', None)
        if not raw_token:
            return None

        token_schema, token = raw_token.split()
        if token_schema.lower() != "token":
            raise BaseExceptionError(key="message", message='Wrong token schema.', code=401)
        token = decoder(key=token)
        try:
            wallet = Wallets.objects.select_related("owned_by").get(pk=token)
        except Wallets.DoesNotExist:
            raise BaseExceptionError(key="message", message='No such user.', code=401)
        
        setattr(request, "user", wallet.owned_by)
        setattr(request, "wallet", wallet)

        return (wallet.owned_by, None)