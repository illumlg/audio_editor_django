from audio_editor_django.settings import BASE_DIR

DATABASE = 'sqlite3.db'
VALID_FORMATS = ['.aif', '.aifc', '.aiff', '.au', '.avr', '.snd', '.wav']
INPUT_DIRECTORY = 'input files/'
OUTPUT_DIRECTORY = 'output files/'
CONTENT_TYPE = ['audio']
MAX_CONTENT_SIZE = 20 * 1024 * 1024  # 20Mb max limit.
STORAGE_LIMIT = 400 * 1024 * 1024 # 400Mb
MAX_REPEATS = 10
MAX_SPEED = 10.0
MIN_SPEED = 0.1
MAX_VOICES = 5
MAX_VOLUME = 15
MIN_VOLUME = -50
