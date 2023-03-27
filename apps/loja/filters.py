from django.forms.widgets import TextInput,Select

import django_filters
from apps.loja.models import Produtos,Fabricante

class InvetarioFilter(django_filters.FilterSet):
    manufacturer = django_filters.ModelChoiceFilter(queryset=Fabricante.objects.all(),
                                                    widget=Select(attrs={'class': 'form-control-lg',
                                                                         'placeholder':'Fabricante',
                                                                         'value': 'foo'}),
                                                                         lookup_expr='exact',label='',
                                                                         empty_label='Fabricante'
                                                                         )
    carrier_plan_type = django_filters.CharFilter(lookup_expr='icontains',
                                                  widget=TextInput(attrs={'class': 'form-control-lg',
                                                                          'placeholder':'Plano'}),label='')
    model = django_filters.CharFilter(lookup_expr='icontains',
                                      widget=TextInput(attrs={'class': 'form-control-lg',
                                                              'placeholder':'Modelo'}),label='')

    class Meta:
        model = Produtos
        fields = ['manufacturer','model','carrier_plan_type']