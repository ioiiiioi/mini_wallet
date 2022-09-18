"""
    The logic class was splitted from view.
    this way whenever we decided to create new gateway e.g.: GraphQL or gRPC
    we no need to write the main functions repeatedly.
"""

from .models import(
    User,
    Wallets,
    Transactions
)
from utils.authenticator import encoder
from utils.abstract import (
    AbstractMain, 
    integer_checker, 
    timezone_to_str,
    wallet_state
)
from utils.exceptions import BaseExceptionError
from django.db import transaction 
from django.utils import timezone

@transaction.atomic
class WalletBase(AbstractMain):

    """
        Main logic for this API
    """

    @property
    def create(self):
        customer_id = self.keyword_args.get("customer_xid", None)

        try:
            user = User.objects.get(pk=customer_id, is_active=True)
        except User.DoesNotExist:
            data = {
                "user":"User already deleted",
            }
            raise BaseExceptionError(key="user", message="User already deleted.", code=404)

        wallet = Wallets.objects.create(owned_by=user)
        data = {
            "token":f"Token {encoder(wallet.pk)}"
        }
        return data

    @property
    def read(self):
        wallet = self.keyword_args.get("wallet")
        wallet_state(wallet)

        data = {
            "id":wallet.pk,
            "owned_by":wallet.owned_by.pk,
            "status":wallet.status,
            "enabled_at":timezone_to_str(wallet.enabled_at),
            "balance":wallet.balance,
        }
        return data

    @property
    def activate(self):
        wallet = self.keyword_args.get("wallet")
        if (not wallet.is_active) and wallet.disabled_at != None:
            raise BaseExceptionError(key="message", message="Wallet already disabled.", code=404)

        setattr(wallet, "is_active", True)
        wallet.save()
        data = {
            "id":wallet.pk,
            "owned_by":wallet.owned_by.pk,
            "status":wallet.status,
            "enabled_at":timezone_to_str(wallet.enabled_at),
            "balance":wallet.balance,
        }
        return data

    @property
    def delete(self):
        is_active_value = not (self.keyword_args.get("is_active"))
        wallet = self.keyword_args.get("wallet")
        wallet_state(wallet)

        setattr(wallet, "is_active", is_active_value)
        setattr(wallet, "disabled_at", timezone.now())
        wallet.save()

        data = {
            "id":wallet.pk,
            "owned_by":wallet.owned_by.pk,
            "status":wallet.status,
            "balance":wallet.balance,
            "disabled_at":timezone_to_str(wallet.disabled_at),
        }
        return data

    @property
    def update(self):
        wallet = self.keyword_args.get("wallet")
        wallet_state(wallet)

        fields = [
            "enabled_at",
            "balance",
            "is_active",
            "disabled_at",
        ]
        for field in fields:
            data = self.keyword_args.get(field, None)
            if data is not None:
                setattr(wallet, field, data)

        wallet.save()
        data = {
            "id":wallet.pk,
            "owned_by":wallet.owned_by.pk,
            "status":wallet.status,
            "enabled_at":timezone_to_str(wallet.enabled_at),
            "balance":wallet.balance,
        }
        return data

    @property
    def deposit(self):
        """
            Status supposed to be in pending state, because it's need confirmation from Switcher/Bank partner.
            but in this case im by pass it straight to success state because it's just mockups. 
        """
        wallet = self.keyword_args.get("wallet")
        wallet_state(wallet)

        amount = integer_checker(self.keyword_args.get("amount"))
        
        transaction = Transactions.objects.create(
            reference_id=self.keyword_args.get("reference_id"),
            wallet=wallet,
            creator=self.keyword_args.get("creator"),
            status=Transactions.TransactionStatuses.SUCCESS,
            type=Transactions.TransactionTypes.DEPOSIT,
            amount=amount,
        )

        wallet.balance += amount
        wallet.save()

        response = {
            "id":transaction.pk,
            "deposited_by":transaction.creator.pk,
            "status":transaction.status,
            "deposited_at":timezone_to_str(transaction.created_at),
            "amount":transaction.amount,
            "reference_id":transaction.reference_id
        }
        return response

    @property
    def withdraw(self):
        """
            Status supposed to be in pending state, because it's need confirmation from payment gateway partner.
            but in this case im by pass it straight to success state because it's just mockups. 
        """

        wallet = self.keyword_args.get("wallet")
        wallet_state(wallet)

        amount = integer_checker(self.keyword_args.get("amount"))

        if (wallet.balance - amount) <= -1:
            raise BaseExceptionError(key="message",message="Wallet balance is not enough.", code=400)

        transaction = Transactions.objects.create(
            reference_id=self.keyword_args.get("reference_id"),
            wallet=wallet,
            creator=self.keyword_args.get("creator"),
            status=Transactions.TransactionStatuses.SUCCESS,
            type=Transactions.TransactionTypes.WITHDRAWAL,
            amount=amount,
        )

        wallet.balance -= amount
        wallet.save()

        response = {
            "id":transaction.pk,
            "withdrawn_by":transaction.creator.pk,
            "status":transaction.status,
            "withdrawn_at":timezone_to_str(transaction.created_at),
            "amount":transaction.amount,
            "reference_id":transaction.reference_id
        }
        return response