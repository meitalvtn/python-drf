from rest_framework import serializers
from .models import Transaction, PolicyRule, PolicyRuleDestination


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'destination', 'outgoing']


class PolicyRuleDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyRuleDestination
        fields = ['address']

    def to_internal_value(self, data):
        return {'address': data}

    def to_representation(self, instance):
        return instance.address


class PolicyRuleSerializer(serializers.ModelSerializer):
    destinations = PolicyRuleDestinationSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = PolicyRule
        fields = ['id', 'amount', 'destinations']

    def create(self, validated_data):
        dests_data = validated_data.pop('destinations')
        rule = PolicyRule.objects.create(**validated_data)
        if dests_data:
            for dest_data in dests_data:
                PolicyRuleDestination.objects.create(rule=rule, **dest_data)
        return rule

    def update(self, instance, validated_data):
        instance.amount = validated_data['amount']
        dests_data = validated_data.pop('destinations')

        # to support additions and deletions, clear out all destinations
        PolicyRuleDestination.objects.filter(rule_id=instance.id).delete()

        # re-add destinations according to request data
        if dests_data:
            for dest_data in dests_data:
                PolicyRuleDestination.objects.create(rule=instance, **dest_data)

        return instance
