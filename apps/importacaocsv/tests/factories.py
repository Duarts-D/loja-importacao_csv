import factory
from pytest_factoryboy import register
from apps.loja.models import Fabricante,Produtos


class FabricanteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fabricante

    fabricante = 'Lenovo'

class ProdutoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Produtos

    manufacturer = factory.SubFactory(FabricanteFactory)
    model = 'iPhone'
    color = 'black'
    carrier_plan_type = 'postpaid'
    quantity = 3
    price = 200

