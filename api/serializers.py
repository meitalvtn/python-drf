from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Transaction, PolicyRule, PolicyRuleDestination


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'dest', 'outgoing']  # TODO: remove outgoing field


class PolicyRuleDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyRuleDestination
        fields = ['address']

    def to_internal_value(self, data):
        return {'address': data}

    def to_representation(self, instance):
        return instance.address



class PolicyRuleSerializer(serializers.ModelSerializer):
    dests = PolicyRuleDestinationSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = PolicyRule
        fields = ['id', 'max', 'dests']

    def create(self, validated_data):
        print(validated_data)
        dests_data = validated_data.pop('dests')
        rule = PolicyRule.objects.create(**validated_data)
        if dests_data:
            for dest_data in dests_data:
                PolicyRuleDestination.objects.create(rule=rule, **dest_data)
        return rule
