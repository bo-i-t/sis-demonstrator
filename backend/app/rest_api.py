'''
REST API backend for SIS speech assistent
'''
import os
import json
import glob
from os.path import join
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename

from app import app

from app.src.audio_file_handler import UploadRecord
from app.src.transcripe import transcripe_and_predict

# packages to use whisper for ASR
import whisper
import spacy

from flask_cors import CORS

SAVING_DIR = os.path.join('user_data', 'audio')
os.makedirs(SAVING_DIR, exist_ok=True)

CORS(app)
api = Api(app, prefix='/humaine/humaine/')

# loading whisper for ASR
WHISPER_MODEL = whisper.load_model("small")
GER_NLP_SPACY = spacy.load("de_core_news_sm")

# request url to NLP Classification
NLP_URL = "http://torchserve:8080/predictions/sismedbert"


def _load_file(filename):
    """loading results of transcript and transforming to list
    ----------
    filename : str
        path and file name

    Returns
    -------
    list
        list containing dictionaries of transcripted text and class predictions
    """

    # Opening JSON file
    with open(filename, encoding="utf-8") as file:
        data = json.load(file)

    return data['transcript']


class SavePredict(Resource):
    """Pipeline to save audio records and applying ASR and
    class predictions."""
    def post(self):
        """save files and apply AI models for transcript

        Returns
        -------
        dict
            transcript dictionary containing text and class
        """
        # saving the audio data as webm and wav
        uploader = UploadRecord(saving_dir=SAVING_DIR)
        filename = uploader.save_record()

        # create
        wavfile = join(SAVING_DIR, filename + ".wav")

        transcript = transcripe_and_predict(
            filename=wavfile,
            asr_model=WHISPER_MODEL,
            nlp_url=NLP_URL,
            nlp_spacy=GER_NLP_SPACY
        )

        return {'transcript': transcript}


class GetLatestResult(Resource):
    """Flask route to read latest transcript with predicted class."""
    def get(self):
        """reading latest transcript

        Returns
        -------
        dict
            transcript dictionary containing text and class
        """
        # identify latest data file
        files = glob.glob(SAVING_DIR + "/*.json")
        latest_filename = max(files, key=os.path.getctime)

        # Opening JSON file
        dictionary = _load_file(latest_filename)

        return dictionary


class GetResult(Resource):
    """Flask route to read specified result file."""
    def get(self, filename):
        """reading specified transcript

        Parameters
        ----------
        filename : str
            name of the transcript

        Returns
        -------
        dict
            transcript dictionary containing text and class
        """
        filename_path = join(SAVING_DIR, filename)
        # Opening JSON file
        dictionary = _load_file(filename_path)

        return dictionary


class GetFileList(Resource):
    """Flask route to receive list of recorded files."""
    def get(self):
        """creating list of recorded audio files.

        Returns
        -------
        list
            all existing file names
        """
        files = glob.glob(SAVING_DIR + "/*.json")

        # iterting through file paths and extract the filename
        list_files = []
        for (_, file_path) in enumerate(files):
            file = file_path.split("/")[-1]
            filename = file.split(".")[0]
            list_files.append(filename)

        return list_files


class DeleteFile(Resource):
    """Flask route for deleting files"""
    def get(self, filename):
        """Deleting audio and result files of given base name.

        Parameters
        ----------
        filename : str
            file name
        """
        file_types = [".wav", ".webm", ".json"]
        file_base_path = join(
            SAVING_DIR,
            secure_filename(filename)
            )

        # delete files if exists
        for file_type in file_types:
            try:
                os.remove(file_base_path + file_type)
            except FileNotFoundError:
                print(f"Did not found file {file_base_path+file_type}.")


class DestroySession(Resource):
    """Flask route to remove data, when session is aborted."""
    def get(self):
        """Deletion of session data."""
        # iterate through data and removing it
        for file in os.listdir(SAVING_DIR):
            os.remove(join(SAVING_DIR, file))


api.add_resource(GetLatestResult, '/latest_result')
api.add_resource(GetFileList, '/file_list')
api.add_resource(GetResult, '/get_result/<string:filename>')
api.add_resource(DeleteFile, '/delete_file/<string:filename>')
api.add_resource(DestroySession, '/destroy_session')
api.add_resource(SavePredict, '/transcription')
