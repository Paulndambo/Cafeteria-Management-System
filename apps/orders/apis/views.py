from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from apps.orders.apis.serializers import SessionCreateSerializer
from apps.orders.models import TemporaryCustomerOrderItem, TemporaryOrderItem
from apps.students.models import Student
from apps.inventory.models import Menu


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


class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        menu_id = request.data.get('menu_id')
        student_id = request.data.get('student_id')
        
        if not menu_id or not student_id:
            return Response(
                {'error': 'menu_id and student_id are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            menu_item = Menu.objects.get(id=menu_id)
            user = request.user
            
            # Check if item already exists in cart
            item_check = TemporaryOrderItem.objects.filter(
                student_id=student_id,
                menu_item=menu_item,
                user=user
            ).first()
            
            total_price = menu_item.price * 1
            
            if item_check:
                item_check.quantity += 1
                item_check.price += total_price
                item_check.save()
            else:
                TemporaryOrderItem.objects.create(
                    user=user,
                    student_id=student_id,
                    menu_item=menu_item,
                    quantity=1,
                    price=total_price
                )
            
            # Get updated cart data
            items = TemporaryOrderItem.objects.filter(student_id=student_id, user=user)
            order_value = sum(items.values_list("price", flat=True))
            
            cart_items = []
            for item in items:
                cart_items.append({
                    'id': item.id,
                    'menu_item': item.menu_item.item,
                    'quantity': item.quantity,
                    'price': float(item.price),
                    'menu_item_price': float(item.menu_item.price),
                    'max_quantity': item.menu_item.quantity
                })
            
            return Response({
                'success': True,
                'message': 'Item added to cart',
                'cart_items': cart_items,
                'order_value': float(order_value)
            }, status=status.HTTP_200_OK)
            
        except Menu.DoesNotExist:
            return Response(
                {'error': 'Menu item not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IncreaseQuantityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item_id = request.data.get('item_id')
        student_id = request.data.get('student_id')
        
        if not item_id or not student_id:
            return Response(
                {'error': 'item_id and student_id are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            item = TemporaryOrderItem.objects.get(id=item_id, student_id=student_id)
            item.quantity += 1
            item.price += item.menu_item.price
            item.save()
            
            # Get updated cart data
            user = request.user
            items = TemporaryOrderItem.objects.filter(student_id=student_id, user=user)
            order_value = sum(items.values_list("price", flat=True))
            
            cart_items = []
            for cart_item in items:
                cart_items.append({
                    'id': cart_item.id,
                    'menu_item': cart_item.menu_item.item,
                    'quantity': cart_item.quantity,
                    'price': float(cart_item.price),
                    'menu_item_price': float(cart_item.menu_item.price),
                    'max_quantity': cart_item.menu_item.quantity
                })
            
            return Response({
                'success': True,
                'message': 'Quantity increased',
                'cart_items': cart_items,
                'order_value': float(order_value)
            }, status=status.HTTP_200_OK)
            
        except TemporaryOrderItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DecreaseQuantityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item_id = request.data.get('item_id')
        student_id = request.data.get('student_id')
        
        if not item_id or not student_id:
            return Response(
                {'error': 'item_id and student_id are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            item = TemporaryOrderItem.objects.get(id=item_id, student_id=student_id)
            
            if item.quantity > 1:
                item.quantity -= 1
                item.price -= item.menu_item.price
                item.save()
            else:
                # If quantity is 1, remove the item
                item.delete()
            
            # Get updated cart data
            user = request.user
            items = TemporaryOrderItem.objects.filter(student_id=student_id, user=user)
            order_value = sum(items.values_list("price", flat=True))
            
            cart_items = []
            for cart_item in items:
                cart_items.append({
                    'id': cart_item.id,
                    'menu_item': cart_item.menu_item.item,
                    'quantity': cart_item.quantity,
                    'price': float(cart_item.price),
                    'menu_item_price': float(cart_item.menu_item.price),
                    'max_quantity': cart_item.menu_item.quantity
                })
            
            return Response({
                'success': True,
                'message': 'Quantity decreased',
                'cart_items': cart_items,
                'order_value': float(order_value)
            }, status=status.HTTP_200_OK)
            
        except TemporaryOrderItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item_id = request.data.get('item_id')
        student_id = request.data.get('student_id')
        
        if not item_id or not student_id:
            return Response(
                {'error': 'item_id and student_id are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            item = TemporaryOrderItem.objects.get(id=item_id)
            item.delete()
            
            # Get updated cart data
            user = request.user
            items = TemporaryOrderItem.objects.filter(student_id=student_id, user=user)
            order_value = sum(items.values_list("price", flat=True))
            
            cart_items = []
            for cart_item in items:
                cart_items.append({
                    'id': cart_item.id,
                    'menu_item': cart_item.menu_item.item,
                    'quantity': cart_item.quantity,
                    'price': float(cart_item.price),
                    'menu_item_price': float(cart_item.menu_item.price),
                    'max_quantity': cart_item.menu_item.quantity
                })
            
            return Response({
                'success': True,
                'message': 'Item removed from cart',
                'cart_items': cart_items,
                'order_value': float(order_value)
            }, status=status.HTTP_200_OK)
            
        except TemporaryOrderItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )