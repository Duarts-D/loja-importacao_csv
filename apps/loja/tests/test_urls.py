from django.urls import reverse,resolve
from apps.loja.views import InputView,InventarioView

class TestLojaUrls:
    def test_inputview_url_e_esta_retornando_correto(self):
        entrada = reverse('input_form')
        saida = InputView
        
        assert resolve(entrada).func.view_class == saida
    
    def test_inventario_url_e_esta_retornando_correto(self):
        entrada = reverse('inventario')
        saida = InventarioView

        assert resolve(entrada).func.view_class == saida