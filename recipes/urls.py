from django.urls import inclucde, path
from . import views

urlpatterns = [
    path('', views.index, name = "index")
]
