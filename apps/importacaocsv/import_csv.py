import pandas as pd
from numpy import nan
from apps.loja.models import Fabricante,Produtos

class ImportFromCsv:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.error = []
        self.dataframe = None

    def erros(self):
        """Faz um verificao se a erros adicionado na lista se houver,
            retornando a lista"""
        if not self.validar_dados_necessario():
            return self.error
        return False
    
    def pega_dataframe(self):
        if self.validar_arquivo_extensao():
            try:
                return pd.read_csv(self.arquivo, usecols=['manufacturer','model','color','carrier_plan_type','quantity','price'])
            except ValueError:
                colunas_obrigatorio = ['manufacturer','model','color','carrier_plan_type','quantity','price']
                return (f'Impossivel continuar a verificaçao pois alguma das colunas pricipais \
                    estao faltando favor verifica as colunas - tem que haver essa colunas {colunas_obrigatorio}')
        else:
            return 'Arquivo invalido'

    def validar_arquivo_extensao(self):
        e_valido = False
        if self.arquivo.name.endswith('.csv'):
            e_valido = True
        return e_valido
    
    def validar_dados_necessario(self):
        """ Faz um validaçao em todos os campo da colunas corresponde,
            Necessario para nao, utilizar dados incompletos,
            ou invalidos de acordo com a logica de salvamento."""

        dataframe = self.pega_dataframe()

        if isinstance(dataframe, pd.DataFrame):
            arquivo = dataframe
            arquivo = arquivo.replace(' ', nan)# corrigir uma problema espacionamento que recolhece como str.
            
            arquivo['price'] = pd.to_numeric(arquivo['price'],errors='coerce')
            arquivo['quantity'] = pd.to_numeric(arquivo['quantity'],errors='coerce')
            arquivo['quantity'] = arquivo['quantity'].astype('Int32')

            erros_encontrado = arquivo[arquivo.isna().any(axis=1)]
            for linha, dado in erros_encontrado.iterrows():
                self.error.append(f'''
                    Linha {linha+2}
                    {str(dado.values).replace("nan","ERRO").replace("<NA>","ERRO")}
                    '''
                )
            if len(self.error) > 0:
                self.error.insert(0,'Ah erros nos arquivo ,verifique o numero da linha \
                    e o local que esta o "ERRO"')
                return False
            
            self.dataframe = dataframe
            return True
        
        self.error.append(dataframe)
        return False

    
    def save(self):
        if not self.dataframe is None:
            """Salva os dados no banco de dados ."""
            produtos_criar = []
            produto_atualizar = []
            for index , dado in self.dataframe.iterrows():
                manufacturer = dado['manufacturer'].lower().capitalize()
                fabricantes = Fabricante.objects.get_or_create(fabricante=manufacturer)
                produto_salvo = Produtos.objects.filter(manufacturer=fabricantes[0],
                                                    model= dado['model'],
                                                    color= dado['color'],
                                                    carrier_plan_type= dado['carrier_plan_type']).first()
                if produto_salvo:
                    produto_salvo.quantity = produto_salvo.quantity + dado['quantity']
                    produto_salvo.price = dado['price']
                    produto_atualizar.append(produto_salvo)
                else:
                    produtos_criar.append(Produtos(
                    manufacturer = fabricantes[0],
                    model = dado['model'],
                    color = dado['color'],
                    carrier_plan_type = dado['carrier_plan_type'],
                    quantity = dado['quantity'],
                    price = dado['price'])),
            
            Produtos.objects.bulk_update(produto_atualizar,fields=['quantity','price'],batch_size=100)
            Produtos.objects.bulk_create(produtos_criar, batch_size=100)
            
            return True
        return False