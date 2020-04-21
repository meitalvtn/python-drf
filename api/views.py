from django.db import transaction
from django.db.models import Q
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from .serializers import PolicyRuleDestinationSerializer
from .exchange import convert_to_satoshis
from .models import Transaction, PolicyRule, PolicyRuleDestination
from .serializers import TransactionSerializer, PolicyRuleSerializer


# TODO change max to amount and dests to destinations

'''View for list of transactions'''
class TransactionAPIView(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter() # TODO add outgoing=True to filter
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):

        transaction_amount = request.data['amount']
        transaction_dest = request.data['dest']

        # get all rules with max greater than the transaction value or max equal to 0 (unlimited)
        rules = PolicyRule.objects.filter(
              (Q(max__lt=transaction_amount) | Q(max=0))
            & (Q(dests__address=transaction_dest) | Q(dests__address=None)))

        request.data['outgoing'] = rules.count() != 0

        if not request.data.get("outgoing"):  # TODO remove
            print('no match found')

        # write to db
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''View for list of policy rules'''
class PolicyRuleAPIView(APIView):
    def get(self, request):
        rules = PolicyRule.objects.all()
        serializer = PolicyRuleSerializer(rules, many=True)
        return Response(serializer.data)

    def post(self, request):
        currency = request.data.pop('currency', None)
        if currency:
            # tranlsate to satoshis
            request.data['max'] = int(convert_to_satoshis(request.data['max'], currency))

        serializer = PolicyRuleSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolicyRuleDetailAPIView(APIView):
    def get_rule(self, id):
        try:
            return PolicyRule.objects.get(pk=id)

        except PolicyRule.Response:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        rule = self.get_rule(id)
        serializer = PolicyRuleSerializer(rule)
        return Response(serializer.data)

    def put(self, request, id):
        rule = self.get_rule(id)
        print(rule, request.data, id)
        serializer = PolicyRuleSerializer(rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        rule = self.get_rule(id)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
