from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.apis.serializers import SessionCreateSerializer
from apps.orders.models import TemporaryCustomerOrderItem, TemporaryOrderItem
from apps.students.models import Student


class SessionCreateAPIView(generics.CreateAPIView):
    serializer_class = SessionCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        cashier_id = request.current_cashier

        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            registration_number = serializer.validated_data["registration_number"]
            student = Student.objects.get(registration_number=registration_number)
            #print(f"Name: {student.user.first_name} {student.user.last_name}, Bal: {student.wallet_balance}, ID: {student.id}")
            
            TemporaryCustomerOrderItem.objects.all().delete()
            TemporaryOrderItem.objects.filter(student=student).delete()

            request.session[f'selected_student_{cashier_id}'] = {
                'id': student.id,
                'last_name': student.user.last_name,
                'first_name': student.user.first_name,
                'registration_number': student.registration_number,
                'wallet_balance': str(student.wallet_balance),
                'cashier_id': cashier_id
            }

            selected_student = request.session.get(f'selected_student_{cashier_id}', {})

            print(f"User With Cashier: {selected_student}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)