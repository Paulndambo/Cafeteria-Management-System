from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apis.verifications.serializers import GenerateVerificationCodeSerializer, CodeVerificationSerializer
from apis.verifications.generate_code import generate_secure_5_digit_code
from apis.models import VerificationCode
from apps.students.models import Student


class GenerateVerificationCodeAPIView(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = GenerateVerificationCodeSerializer

    def post(self, request, *args, **kwargs):
        # Implement verification logic here
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = generate_secure_5_digit_code()
            # Here you would typically save the code to the database associated with the user
            VerificationCode.objects.create(
                code=code,
                student=Student.objects.get(registration_number=serializer.validated_data['registration_number'])
            )
            return Response({"message": "Verification code generated", "code": code}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VerifyCodeAPIView(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = CodeVerificationSerializer

    def post(self, request, *args, **kwargs):
        # Implement code verification logic here
        print("Received data:", request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            last_code = VerificationCode.objects.filter(
                student__registration_number=serializer.validated_data['registration_number'],
                is_verified=False
            ).order_by('-created').first()

            if last_code is None or serializer.validated_data['verification_code'] != last_code.code:
                print(f"Expected: {last_code.code if last_code else 'None'}, Received: {serializer.validated_data['verification_code']}")
                return Response({"message": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
            last_code.is_verified = True
            last_code.save()
            return Response({"message": "Code verified successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)