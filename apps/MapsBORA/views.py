from django.shortcuts import render
from django.http import HttpResponse
from .models import Submissao


def lista_submissoes(request):
    queue = Submissao.objects.all()
    return render(request, 'MapsBORA/queue.html', {'queue':queue})

