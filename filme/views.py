from django.shortcuts import render, redirect,reverse
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormHomepage


# Create your views here.

class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        # se usuario estiver autenticado redirecionar para homefilmes
        if request.user.is_authenticated:
           return redirect('filme:homefilmes')
        else:
            return super().get(self, request, *args, **kwargs) #redireciona usuario para homepage

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuario = Usuario.objects.filter(email=email)
        if usuario:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')

class Homefilmes(LoginRequiredMixin,ListView):
    template_name = "homefilmes.html"
    model = Filme
    #object_list - lista de itens do modelo

class Detalhefilme(LoginRequiredMixin,DetailView):
    template_name = "detalhefilme.html"
    model = Filme
    #object - um item do modelo

    def get(self, request, *args, **kwargs):
        #descobrir qual filme e a pagina
        filme = self.get_object()
        #contabilizar visualizacoes
        filme.visualizacoes +=1
        #salvar no banco de dados
        filme.save()
        usuario = request.user
        usuario.filme_vistos.add(filme)

        return super().get(request,*args,**kwargs) #redireciona para a pagina final

    def get_context_data(self, **kwargs):
        #filtrar na minha tabela do bd o filme com a categoria igual a do filme da pagina
        context = super(Detalhefilme,self).get_context_data(**kwargs)
        filmes_relacionados = Filme.objects.filter(categoria = self.get_object().categoria)[0:3]
        context['filmes_relacionados'] = filmes_relacionados

        return context

class Pesquisafilme(LoginRequiredMixin,ListView):
    template_name = "pesquisa.html"
    model = Filme

    #definindo o object list de acordo com o termo de pesquisa
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')


