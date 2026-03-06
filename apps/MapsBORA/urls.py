from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista_submissoes, name="lista_submissoes"),
]
