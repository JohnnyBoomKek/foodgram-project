from django.urls import path
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    # path() для страницы регистрации нового пользователя
    # её полный адрес будет auth/signup/, но префикс auth/ обрабатывется в головном urls.py
    path("signup/", views.SignUp.as_view(),name="signup")
] 