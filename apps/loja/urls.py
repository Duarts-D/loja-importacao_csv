from django.urls import path
from .views import InputView,InventarioView

urlpatterns = [
    path('importa_arquivo/',InputView.as_view(),name='input_form'),
    path('',InventarioView.as_view(),name='inventario')
]