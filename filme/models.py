from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

LISTA_CATEGORIAS = (
    ("ACAO", "Ação"),
    ("ROMANCE", "Romance"),
    ("TERROR", "Terror"),
    ("DOCUMENTARIO", "Documentário"),

)

# criar o filme
class Filme(models.Model):
    titulo = models.CharField(max_length=100, default="INSIRA O TITULO")
    thumb = models.ImageField(upload_to='thumb_filmes',null=True)
    descricao = models.TextField(max_length=10000, null=True)
    categoria = models.CharField(max_length=20,null=True, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField(default=0)
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

# criar os episodios
class Episodio(models.Model):
    filme = models.ForeignKey("Filme", related_name="episodios",on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    video = models.URLField()

    def __str__(self):
        return self.filme.titulo + " - " + self.titulo

#cria usuario personalizado
class Usuario(AbstractUser):
    filme_vistos = models.ManyToManyField("Filme")


