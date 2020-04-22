from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .exchange import convert_to_satoshis
from .models import Transaction, PolicyRule
from .serializers import TransactionSerializer, PolicyRuleSerializer

'''View for list of transactions'''


class TransactionAPIView(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter() # TODO add outgoing=True to filter
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        transaction_amount = request.data['amount']
        transaction_dest = request.data['destination']

        # get all rules where amount greater than transaction amount OR
        # where amount is 0 (unlimited) AND
        # where transaction destination is in that rule's destinations list OR
        # where that rule acccepts any destination
        rules = PolicyRule.objects.filter(
              (Q(amount__gt=transaction_amount) | Q(amount=0))
            & (Q(destinations__address=transaction_dest) | Q(destinations__address=None)))

        print(rules)

        # set outgoing according to whether or not at least one match was found
        request.data['outgoing'] = rules.count() != 0

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
            # translate to satoshis
            request.data['amount'] = int(convert_to_satoshis(request.data['amount'], currency))

        serializer = PolicyRuleSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''View for single policy rule'''


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
        serializer = PolicyRuleSerializer(rule, data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        rule = self.get_rule(id)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
