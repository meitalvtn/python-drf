from django.db import models


class Transaction(models.Model):
    amount = models.IntegerField()
    dest = models.CharField(max_length=60)  # TODO: max length?
    outgoing = models.BooleanField(default=False) # TODO: Should this be here?

    def __str__(self):
        return f'(amount: {self.amount}, dest: {self.dest}, outgoing: {self.outgoing})'


class PolicyRule(models.Model):
    max = models.IntegerField()

    def __str__(self):
        return f'(amount: {self.max})'


class PolicyRuleDestination(models.Model):
    address = models.CharField(max_length=60)
    rule = models.ForeignKey(
        to=PolicyRule,
        related_name='dests',
        on_delete=models.CASCADE, # TODO: make sure this is what u want
        blank=True,
        null=True
    )

    def __str__(self):
        return self.address
