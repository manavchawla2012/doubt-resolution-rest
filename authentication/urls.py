from django.urls import path

from authentication.api_views import LoginView, VerifyAuthView, LogoutView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('verify-token', VerifyAuthView.as_view(), name='verify'),
    path('logout', LogoutView.as_view(), name="logout")
]
