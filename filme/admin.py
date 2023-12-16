from django.contrib import admin
from .models import Filme, Episodio, Usuario
from django.contrib.auth.admin import UserAdmin

#mostrando o campo extra criado de filmes_vistos no admin do site
campos = list(UserAdmin.fieldsets)
campos.append(
    ("Historico", {'fields': ('filme_vistos',)})
)
UserAdmin.fieldsets = tuple(campos)

admin.site.register(Filme)
admin.site.register(Episodio)
admin.site.register(Usuario, UserAdmin)

# Register your models here.
