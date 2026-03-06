from django.shortcuts import render
from django.http import HttpResponse
from .models import Submission


def submission_list(request):
    queue = Submission.objects.all()
    return render(request, 'MapsBORA/queue.html', {'queue':queue})

def index(request):
    submissions = Submission.objects.all().order_by('submitted_date')

    return render(request, 'MapsBORA/index.html', {
        'submissions': submissions
    })