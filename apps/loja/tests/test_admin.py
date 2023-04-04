from django.contrib.admin.sites import AdminSite
from django.contrib import admin
from apps.loja.admin import FabricanteAdmin
from unittest.mock import Mock

from apps.loja.models import Fabricante,Produtos
import pytest


@pytest.mark.django_db
class TestLojaAdmin:
    def setup_method(self):
        self.site = AdminSite()

    def test_num_produtos_deve_retornar_1(self,fabricante_factory,produto_factory):
        produto = produto_factory.create()
        
        esperado = FabricanteAdmin(Fabricante,self.site)
        resultado = esperado.num_produtos(produto.manufacturer)
        
        
        assert  resultado == 1