from django.views.generic.base import TemplateView
from django.shortcuts import render
 
from django.urls import  reverse_lazy
from django.shortcuts import render,  redirect 

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = "core/home.html"
 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'Hillel Argentina'})
 

class SamplePageView(TemplateView):
    template_name = "core/sample.html"


def export_csv(request):
     return redirect(reverse_lazy('pages:pages'))


def enviar_mail(request):
     return redirect(reverse_lazy('pages:pages'))