from django.urls import path
from .views import InputView

urlpatterns = [
    path('',InputView.as_view(),name='input_form')
]