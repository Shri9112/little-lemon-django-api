from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking, MenuItem
from .serializers import BookingSerializer, MenuItemSerializer, RegistrationSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all().order_by("id")
    serializer_class = MenuItemSerializer
    # Public reads; only authenticated users can create, update or delete.
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("user").all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Authenticated users see only their own bookings; staff can see all.
        qs = Booking.objects.select_related("user").all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "token": token.key,
        }, status=201)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid username or password."}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from rest_framework.authtoken.models import Token
        Token.objects.filter(user=request.user).delete()
        return Response(status=204)
