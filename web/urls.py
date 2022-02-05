from django.urls import path,re_path
from . import views

urlpatterns = [
    path("submit/expense" , views.submit_expense ),
    path("submit/income", views.submit_income),
    path("register/" ,views.register),

]
