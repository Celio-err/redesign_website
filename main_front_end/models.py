from django.db import models



class MandatoView(models.Model):
    id_identificacao = models.UUIDField(primary_key=True)
    nome_pessoa = models.CharField(max_length=255)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    funcao_mandato = models.CharField(max_length=100, blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True, null=True)
    tipo_mandato = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mandato_cfp'

    def __str__(self):
        return self.nome_pessoa
    
class NoticiasView(models.Model):
    id_noticia = models.UUIDField(primary_key=True)
    noticia = models.TextField(blank=True, null=True)
    data_publicacao = models.DateField(blank=True, null=True)
    inserido_por = models.CharField(max_length=50, blank=True, null=True)
    inserido_em = models.CharField(max_length=40, blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    id_tipo_noticia_id = models.UUIDField(blank=True, null=True)
    nome_noticia = models.CharField(max_length=255)
    tipo_noticia = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"website_foun"."noticias_pulico"'

    def __str__(self):
        return self.nome_noticia