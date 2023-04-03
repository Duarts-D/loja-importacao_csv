from django.db import models

# Create your models here.
class Fabricante(models.Model):
    fabricante = models.CharField(max_length=100)
    def __str__(self):
        return self.fabricante
    
class Produtos(models.Model):
    manufacturer = models.ForeignKey(Fabricante,on_delete=models.DO_NOTHING)
    model = models.CharField(max_length=255,)
    color = models.CharField(max_length=100,)
    carrier_plan_type = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.FloatField(verbose_name='Preço')
    
    @property
    def price_br(self):
        price = self.price
        price = f"R$ {price:_.2f}".replace('.',',').replace('_','.')
        return price

    def __str__(self):
        return self.model
    