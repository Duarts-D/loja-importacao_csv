from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView
from .models import Produtos
from apps.importacaocsv.import_csv import ImportFromCsv
from django.contrib import messages

class InputView(View):
    template_name = 'import_input.html'
    
    def post(self,*args):
        arquivo = self.request.FILES['arquivo']
        
        importar = ImportFromCsv(arquivo)
        
        if not importar.erros():
            importar.save(Produtos)
            messages.success(self.request,'Importado com sucesso')
            return redirect('inventario')
        
        for message in importar.erros():
            messages.error(self.request,message)

        return render(self.request,self.template_name)

    def get(self,*args):
        return render(self.request,self.template_name)

class InventarioView(ListView):
    template_name = 'index_inventario.html'
    model = Produtos
    context_object_name = 'inventario'