from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import filesizeformat

from audio_editor.choices import FORMAT_CHOICES, FLANGER_CHOICES, CHORUS_CHOICES
from audio_editor.const import MAX_CONTENT_SIZE


class AudiofileForm(forms.Form):
    audiofile = forms.FileField(label='Select a file', help_text='max 20 mb', allow_empty_file=False)
    convert = forms.BooleanField(label='convert', required=False)
    format = forms.ChoiceField(label='format', required=False, choices=FORMAT_CHOICES)
    chorus = forms.BooleanField(label='chorus', required=False)
    voices = forms.ChoiceField(label='voices', required=False, choices=CHORUS_CHOICES)
    trim = forms.BooleanField(label='trim', required=False)
    start_time = forms.IntegerField(label='start time', required=False)
    end_time = forms.IntegerField(label='end time', required=False)
    treble = forms.BooleanField(label='treble', required=False)
    gain = forms.IntegerField(label='gain(-20 to 20)', required=False, min_value=-20, max_value=20)
    reverse = forms.BooleanField(label='reverse', required=False)
    flanger = forms.BooleanField(label='flanger', required=False)
    preset = forms.ChoiceField(label='preset', required=False, choices=FLANGER_CHOICES)
    tremolo = forms.BooleanField(label='tremolo', required=False)
    tremolo_speed = forms.FloatField(label='speed(-1 to 20)', required=False, min_value=1.0, max_value=20.0)
    depth = forms.FloatField(label='depth(10 to 100)', required=False, min_value=10.0, max_value=100.0)
    volume = forms.BooleanField(label='volume', required=False)
    volume_value = forms.IntegerField(label='value(-50 to 15)', required=False, min_value=-50, max_value=15)
    echo = forms.BooleanField(label='echo', required=False)
    gain_in = forms.FloatField(label='gain_in(0.1 to 1)', required=False, min_value=0.1, max_value=1.0)
    gain_out = forms.FloatField(label='gain_out(0.1 to 1)', required=False, min_value=0.1, max_value=1.0)
    bass = forms.BooleanField(label='bass', required=False)
    gain_db = forms.FloatField(label='gain_db(-20 to 20)', required=False, min_value=-20, max_value=20)
    freq = forms.FloatField(label='frequency(10 to 200)', required=False, min_value=10, max_value=200)
    slope = forms.FloatField(label='slope(0.3 to 1)', required=False, min_value=0.3, max_value=1.0)
    speed = forms.BooleanField(label='speed', required=False)
    speed_value = forms.FloatField(label='value(0.1 to 10)', required=False, min_value=0.1, max_value=10.0)
    repeat = forms.BooleanField(label='repeat', required=False)
    count = forms.IntegerField(label='count(1 to 10)', required=False, min_value=1, max_value=10)
    fade = forms.BooleanField(label='fade', required=False)
    fade_start = forms.FloatField(label='start(0.0 to 10)', required=False, min_value=0.0, max_value=10)
    fade_end = forms.FloatField(label='end(0.0 to 10)', required=False, min_value=0.0, max_value=10)

    def clean_audiofile(self):
        audiofile = self.cleaned_data['audiofile']
        content_type = audiofile.content_type.split('/')[0]
        if content_type == 'audio':
            if audiofile.size > MAX_CONTENT_SIZE:
                raise forms.ValidationError('Please keep filesize under %s. Current filesize %s' % filesizeformat(MAX_CONTENT_SIZE), filesizeformat(audiofile.size))
        else:
            raise forms.ValidationError('File type is not supported')
        return audiofile