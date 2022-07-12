from django.urls import path
from .views import SignUpView


urlpatterns = [
    path('singup/', SignUpView.as_view(), name='signup.html')
]