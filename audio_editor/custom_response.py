import os

from django.http import FileResponse


class ResponseThen(FileResponse):

    def __init__(self, *args, full_path_input, full_path_output, **kwargs):
        super().__init__(*args, **kwargs)
        self.full_path_input = full_path_input
        self.full_path_output = full_path_output

    def close(self):
        super(ResponseThen, self).close()
        os.remove(self.full_path_input)
        os.remove(self.full_path_output)
