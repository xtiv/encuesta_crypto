from django.contrib import admin
from encuestas.models import Pregunta, Opciones

class OpcionesInline(admin.StackedInline):
    model = Opciones
    extra = 2
    
class PreguntaAdmin(admin.ModelAdmin):
    fields = ["pub_date", "pregunta_text"]
    inlines = [OpcionesInline]
    list_display = ("pregunta_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["pregunta_text"]

admin.site.register(Pregunta, PreguntaAdmin)
