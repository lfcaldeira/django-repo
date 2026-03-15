from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Submission
import random, string
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.base import ContentFile
import xml.etree.ElementTree as ET
from django.core.exceptions import ValidationError
from django.urls import reverse

def validate_gpx_file(request, gpx_file):
    if not gpx_file:
        return None
    if gpx_file.size > 5 * 1024 * 1024:
        return False
    
    try:
        content = gpx_file.read(1024)
        gpx_file.seek(0)
        if b'<gpx' not in content.lower():
            messages.error(request, "GPX is not valid")
            return False
        return gpx_file
    except:
        messages.error(request, "Error reading GPX file")
        return False


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
        gpx_f = request.FILES.get('gpx_file')
        request_date = request.POST.get('request_date')
        status = 'pending'

        existing_maps = Submission.objects.filter(map_url__icontains=map_url)

        if not map_url and not gpx_f:
            messages.error(request, "You must fill out MapURL or upload a GPX File")
            return redirect("index")
        
        gpx_to_save = validate_gpx_file(request, gpx_f)

        if gpx_to_save is False:
            return redirect("index")

        if existing_maps.filter(status__in=['pending', 'approved']).exists():
            messages.error(request, "This map is already in the queue to be ridden")
            return redirect("index")
        if Submission.objects.filter(request_date=request_date).exists():
            messages.error(request, "This Tuesday is already occupied")
            return redirect("index")
        if Submission.objects.filter(map_name__icontains=map_name).exists():
            messages.error(request, "Map name already exists")
            return redirect("index")
        
        new_submission = Submission.objects.create(
            map_name = map_name,
            mapper_name = mapper_name, 
            map_url = map_url,
            gpx_file = gpx_to_save,
            request_date=request_date,
            status=status,
            token=get_token(10)
        )

        token_url = reverse('edit_submission_with_token', kwargs={'id': new_submission.id, 'token':new_submission.token})
        link_with_token = request.build_absolute_uri(token_url)
        #link_with_token = f"https://lisboramaps.cc/edit/{new_submission.id}/{new_submission.token}"

        messages.success(request, f'Submission successful! save this link: {link_with_token} to edit the map request later')
        return redirect('index')

    submissions = Submission.objects.filter(request_date__gte=today, status__in=['approved', 'pending']).order_by('request_date')

    return render(request, 'MapsBORA/index.html', {
        'submissions': submissions,
        'next_tuesdays': next_tuesdays
    })

def edit_submission(request, id, token=None):
    submission = get_object_or_404(Submission, id=id)
    
    if token:
        if submission.token == token:
            request.session[f'auth_{id}'] = token
            return redirect('edit_submission', id=id)
        else:
            messages.error(request, "Invalid access token")
            return redirect('index')
        
    session_token = request.session.get(f'auth_{id}')
    if session_token != submission.token:
        messages.error(request, "Access denied. Please use your original edit link")
        return redirect("index")

    # Generate the Tuesday list for the picker
    next_tuesdays = []
    today = datetime.now().date()
    days_until_tuesday = (1 - today.weekday()) % 7
    first_tuesday = today + timedelta(days=days_until_tuesday)
    for i in range(10):
        next_tuesdays.append(first_tuesday + timedelta(weeks=i))

    if request.method == 'POST':
        word = request.POST.get('token')

        new_map_url = request.POST.get('map_url')
        new_date = request.POST.get('request_date')
        delete_gpx_flag = request.POST.get('delete_gpx') == 'true'
        if Submission.objects.filter(request_date=new_date).exclude(id=id).exists():
            messages.error(request, "That Tuesday is already taken by another map.")
            return render(request, 'MapsBORA/edit.html', {'submission': submission, 'next_tuesdays': next_tuesdays})
        if Submission.objects.filter(map_url=new_map_url, status__in=['pending', 'approved']).exclude(id=id).exists():
            messages.error(request, "This map URL is already in the queue!")
            return render(request, 'MapsBORA/edit.html', {'submission': submission, 'next_tuesdays': next_tuesdays})
        if word == submission.token:
            submission.map_name = request.POST.get('map_name')
            submission.description = request.POST.get('description')
            submission.request_date = new_date
            submission.map_url = new_map_url
            gpx_file = request.FILES.get('gpx_file')
            gpx_to_save = validate_gpx_file(request, gpx_file)

            if gpx_to_save is False:
                return render(request, 'MapsBORA/edit.html', {'submission': submission, 'next_tuesdays': next_tuesdays})
            
            if gpx_to_save: # if returned None
                if submission.gpx_file:
                    submission.gpx_file.delete(save=False)
                submission.gpx_file = gpx_to_save
                submission.map_url = ""
                messages.info(request, "GPX uploaded. Map URL cleared for priority.")
            
            elif delete_gpx_flag: #user clicked to delete GPX file
                if submission.gpx_file:
                    submission.gpx_file.delete(save=False)
                submission.gpx_file = None
                submission.map_url = new_map_url
                messages.info(request, "GPX File removed. Map URL updated")
            else:
                if not submission.gpx_file:
                    submission.map_url = new_map_url

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