from apps.importacaocsv.import_csv import ImportFromCsv
from django.core.files.uploadedfile import SimpleUploadedFile
class TestImportFromCsv:
    def setup_method(self):
        arquivo = SimpleUploadedFile('arquivo.csv',b'manufacturer,model,color,carrier_plan_type,quantity,price\n\
                                    Motorola,Moto G5 16GB,Preto,pre,20,1299\n\
                                   Motorola,Moto G5 16GB,Preto,pos,20,599')
        self.arquivo = ImportFromCsv(arquivo)

    def test_arquivo(self):
        entrada = self.arquivo.verificar_tipo_arquivo()
        
        assert entrada == ''
