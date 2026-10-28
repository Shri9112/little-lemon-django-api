from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, LoginView, LogoutView, MenuItemViewSet, RegisterView

router = DefaultRouter()
router.register("menu", MenuItemViewSet, basename="menu")
router.register("bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", include(router.urls)),
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
