from django.contrib import admin
from .models import Transaction, PolicyRule, PolicyRuleDestination

admin.site.register(Transaction)
admin.site.register(PolicyRule)
admin.site.register(PolicyRuleDestination)