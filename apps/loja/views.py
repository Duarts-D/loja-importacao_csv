from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Produtos
# Create your views here.
class InputView(View):
    def get(self,*args):
        return render(self.request,'import_input.html')

class InventarioView(ListView):
    template_name = 'index_inventario.html'
    model = Produtos
    context_object_name = 'inventario'