from django.contrib import admin

from anuncio.models import Anuncio

# Register your models here.
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ['id', 'data_criacao', 'veiculo', 'valor', 'usuario']
    search_fields =  ['titulo', 'descricao']

admin.site.register(Anuncio, AnuncioAdmin)
