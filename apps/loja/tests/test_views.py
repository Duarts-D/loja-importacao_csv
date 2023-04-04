from django.urls import reverse
import pytest
from io import BytesIO
from apps.loja.models import Fabricante,Produtos

@pytest.mark.django_db
class TestLojaViewsInputView:
    def setup_method(self):
        arquivo = BytesIO(b'manufacturer,model,color,carrier_plan_type,quantity,price\n\
                            Motorola,Moto G5 16GB,Preto,pre,20,1299\n\
                            Motorola,Moto G5 16GB,Preto,pos,20,599')
        arquivo.name = 'arquivo_txt'
        self.arquivo = arquivo

    def test_inputview_get_template_retorna_html_import_input_html(self,client):
        entrada = client.get(reverse('input_form'))
        esperando = 'import_input.html'

        assert entrada.status_code == 200
        assert entrada.templates[0].name == esperando

    def test_inputview_post_arquivo_invalido_retonando_error_igual_1(self,client):
        
        entrada = client.post(reverse('input_form'),{'arquivo':self.arquivo})
        
        assert entrada.status_code == 200
        assert len(entrada.context['messages']) == 1

    def test_inputview_post_arquivo_valido_redirecionando_para_inventario_e_retornando_msg(self,client):
        arquivo = self.arquivo
        arquivo.name = 'arquivo.csv'
        entrada = client.post(reverse('input_form'),{'arquivo':arquivo})

        assert entrada.status_code == 302
        entrada_inventario = client.get(reverse('inventario'))
        assert len(entrada_inventario.context['messages']) == 1
    
    def test_inputview_post_arquivo_tipo_valido_com_erros_4_retornados(self,client):
        arquivo = BytesIO(b'manufacturer,model,color,carrier_plan_type,quantity,price\n\
                            Motorola,,Preto,pre,20,1299\n\
                            Motorola,Moto G5 16GB,Preto,pos,b20,599\n\
                            bb,bbb,bbb,,,,')
        arquivo.name = 'arquivo.csv'
        entrada = client.post(reverse('input_form'),{'arquivo':arquivo})
        assert len(entrada.context['messages']) == 4 

@pytest.mark.django_db 
class TestViewInvetarioView:
    def setup_method(self):
        fabricante = Fabricante.objects.create(fabricante='Motorola')
        self.queryset = Produtos.objects.create(manufacturer=fabricante,
                                           model= 'S9',
                                           color= 'Prata',
                                           carrier_plan_type= 'Pos',
                                           quantity= 20,
                                           price= 10)
        self.queryset_2 = Produtos.objects.create(manufacturer=fabricante,
                                            model= 'primet',
                                            color= 'Prata',
                                            carrier_plan_type= 'Pos',
                                            quantity= 20,
                                            price= 10)
    def test_inventarioview_template_retorna_html_index_inventario_html(self,client):
        entrada = client.get(reverse('inventario'))
        esperando = 'index_inventario.html'
        
        assert entrada.status_code == 200
        assert entrada.templates[0].name == esperando

    def test_inventarioview_model_e_igual_dois(self,client):
        entrada = client.get(reverse('inventario'))
        assert len(entrada.context['inventario']) == 2
    
    def test_inventario_fillterset_class_retornando_queryset_primet(self,client):
        entrada = client.get(reverse('inventario'),{'model':'primet'})
        esperado = self.queryset_2
        
        assert entrada.context['inventario'][0] == esperado