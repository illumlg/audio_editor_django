from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase, Client
import sox

from audio_editor.forms import AudiofileForm
from audio_editor_django.settings import BASE_DIR


class AudioEditorTests(TestCase):
    test_file = BASE_DIR / 'testFile.wav'

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='test')
        self.tfm = sox.Transformer()

    def tearDown(self) -> None:
        pass

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_upload_unauth(self):
        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 302)

    def test_upload_auth(self):
        self.client.login(username='user', password='ytrewq4444')
        response = self.client.get('/upload', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_edit(self):
        file = open(self.test_file, 'rb')
        self.client.force_login(self.user)
        form = AudiofileForm(files={'audiofile': File(file)}, data={
                                   'convert': True, 'format': '.snd', 'chorus': 'true',
                                   'voices': 3, 'trim': True,
                                   'start_time': 1, 'end_time': 10, 'treble': True, 'gain': 15,
                                   'reverse': True, 'flanger': True, 'preset': 'medium', 'tremolo': True,
                                   'tremolo_speed': 7, 'depth': 50, 'volume': True, 'volume_value': 5,
                                   'echo': True, 'gain_in': 0.5, 'gain_out': 0.5,
                                   'bass': True, 'gain_db': 15, 'freq': 150, 'slope': 0.5,
                                   'speed': True, 'speed_value': 0.9, 'repeat': True, 'count': 2,
                                   'fade': True, 'fade_start': 5, 'fade_end': 5})
        response = self.client.post('/upload', data={'audiofile': File(file),
                                    'convert': True, 'format': '.snd', 'chorus': 'true',
                                   'voices': 3, 'trim': True,
                                   'start_time': 1, 'end_time': 10, 'treble': True, 'gain': 15,
                                   'reverse': True, 'flanger': True, 'preset': 'medium', 'tremolo': True,
                                   'tremolo_speed': 7, 'depth': 50, 'volume': True, 'volume_value': 5,
                                   'echo': True, 'gain_in': 0.5, 'gain_out': 0.5,
                                   'bass': True, 'gain_db': 15, 'freq': 150, 'slope': 0.5,
                                   'speed': True, 'speed_value': 0.9, 'repeat': True, 'count': 2,
                                   'fade': True, 'fade_start': 5, 'fade_end': 5})
        file.close()
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('attachment; filename' in response.get('Content-Disposition'))
