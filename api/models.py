import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)

class BaseModels(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True

class User(AbstractUser, BaseModels):
    """
        Inherited from AbstracUser class for user property.
        Inherited from BaseModels class for customize id as UUID.
    """
    pass

class Wallets(BaseModels):

    owned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallet")
    enabled_at = models.DateTimeField(auto_now_add=True)
    balance = models.FloatField(null=True, blank=True, default=0.0)
    is_active = models.BooleanField(null=True, blank=True, default=False)
    disabled_at = models.DateTimeField(null=True, blank=True)

    @property
    def status(self):
        return "enabled" if self.is_active else "disabled"


class Transactions(BaseModels):
    
    class TransactionTypes(models.TextChoices):
        DEPOSIT = ("deposit", "deposit")
        WITHDRAWAL = ("withdrawal", "withdrawal")
    
    class TransactionStatuses(models.TextChoices):
        PENDING = ("pending", "pending")
        SUCCESS = ("success", "success")
        FAILED = ("failed", "failed")

    reference_id = models.UUIDField(null=True, blank=True, default=uuid.uuid4)
    wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE, related_name="transactions")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    status = models.CharField(max_length=7, choices=TransactionStatuses.choices, null=True, blank=True, default=TransactionStatuses.PENDING)
    type = models.CharField(max_length=11, choices=TransactionTypes.choices, null=True, blank=True, default=TransactionTypes.DEPOSIT)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

