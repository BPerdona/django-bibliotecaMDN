from pyexpat import model
from xmlrpc.client import TRANSPORT_ERROR
from django.db import models
from django.urls import reverse

# Create your models here.

class Genero(models.Model):

    nome = models.CharField(max_length=200, help_text='Entre com um gênero do livro. Ex: Ficção cientifica.')

    def __str__(self):
        return self.nome

class Linguagem(models.Model):

    nome = models.CharField(max_length=200, help_text="Entre com a linguagem do livro. Ex: Inglês, Francês, Japonês")

    def __str__(self):
        return self.nome

class Autor(models.Model):

    primeiro_nome = models.CharField(max_length=100)
    ultimo_nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    data_falecimento = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['ultimo_nome', 'primeiro_nome']

        def __str__(self):
            return f'{self.ultimo_nome}, {self.primeiro_nome}'

class Livro(models.Model):

    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True)
    resumo = models.TextField(max_length=1000, help_text='entre com uma breve descrição do livro')
    isbn = models.CharField('ISBN', max_length=13)
    genero = models.ManyToManyField(Genero, help_text='Selecione um mais gênero para esse livro.')
    linguagem = models.ForeignKey(Linguagem, on_delete=models.SET_NULL, null=True)


    def get_absolute_url(self):
        return reverse('livro-detalhes', args=[str(self.id)])

    def __str__(self):
        return self.titulo

import uuid

class ExemplarLivro(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Identificador único para este exemplar.")
    livro = models.ForeignKey(Livro, on_delete=models.SET_NULL, null=True)
    editora = models.CharField(max_length=200)
    data_devolucao = models.DateField(null=True, blank=True)

    SITUACAO_EXEMPLAR = (
        ('m', 'Manutenção'),
        ('e', 'Emprestado'),
        ('d', 'Disponível'),
        ('r', 'Reservado')
    )

    sitaucao = models.CharField(
        max_length=1,
        choices=SITUACAO_EXEMPLAR,
        blank=True,
        default='m',
        help_text='Situação do exemplar',
    )

    class Meta:
        ordering = ['data_devolucao']

    def __str__(self):
        return f'{self.id} ({self.livro.titulo})'