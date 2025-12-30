from django.urls import path

from apis.verifications.views import GenerateVerificationCodeAPIView, VerifyCodeAPIView
from apis.views import StudentListAPIView, MpesaSTKPushCallbackAPIView, ConfirmOrderPaymentAPIView
from apis.mpesa.views import MpesaSTKPushAPIView, ConfirmPaymentAPIView

urlpatterns = [
    path('generate-verification-code/', GenerateVerificationCodeAPIView.as_view(), name='generate-verification-code'),
    path('verify-code/', VerifyCodeAPIView.as_view(), name='verify-code'),
    path('students/', StudentListAPIView.as_view(), name='student-list'),
    path('stk-push-callback/', MpesaSTKPushCallbackAPIView.as_view(), name='mpesa-stk-push-callback'),
    path('stk-push/', MpesaSTKPushAPIView.as_view(), name='mpesa-stk-push'),
    path('confirm-mpesa-payment/', ConfirmPaymentAPIView.as_view(), name='confirm-mpesa-payment'),
    path('confirm-order-payment/', ConfirmOrderPaymentAPIView.as_view(), name='confirm-order-payment'),
]