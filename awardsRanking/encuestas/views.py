from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect   
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Models
from .models import Opciones, Pregunta


# def index(request):
#     latest_question_list = Pregunta.objects.all()
#     return render(request, "encuestas/index.html", {
#         'latest_question_list': latest_question_list
#     })


# def detalle_pregunta(request, pregunta_id):
#     pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
#     return render(request, "encuestas/detalle.html", {
#         'pregunta': pregunta
#     })


# def resultados_pregunta(request, pregunta_id):
#     pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
#     return render(request, "encuestas/resultados.html", {
#         "pregunta" : pregunta
#     })


class IndexView(generic.ListView):
    template_name= "encuestas/index.html"
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Pregunta.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Pregunta
    template_name = "encuestas/detalle.html"
    
    def get_queryset(self):
        """
        Exlclude question that aren't published yet
        """
        return Pregunta.objects.filter(pub_date__lte=timezone.now())
    
    
class ResultView(generic.DetailView):
    model = Pregunta
    template_name = "encuestas/resultados.html"
    
    def get_queryset(self):
        return Pregunta.objects.filter(pub_date__lte=timezone.now())
    


def votar_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        opcion_seleccionada = pregunta.opciones_set.get(pk=request.POST["opcion"])
    except (KeyError, Opciones.DoesNotExist):
        return render(request, "encuestas/detalle.html", {
            "pregunta" : pregunta,
            "error_message": "No elegiste una respuesta"
        })
    else:
        opcion_seleccionada.votos +=1
        opcion_seleccionada.save()
        return HttpResponseRedirect(reverse("encuestas:resultados_pregunta", args=(pregunta.id,)))
    
        
   