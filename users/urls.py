from django.urls import path
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(),name="signup")
] 