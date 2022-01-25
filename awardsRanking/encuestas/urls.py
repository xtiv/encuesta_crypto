from django.urls import path
from . import views

app_name="encuestas"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detalle_pregunta'),
    path('<int:pk>/results', views.ResultView.as_view(), name='resultados_pregunta'),
    path('<int:pregunta_id>/vote', views.votar_pregunta, name='voto')
]