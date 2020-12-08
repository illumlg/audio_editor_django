import sox as sox
from django.core.files.uploadedfile import UploadedFile

from audio_editor.const import INPUT_DIRECTORY, OUTPUT_DIRECTORY


new_format = ''

def convert(tfm, format: str):
    global new_format
    new_format = format


def chorus(tfm, voices: int):
    tfm.chorus(n_voices=voices)


def trim(tfm, start_time:int, end_time):
    tfm.trim(start_time, end_time)


def treble(tfm, gain: int):
    tfm.treble(gain_db=gain)


def reverse(tfm):
    tfm.reverse()


def flanger(tfm, preset: str):
    if preset == 'low':
        tfm.flanger()
    elif preset == 'medium':
        tfm.flanger(5, 4, speed=2, shape='triangle')
    elif preset == 'high':
        tfm.flanger(20, 8, speed=5, shape='triangle')


def tremolo(tfm, speed, depth):
    tfm.tremolo(speed, depth)


def volume(tfm, volume):
    tfm.vol(volume, 'db')


def echo(tfm, gain_in, gain_out):
    tfm.echo(gain_in, gain_out, 1)


def bass(tfm, gain_db, freq, slope):
    tfm.bass(gain_db, freq, slope)


def speed(tfm, value):
    tfm.speed(value)


def repeat(tfm, count):
    tfm.repeat(count)


def fade(tfm, start, end):
    tfm.fade(start, end)

# def concatenate(tfm, *files):
#     global combiner
#     combiner = sox.Combiner
#
#
# def mix(tfm, *files):
#     global combiner
#     combiner = sox.Combiner
#

def get_file(tfm, filename, file_format):
    global new_format
    if len(new_format) > 0:
        tfm.build_file(INPUT_DIRECTORY + filename + file_format,
                              OUTPUT_DIRECTORY + filename + new_format)
        file_format = new_format
        new_format = ''
    else:
        tfm.build_file(INPUT_DIRECTORY + filename + file_format,
                                   OUTPUT_DIRECTORY + filename + file_format)
    return filename, file_format
        # g.params = '(' + new_format + ')'
        # if g.access:
        #     try:
        #         file = request.files['file']
        #         format = get_format(file)
        #         is_success, filename = save_file(file)
        #         g.path_to_files.append(OUTPUT_DIRECTORY + filename + new_format)
        #         sox.Transformer().build_file(INPUT_DIRECTORY + filename + format,
        #                                      OUTPUT_DIRECTORY + filename + new_format)
        #         return app.make_response(read_file(OUTPUT_DIRECTORY + filename + new_format))
        #     except werkzeug.exceptions.BadRequest as e:
        #         g.error = True
        #         save_log(g.request_name, 'ERROR', 400, str(e), g.params)
        #         return abort(400, e)
        #     except sox.core.SoxiError or sox.core.SoxError as e:
        #         g.error = True
        #         save_log(g.request_name, 'ERROR', 400, str(e), g.params)
        #         return abort(500, e)
        #     except Exception as e:
        #         g.error = True
        #         save_log(g.request_name, 'ERROR', 500, str(e), g.params)
        #         return abort(500, e)
        # g.error = True
        # res = app.make_response('Storage is overflow, try again after a few seconds')
        # res.status_code = 507
        # save_log(g.request_name, 'ERROR', 507,
        #          'Storage is overflow, try again after a few seconds', g.params)
        # return res
