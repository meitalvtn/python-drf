from django.db import models


class Transaction(models.Model):
    amount = models.IntegerField()
    destination = models.CharField(max_length=60)
    outgoing = models.BooleanField(default=False)

    def __str__(self):
        return f'(id: {self.id}, amount: {self.amount}, dest: {self.destination}, outgoing: {self.outgoing})'


class PolicyRule(models.Model):
    amount = models.IntegerField()

    def __str__(self):
        return f'(id: {self.id}, amount: {self.amount})'


class PolicyRuleDestination(models.Model):
    address = models.CharField(max_length=60)
    rule = models.ForeignKey(
        to=PolicyRule,
        related_name='destinations',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.address
