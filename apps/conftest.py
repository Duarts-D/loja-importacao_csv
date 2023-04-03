from pytest_factoryboy import register
from apps.importacaocsv.tests.factories import FabricanteFactory,ProdutoFactory

register(FabricanteFactory)
register(ProdutoFactory)