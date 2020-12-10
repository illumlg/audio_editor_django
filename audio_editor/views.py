import datetime
import os
from typing import List, Callable, Tuple

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from audio_editor.audio_operations import convert, chorus, trim, treble, reverse, flanger, tremolo, volume, echo, bass, \
    speed, repeat, fade
from audio_editor.const import INPUT_DIRECTORY, MAX_CONTENT_SIZE, STORAGE_LIMIT
from audio_editor.custom_response import ResponseThen
from audio_editor.forms import AudiofileForm
from audio_editor.models import Request
from audio_editor.utils import handle_file


def index(request):
    return render(request, 'index.html')

@login_required(login_url='/accounts/login/?next=/upload')
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        form = AudiofileForm(request.POST, request.FILES)
        if form.is_valid():
            ops = []
            if form['convert'].data:
                ops.append((convert, [form['format'].data]))
            if form['chorus'].data:
                ops.append((chorus, [int(form['voices'].data)]))
            if form['trim'].data:
                ops.append((trim, [int(form['start_time'].data), int(form['end_time'].data)]))
            if form['treble'].data:
                ops.append((treble, [int(form['gain'].data)]))
            if form['reverse'].data:
                ops.append((reverse, []))
            if form['flanger'].data:
                ops.append((flanger, [form['preset'].data]))
            if form['tremolo'].data:
                ops.append((tremolo, [int(form['tremolo_speed'].data), int(form['depth'].data)]))
            if form['volume'].data:
                ops.append((volume, [int(form['volume_value'].data)]))
            if form['echo'].data:
                ops.append((echo, [float(form['gain_in'].data), float(form['gain_out'].data)]))
            if form['bass'].data:
                ops.append((bass, [float(form['gain_db'].data), float(form['freq'].data), float(form['slope'].data)]))
            if form['speed'].data:
                ops.append((speed, [float(form['speed_value'].data)]))
            if form['repeat'].data:
                ops.append((repeat, [int(form['count'].data)]))
            if form['fade'].data:
                ops.append((fade, [float(form['fade_start'].data), float(form['fade_end'].data)]))
            s = sum([os.path.getsize(INPUT_DIRECTORY + file)  for file in os.listdir(INPUT_DIRECTORY)])
            if s > STORAGE_LIMIT:
                response = HttpResponse('Inner storage is full, try again later')
                response.status_code=507
                return response
            full_path_input, full_path_output = handle_file(request.FILES['audiofile'], ops)
            log = Request(date=datetime.datetime.now(),
                          name=request.method,
                          status='OK',
                          status_code=200,
                          description='success',
                          user=request.user.get_username(),
                          params=str(ops))
            log.save()
            print(len(os.listdir('input files'))-1)
            response = ResponseThen(open(full_path_output, 'rb'), content_type='audio/*', full_path_input=full_path_input, full_path_output=full_path_output, as_attachment=True)
            return response
    else:
        form = AudiofileForm()
    return render(request, 'upload.html', {'form': form})
