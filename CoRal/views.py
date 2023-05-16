import pandas as pd
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Recording
from django.core.files import File
import settings

import random


def index(request):
    template = loader.get_template('index.html')
    processed_articles = pd.read_csv(Path(settings.MEDIA_ROOT) / "processed_articles.csv")
    transcriptions = processed_articles["text"].tolist()
    transcriptions = [line.rstrip() for line in transcriptions]
    random.shuffle(transcriptions)
    content = {
        "transcriptions": transcriptions[:2000],
    }
    return HttpResponse(template.render(content, request))


def requirements(request):
    template = loader.get_template('requirements.html')
    return HttpResponse(template.render({}, request))


def save_audio(request):
    """Save recorded audio blob sent by user."""
    audio_file = request.FILES.get('recorded_audio')
    transcription = request.POST.get("transcription")
    room_dimensions = request.POST.get("room_dimensions")
    name = request.POST.get("name")
    email = request.POST.get("email")
    address = request.POST.get("address")
    background_noise = request.POST.get("background_noise")
    noise = request.POST.get("noise")
    age = request.POST.get("age")
    dialect = request.POST.get('dialect')
    languages = request.POST.get('languages')
    gender = request.POST.get('gender')
    accent = request.POST.get('accent')
    zipcode_school = request.POST.get('zipcode_school')
    zipcode_birth = request.POST.get('zipcode_birth')
    education = request.POST.get('education')
    occupation = request.POST.get('occupation')
    birth_place = request.POST.get('birth_place')
    experiment_start_time = request.POST.get('experiment_start_time')
    submitted_time = request.POST.get('submitted_time')
    recording = Recording()
    recording.name = name
    recording.email = email
    recording.room_dimensions = room_dimensions
    recording.address = address
    recording.background_noise = background_noise
    recording.noise = noise
    recording.recorded_file = audio_file
    recording.transcription = transcription
    recording.age = age
    recording.languages = languages
    recording.dialect = dialect
    recording.gender = gender
    recording.accent = accent
    recording.zipcode_school = zipcode_school
    recording.zipcode_birth = zipcode_birth
    recording.education = education
    recording.occupation = occupation
    recording.birth_place = birth_place
    recording.experiment_start_time = experiment_start_time
    recording.submitted_time = submitted_time
    recording.save()

    return JsonResponse({
        'success': True,
    })
