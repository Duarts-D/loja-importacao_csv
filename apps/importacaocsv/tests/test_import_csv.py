from unittest.mock import patch, MagicMock,Mock
import pytest
from apps.importacaocsv.import_csv import ImportFromCsv
from apps.loja.models import Produtos,Fabricante
import pandas as pd

@pytest.fixture
def mock_dados():
    mock_data = {
        'manufacturer': ['Lenovo', 'Samsung'],
        'model': ['iPhone', 'Galaxy'],
        'color': ['black', 'white'],
        'carrier_plan_type': ['postpaid', 'prepaid'],
        'quantity': [1, 2],
        'price': [1000.0, 500.0]
    }
    return mock_data

@pytest.fixture
def columns_csv():
    columns=['manufacturer','model','color','carrier_plan_type','quantity','price']
    return columns


@pytest.mark.django_db
class TestImportFromCsv:
    def setup_method(self):
        mock_arquivo = MagicMock()
        mock_arquivo.name = 'valid.csv'
        self.mock_arquivo = ImportFromCsv(arquivo=mock_arquivo)

    def test_erros_retonar_lista(self):
        mock_funcao = self.mock_arquivo
        mock_funcao.validar_dados_necessario = Mock(return_value=False)
        
        resultado = self.mock_arquivo.erros()
        
        assert type(resultado) == list
        assert mock_funcao.validar_dados_necessario.called
    
    def test_erros_retornar_false(self):
        mock_funcao = self.mock_arquivo
        mock_funcao.validar_dados_necessario = Mock(return_value=True)
        
        resultado = self.mock_arquivo.erros()
        
        assert resultado == False
        assert mock_funcao.validar_dados_necessario.called
    
    @patch('pandas.read_csv')
    def test_pega_dataframe_valido_retorna_pands_dataframe(self,read_csv_mock,columns_csv):
        read_csv_mock.return_value = pd.DataFrame([['apple', 's9', 'azul', 'pos', '450', '55.0']], columns=columns_csv)

        mock_funcao = self.mock_arquivo
        mock_funcao.validar_arquivo_extensao = Mock(return_value=True)
        
        resultado = self.mock_arquivo.pega_dataframe()

        assert isinstance(resultado,pd.DataFrame)
        assert mock_funcao.validar_arquivo_extensao.called
    
    def test_pega_dataframe_estensao_invalido_retornar_msg_arquivo_invalido(self):
        mock_funcao = self.mock_arquivo
        mock_funcao.validar_arquivo_extensao = Mock(return_value=False)
        
        resultado = self.mock_arquivo.pega_dataframe()

        assert resultado == 'Arquivo invalido'
        assert mock_funcao.validar_arquivo_extensao.called
    
    @patch('pandas.read_csv')
    def test_pega_dataframe_estensao_valido_com_colunas_faltando_retornando_str(self,read_csv_mock):
            read_csv_mock.side_effect = ValueError()
            mock_funcao = self.mock_arquivo
            mock_funcao.validar_arquivo_extensao = Mock(return_value=True)
            
            resultado = self.mock_arquivo.pega_dataframe()  

            assert isinstance(resultado, str)
            assert mock_funcao.validar_arquivo_extensao.called
    
    def test_validar_arquivo_extensao_valido_retornar_true(self):
        resultado = self.mock_arquivo.validar_arquivo_extensao()
        assert resultado == True
    
    def test_validar_arquivo_extensao_invalido_retornar_false(self):
        mock_arquivo = MagicMock()
        mock_arquivo.name = 'valid.txt'
        
        entrada = ImportFromCsv(mock_arquivo)
        resultado = entrada.validar_arquivo_extensao()     
        
        assert resultado == False

    @pytest.mark.parametrize('dados',[
            ['apple', 's9', 'azul', 'pos', '450', '55.0']
    ])
    def test_validar_dados_necessario_arquivo_tipo_dataframe_valido_retornar_true_e_adicionando_dataframe(self,dados,columns_csv):
        mock_funcao = self.mock_arquivo
        mock_funcao.pega_dataframe = Mock(return_value=(pd.DataFrame([dados], columns=columns_csv)))
        
        resultado = self.mock_arquivo.validar_dados_necessario()

        assert resultado == True
        assert isinstance(self.mock_arquivo.dataframe,pd.DataFrame)
        assert mock_funcao.pega_dataframe.called

    def test_validar_dados_necessario_arquivo_invalido_retornar_false_e_adicionando_msg_error(self):
        mock_funcao = self.mock_arquivo
        mock_funcao.pega_dataframe = Mock(return_value=False)
        
        resultado = self.mock_arquivo.validar_dados_necessario()

        assert resultado == False
        assert len(self.mock_arquivo.error) == 1 
        assert mock_funcao.pega_dataframe.called

    @pytest.mark.parametrize('dados',[
        ['apple', 's9', 'azul', 'pos', 'a450', '55.0']])
    def test_validar_dados_necessario_contem_erros_retornando_false(self,dados,columns_csv):
        mock_funcao = self.mock_arquivo
        mock_funcao.pega_dataframe = Mock(return_value=pd.DataFrame([dados],columns=columns_csv))

        resultado = self.mock_arquivo.validar_dados_necessario()

        assert resultado == False
        assert len(self.mock_arquivo.error) == 2

    @pytest.mark.parametrize('dados',[
        ['apple', 's9', 'azul', 'pos', 'a450', '55.0']])
    def test_save_dataframe_nao_e_none_retornar_true(self,dados,columns_csv):
        dataframe = pd.DataFrame([dados],columns=columns_csv)
        mock_parametro = self.mock_arquivo
        mock_parametro.dataframe = MagicMock(return_value=dataframe)
        
        resultado = self.mock_arquivo.save()

        assert resultado == True
    
    def test_save_dataframe_e_none_retornar_false(self):
        resultado = self.mock_arquivo.save()

        assert resultado == False

    def test_save_fabricante_get_or_create_retorna_2_objetos_criado_e_com_a_dado_ja_criado_e_outra_com_samsung(self,mock_dados,fabricante_factory):
        fabricante = fabricante_factory.create()
        mock_parametro = self.mock_arquivo
        mock_parametro.dataframe = pd.DataFrame(data=mock_dados)

        self.mock_arquivo.save()

        assert len(Fabricante.objects.all()) == 2 
        assert Fabricante.objects.get(id=1) == fabricante
        assert Fabricante.objects.get(id=2).fabricante == 'Samsung'

    def test_save_produtos_filter_encontrado_retornando_so_2_banco_de_dados_e_alterando_price_e_quantidade(self,mock_dados,produto_factory):
        produto = produto_factory.create()

        mock_parametro = self.mock_arquivo
        mock_parametro.dataframe = pd.DataFrame(data=mock_dados)
        self.mock_arquivo.save()
        
        entrada = Produtos.objects.get(id=1)
        
        assert len(Produtos.objects.all()) == 2
        assert entrada == produto
        assert entrada.price == 1000
        assert entrada.quantity == 4
  