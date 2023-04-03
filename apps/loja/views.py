from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView
from .models import Produtos
from apps.importacaocsv.import_csv import ImportFromCsv
from django.contrib import messages
from django_filters.views import FilterView
from apps.loja.filters import InvetarioFilter

class InputView(View):
    template_name = 'import_input.html'
    
    def post(self,*args):
        arquivo = self.request.FILES['arquivo']
        
        importador = ImportFromCsv(arquivo=arquivo)
        erros = importador.erros()
        importador.save()

        if not erros:
            messages.success(self.request,'Importado com sucesso.')
            return redirect('inventario')    
        
        for error in erros:
            messages.error(self.request,error)
        
        return render(self.request,self.template_name)


    def get(self,*args):
        return render(self.request,self.template_name)

class InventarioView(FilterView,ListView):
    model = Produtos
    title = 'Inventario'
    template_name = 'index_inventario.html'
    context_object_name = 'inventario'
    paginate_by = 10
    ordering = ['-pk']
    filterset_class = InvetarioFilter
    