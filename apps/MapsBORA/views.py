from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Submission
import random, string
from django.contrib import messages

def get_token(length=10):
   letters = string.ascii_lowercase + string.digits # Adicionei números para ser mais seguro
   return ''.join(random.choice(letters) for i in range(length))

def submission_list(request):
    queue = Submission.objects.all()
    return render(request, 'MapsBORA/queue.html', {'queue':queue})

def index(request):

    if request.method == 'POST':
        map_name = request.POST.get('map_name')
        mapper_name = request.POST.get('mapper_name')
        submitted_date = request.POST.get('submitted_date')
        status = 'Pending'

        new_submission = Submission.objects.create(
            map_name = f"{map_name} (by {mapper_name})", 
            submitted_date=submitted_date,
            status=status,
            randomword=get_token(10)
        )
        messages.success(request, f'Submission successful! Your tracking code is: {new_submission.randomword}')
        return redirect('index')

    submissions = Submission.objects.all().order_by('submitted_date')

    return render(request, 'MapsBORA/index.html', {
        'submissions': submissions
    })

def edit_submission(request, id):
    submission = get_object_or_404(Submission, id=id)

    if request.method == 'POST':
        word = request.POST.get('randomword')
        messages.success(request,"this is the token"+word)

        if word == submission.randomword:
            submission.mapper_name = request.POST.get('mapper_name')
            submission.map_name = request.POST.get('map_name')
            submission.description = request.POST.get('description')
            submission.save()
            messages.success(request, "Map updated successfully")
            return redirect('index')
        else:
            messages.error(request, "Invalid token! You cannot edit this map.")
            return redirect('index')

    return render(request, 'MapsBORA/edit.html',{'submissions': submission})