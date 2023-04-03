from pytest import mark

@mark.django_db
class TestProdutos:
    def test_price_br_200_retorna_valor_real_200_virgula_00(self,produto_factory):
        
        entrada = produto_factory.create()
        
        assert entrada.price_br == 'R$ 200,00'

