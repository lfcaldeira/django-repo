from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Submission


def submission_list(request):
    queue = Submission.objects.all()
    return render(request, 'MapsBORA/queue.html', {'queue':queue})

def index(request):

    if request.method == 'POST':
        map_name = request.POST.get('map_name')
        mapper_name = request.POST.get('mapper_name')
        submitted_date = request.POST.get('submitted_date')
        status = 'Pending'

        Submission.objects.create(
            map_name = f"{map_name} (by {mapper_name})", 
            submitted_date=submitted_date,
            status=status
        )
        return redirect('index')

    submissions = Submission.objects.all().order_by('submitted_date')

    return render(request, 'MapsBORA/index.html', {
        'submissions': submissions
    })