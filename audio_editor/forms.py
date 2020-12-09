from django import forms
from django.core.validators import FileExtensionValidator
from django.template.defaultfilters import filesizeformat

from audio_editor.choices import FORMAT_CHOICES, FLANGER_CHOICES, CHORUS_CHOICES
from audio_editor.const import MAX_CONTENT_SIZE


class AudiofileForm(forms.Form):
    audiofile = forms.FileField(label='Select a file(max 20 mb)', allow_empty_file=False, validators=[FileExtensionValidator(allowed_extensions=['aif', 'aifc', 'aiff', 'au', 'avr', 'snd', 'wav'])])
    convert = forms.BooleanField(label='convert', required=False)
    format = forms.ChoiceField(label='format', required=True, choices=FORMAT_CHOICES)
    chorus = forms.BooleanField(label='chorus', required=False)
    voices = forms.ChoiceField(label='voices', required=True, choices=CHORUS_CHOICES)
    trim = forms.BooleanField(label='trim', required=False)
    start_time = forms.IntegerField(label='start time', required=True, min_value=0, initial=0)
    end_time = forms.IntegerField(label='end time', required=True, min_value=1, initial=1)
    treble = forms.BooleanField(label='treble', required=False)
    gain = forms.IntegerField(label='gain(-20 to 20)', required=True, min_value=-20, max_value=20, initial=0)
    reverse = forms.BooleanField(label='reverse', required=False)
    flanger = forms.BooleanField(label='flanger', required=False)
    preset = forms.ChoiceField(label='preset', required=True, choices=FLANGER_CHOICES)
    tremolo = forms.BooleanField(label='tremolo', required=False)
    tremolo_speed = forms.FloatField(label='speed(-1 to 20)', required=True, min_value=1, max_value=20, initial=1)
    depth = forms.FloatField(label='depth(10 to 100)', required=True, min_value=10, max_value=100, initial=10)
    volume = forms.BooleanField(label='volume', required=False)
    volume_value = forms.IntegerField(label='value(-50 to 15)', required=True, min_value=-50, max_value=15, initial=0)
    echo = forms.BooleanField(label='echo', required=False)
    gain_in = forms.FloatField(label='gain_in(0.1 to 1)', required=True, min_value=0.1, max_value=1, initial=0.1)
    gain_out = forms.FloatField(label='gain_out(0.1 to 1)', required=True, min_value=0.1, max_value=1.0, initial=0.1)
    bass = forms.BooleanField(label='bass', required=False)
    gain_db = forms.FloatField(label='gain_db(-20 to 20)', required=True, min_value=-20, max_value=20, initial=0)
    freq = forms.FloatField(label='frequency(10 to 200)', required=True, min_value=10, max_value=200, initial=10)
    slope = forms.FloatField(label='slope(0.3 to 1)', required=True, min_value=0.3, max_value=1, initial=0.3)
    speed = forms.BooleanField(label='speed', required=False)
    speed_value = forms.FloatField(label='value(0.1 to 10)', required=True, min_value=0.1, max_value=10, initial=0.1)
    repeat = forms.BooleanField(label='repeat', required=False)
    count = forms.IntegerField(label='count(1 to 10)', required=True, min_value=1, max_value=10, initial=1)
    fade = forms.BooleanField(label='fade', required=False)
    fade_start = forms.FloatField(label='start(0.0 to 10)', required=True, min_value=0.0, max_value=10, initial=0)
    fade_end = forms.FloatField(label='end(0.0 to 10)', required=True, min_value=0.0, max_value=10, initial=0)

    def clean_audiofile(self):
        audiofile = self.cleaned_data['audiofile']
        if audiofile.size > MAX_CONTENT_SIZE:
            raise forms.ValidationError('Please keep filesize under %s. Current filesize %s' % filesizeformat(MAX_CONTENT_SIZE), filesizeformat(audiofile.size))
        return audiofile

    def clean(self):
        cleaned_data = super(AudiofileForm, self).clean()
        trim_start = cleaned_data.get('start_time')
        trim_end = cleaned_data.get('end_time')
        if cleaned_data.get('trim'):

            if trim_start > trim_end:
                self.add_error('trim', 'Start time is greater then end time')