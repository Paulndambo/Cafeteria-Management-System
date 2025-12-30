from urllib import response
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from apps.students.models import Student
from apis.serializers import StudentSerializer, MpesaCallbackSerializer, OrderConfirmationSerializer
from apis.models import MpesaTransaction
from apis.mpesa.support_functions import cleanup_mpesa_callback, cleanup_phone_number
# Create your views here.
class StudentListAPIView(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class MpesaSTKPushCallbackAPIView(generics.GenericAPIView):
    serializer_class = MpesaCallbackSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Process the callback data as needed
            callback_data = serializer.validated_data

            
            cleaned_data = cleanup_mpesa_callback(callback_data)
            print("Cleaned Data:", cleaned_data)

            # Update the MpesaTransaction based on the callback data
            merchant_request_id = cleaned_data.get("merchant_request_id")
            try:
                transaction = MpesaTransaction.objects.get(merchant_request_id=merchant_request_id)
                transaction.result_code = cleaned_data.get("result_code")
                transaction.result_desc = cleaned_data.get("result_desc")
                transaction.amount = cleaned_data.get("amount")
                transaction.mpesa_receipt_number = cleaned_data.get("mpesa_receipt_number")
                transaction.balance = cleaned_data.get("balance")
                transaction.transaction_date = cleaned_data.get("transaction_date")
                transaction.phone_number = cleaned_data.get("phone_number")
                
                if transaction.result_code == 0:
                    transaction.status = 'Successful'
                else:
                    transaction.status = 'Failed'
                
                transaction.save()
            except MpesaTransaction.DoesNotExist:
                print(f"No transaction found for MerchantRequestID: {merchant_request_id}")

            # For demonstration, we just return the received data
            return Response({"status": "success", "data": callback_data}, status=status.HTTP_200_OK)            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
    


class ConfirmOrderPaymentAPIView(generics.GenericAPIView):
    serializer_class = OrderConfirmationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        print("Request Data:", request.data)

        if serializer.is_valid(raise_exception=True):
            # Process the callback data as needed
            return Response({"status": "Order payment confirmed"}, status=status.HTTP_200_OK)            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)