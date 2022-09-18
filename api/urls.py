from django.urls import path
from .views import (
    init_wallet,
    deposit,
    withdraw,
    WalletAPI,
)

urlpatterns = [
    path("v1/init", init_wallet, name="init_wallet"),
    path("v1/wallet", WalletAPI.as_view(), name="enable_wallet"),
    path("v1/wallet/deposits", deposit, name="deposits_wallet"),
    path("v1/wallet/withdrawals", withdraw, name="withdrawals_wallet"),
]