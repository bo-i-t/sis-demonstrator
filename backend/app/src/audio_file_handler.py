'''
Processing audio files
'''
from os import system as sys
from os.path import join
import werkzeug
from flask_restful import reqparse
from werkzeug.utils import secure_filename


class UploadRecord():
    """Class to save audio files."""
    def __init__(self, saving_dir):
        self.saving_dir = saving_dir
        self.audio_file = self._get_audio_file()
        self.base_name = secure_filename(self.audio_file.filename)
        self.file_path = join(saving_dir, self.base_name)

    def _get_audio_file(self):
        """Getting the recorded audio file

        Returns
        -------
        werkzeug.datastructures.FileStorage
            recorded audio data
        """
        parse = reqparse.RequestParser()
        parse.add_argument(
            'file',
            type=werkzeug.datastructures.FileStorage,
            location='files'
            )
        args = parse.parse_args()
        audio_file = args['file']

        return audio_file

    def _convert_webm_to_wav(self):
        """converting webm file to wav with ffmpeg"""
        # creating paths with file name for the converting to wav
        filename = self.file_path + ".webm"
        wavfile = self.file_path + ".wav"

        # applying ffmpeg to convert file format
        sys(f'ffmpeg -y -i {filename} \
            -acodec pcm_s16le -ac 1 -ar 16000 {wavfile}'
            )

    def save_record(self):
        """Saving the recorded audio file as webm and wav

        Returns
        -------
        dict
            dictionary containing the base file name
        """
        # save audio file as .webm format
        self.audio_file.save(self.file_path + '.webm')

        # convert webm data to wav
        self._convert_webm_to_wav()

        return self.base_name
