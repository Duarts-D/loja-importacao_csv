from django.shortcuts import render
from django.views import View

# Create your views here.
class InputView(View):
    def get(self,*args):
        return render(self.request,'import_input.html')

