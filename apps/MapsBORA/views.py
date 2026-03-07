from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Submission
import random, string
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime, timedelta


def get_token(length=10):
   letters = string.ascii_lowercase + string.digits 
   return ''.join(random.choice(letters) for i in range(length))

def submission_list(request):
    queue = Submission.objects.all()
    return render(request, 'MapsBORA/queue.html', {'queue':queue})

def index(request):

    next_tuesdays = []
    today = datetime.now().date()

    days_until_tuesday = (1 - today.weekday()) % 7
    first_tuesday = today + timedelta(days=days_until_tuesday)

    for i in range(10):
        next_tuesdays.append(first_tuesday+timedelta(weeks=i))

    if request.method == 'POST':
        map_name = request.POST.get('map_name')
        mapper_name = request.POST.get('mapper_name')
        map_url = request.POST.get('map_url')
        request_date = request.POST.get('request_date')
        status = 'Pending'

        if Submission.objects.filter(request_date=request_date).exists():
            messages.error(request, "This Tuesday is already occupied")
            return redirect("index")
        if Submission.objects.filter(map_name__icontains=map_name).exists():
            messages.error(request, "This map is in the list to be ridden")
            return redirect("index")

        new_submission = Submission.objects.create(
            map_name = f"{map_name} (by {mapper_name})", 
            map_url = map_url,
            request_date=request_date,
            status=status,
            token=get_token(10)
        )
        messages.success(request, f'Submission successful! Your tracking code is: {new_submission.token}')
        return redirect('index')

    submissions = Submission.objects.all().order_by('request_date')

    return render(request, 'MapsBORA/index.html', {
        'submissions': submissions,
        'next_tuesdays': next_tuesdays
    })

def edit_submission(request, id):
    submission = get_object_or_404(Submission, id=id)
    
    # Generate the Tuesday list for the picker
    next_tuesdays = []
    today = datetime.now().date()
    days_until_tuesday = (1 - today.weekday()) % 7
    first_tuesday = today + timedelta(days=days_until_tuesday)
    for i in range(10):
        next_tuesdays.append(first_tuesday + timedelta(weeks=i))

    if request.method == 'POST':
        word = request.POST.get('token')

        if word == submission.token:
            submission.map_name = request.POST.get('map_name')
            submission.description = request.POST.get('description')
            submission.request_date = request.POST.get('request_date')
            submission.map_url = request.POST.get('map_url')
            submission.save()
            messages.success(request, "Map updated successfully!")
            return redirect('index')
        else:
            messages.error(request, "Invalid token! Access denied.")
            return redirect('index')

    return render(request, 'MapsBORA/edit.html', {
        'submission': submission, # Use singular 'submission' to match your previous edit.html
        'next_tuesdays': next_tuesdays
    })

def delete_with_token(request, id):
    submission = get_object_or_404(Submission, id=id)
    if request.method == 'POST':
        user_token = request.POST.get('token')
        if user_token == submission.token:
            map_name = submission.map_name
            submission.delete()
            messages.warning(request, f"Mission Aborted: '{map_name}' was removed from the queue.")
            return redirect('index')
        else:
            messages.error(request, "Invalid token! You cannot delete this submission.")
            return redirect('index')
    return redirect('index')

@staff_member_required
def approve_submission(request, id):
    submission = get_object_or_404(Submission, id=id)
    submission.status = 'approved'
    submission.save()
    messages.success(request, f"Map '{submission.map_name}' approved!")
    return redirect('index')

@staff_member_required
def delete_submission(request, id):
    submission = get_object_or_404(Submission, id=id)
    map_name = submission.map_name
    submission.delete()
    messages.warning(request, f"Map '{map_name}' was removed from the list.")
    return redirect('index')

@staff_member_required
def recover_token(request, id):
    submission = get_object_or_404(Submission, id=id)
    messages.info(request, f"The token for '{submission.map_name}' is: {submission.token}")
    return redirect('index')