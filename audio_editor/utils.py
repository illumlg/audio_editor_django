import os
import random
import re
import time
from typing import Callable, Tuple, List

import sox
from django.core.files.uploadedfile import UploadedFile

from audio_editor.audio_operations import get_file
from audio_editor.const import INPUT_DIRECTORY, OUTPUT_DIRECTORY


def get_format(file: UploadedFile) -> str or None:
    if isinstance(file, UploadedFile) and file.name != '' and \
            isinstance(file.name, str):
        return '.' + re.split('\.', file.name)[-1].lower()
    return None


def generate_filename() -> str:
    return str(round(time.time() * 10000000)) + str(random.randint(1, 10000000))


def handle_file(file: UploadedFile, ops: List[Tuple[Callable, List]]):
    tfm = sox.Transformer()
    full_path_input, filename = save_file(file)
    format = get_format(file)
    for o in ops:
        o[0](tfm, *o[1])
    filename, format = get_file(tfm, filename, format)
    full_path_output = OUTPUT_DIRECTORY + filename + format
    return full_path_input, full_path_output


def save_file(file: UploadedFile) -> (bool, str):
    format = get_format(file)
    filename = generate_filename()
    full_path = INPUT_DIRECTORY + filename + format
    with open(INPUT_DIRECTORY + filename + format, 'wb+') as f:
        f.write(file.read())
    return full_path, filename
