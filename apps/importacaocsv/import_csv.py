import pandas as pd
from numpy import nan
from apps.loja.models import Fabricante,Produtos

class ImportFromCsv:
    def __init__(self,arquivo):
        self.arquivos = arquivo
        self.msg = []
        
    def verificar_tipo_arquivo(self):
        if self.arquivos.name[-4:] == '.csv':
            return self.verificar_colunas_x_arquivos_exiteste()
        return self.msg.append('Arquivo invalido favor inserir arquivo tipo csv')

    
    def verificar_colunas_x_arquivos_exiteste(self):
        try:
            self.tabela = pd.read_csv(self.arquivos,usecols=['manufacturer','model','color','carrier_plan_type','quantity','price'])
            return self.validando_dados_necessario()
        
        except ValueError :
            nome_da_coluna = ['manufacturer','model','color','carrier_plan_type','quantity','price']
            return f'Impossivel continuar a verificaçao pois alguma das colunas pricipais\
                estao faltando favor verifica as colunas - tem que haver essa colunas {nome_da_coluna}'
    


    def validando_dados_necessario(self):
        """ Faz um validaçao em todos os campo da colunas corresponde,
            Necessario para nao, utilizar dados incompletos,
            ou invalidos de acordo com a logica de salvamento."""
        arquivo = self.tabela
        arquivo = arquivo.replace(' ', nan )# corrigir uma problema espacionamento que recolhece como str.
        
        arquivo['price'] = pd.to_numeric(arquivo['price'],errors='coerce')
        arquivo['quantity'] = pd.to_numeric(arquivo['quantity'],errors='coerce')
        arquivo['quantity'] = arquivo['quantity'].astype('Int32')
       
        erros_encontrado = arquivo[arquivo.isna().any(axis=1)]
        
        for linha,coluna in erros_encontrado.iterrows():
            self.msg.append(f'Linha {linha+2} = \
                            {str(coluna.values).replace("nan","ERROR").replace("<NA>","ERROR")}')
        if len(self.msg) >= 1 :
            self.msg.insert(0,'Ah erros nos arquivos ,verifique o numero da linha \
                e o local que esta o "ERROR"')
    
    def erros(self):
        """Faz um verificao se a erros adicionado na lista se ouver,
            retornando a lista"""
        if len(self.msg) == 0:
            self.verificar_tipo_arquivo()
        if len(self.msg) >= 1:
            return self.msg
        return False
    
    def salvando_dado_dados(self): 
        produtos = []
        
        for linha , coluna in self.tabela.iterrows():
            produtos.append(Produtos(
            manufacturer =  Fabricante.objects.get(fabricante=coluna['manufacturer'])\
                if Fabricante.objects.filter(fabricante=coluna['manufacturer'])\
                else Fabricante.objects.create(fabricante=coluna['manufacturer']),
            model = coluna['model'],
            color = coluna['color'],
            carrier_plan_type = coluna['carrier_plan_type'],
            quantity = coluna['quantity'],
            price = coluna['price'])),
        
        return produtos
    
    def save(self,model):
        self.verificar_tipo_arquivo()
        if len(self.msg) == 0:
            salvar = self.salvando_dado_dados()
            return model.objects.bulk_create(salvar)
        return