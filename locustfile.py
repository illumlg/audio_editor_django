from django.core.files import File
from locust import HttpUser, task, constant

from audio_editor_django.settings import BASE_DIR


class User(HttpUser):
    host = 'https://audio-editor-django.herokuapp.com'
    #host = 'http://127.0.0.1:8000'
    wait_time = constant(0)

    @task
    def convert(self):
        with open(BASE_DIR / 'testFile.wav', 'rb') as file:
            self.client.post('/upload', files={'audiofile': File(file)}, data={
                'convert': True, 'format': '.snd', 'chorus': 'true',
                'voices': 3, 'trim': True,
                'start_time': 1, 'end_time': 10, 'treble': True, 'gain': 15,
                'reverse': True, 'flanger': True, 'preset': 'medium', 'tremolo': True,
                'tremolo_speed': 7, 'depth': 50, 'volume': True, 'volume_value': 5,
                'echo': True, 'gain_in': 0.5, 'gain_out': 0.5,
                'bass': True, 'gain_db': 15, 'freq': 150, 'slope': 0.5,
                'speed': True, 'speed_value': 0.9, 'repeat': True, 'count': 2,
                'fade': True, 'fade_start': 5, 'fade_end': 5})