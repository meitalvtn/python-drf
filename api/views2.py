from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionAPIView(APIView):
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
            serializer = TransactionSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetails(APIView):
    def get_object(self, id):
        try:
            transaction = Transaction.objects.get(pk=id)

        except Transaction.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        transaction = self.get_object(id)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, id):
        transaction = self.get_object(id)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        transaction = self.get_object(id)
        transaction.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)





# @api_view(['GET', 'POST'])
# def transaction_list(request):
#     if request.method == 'GET':
#         transactions = Transaction.objects.all()
#         serializer = TransactionSerializer(transactions, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = TransactionSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def transaction_detail(request, pk):
#     try:
#         transaction = Transaction.objects.get(pk=pk)
#
#     except Transaction.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = TransactionSerializer(transaction)
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         serializer = TransactionSerializer(transaction, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == "DELETE":
#         transaction.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)