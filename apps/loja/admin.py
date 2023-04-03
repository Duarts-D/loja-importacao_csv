from django.contrib import admin
from apps.loja.models import Fabricante,Produtos

class ProdutosInline(admin.TabularInline):
    model = Produtos
    extra = 0
class FabricanteAdmin(admin.ModelAdmin):
    inlines = [
        ProdutosInline
    ]
    def num_produtos(self,obj):
        return obj.produtos_set.count()
    
    num_produtos.short_description = 'Quantidade'

    list_display = ('fabricante','num_produtos')
    list_per_page = 10
    search_fields = ('fabricante',)
    
admin.site.register(Fabricante,FabricanteAdmin)


class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('model','manufacturer','carrier_plan_type','quantity','price_br',)
    list_filter = ('manufacturer','carrier_plan_type')
    search_fields = ('model','manufacturer__fabricante')
    ordering = ('-id',)
    
admin.site.register(Produtos,ProdutosAdmin)
