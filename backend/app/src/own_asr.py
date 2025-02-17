'''
This is outsourced code of our own ASR. For the usage code
have to be copied into rest_api.py
'''
from flask_restful import Api, Resource

# packages to use own ASR model
from speechbrain.pretrained import EncoderDecoderASR
from speechbrain.pretrained import EncoderClassifier
from speechbrain.pretrained import VAD
from app import app
from app.src.vad import apply_vad
from app.src.audio_file_handler import convert_webm_to_wav
from app.src.transcripe import create_embeddings, create_transcript
from app.src.speaker_recognition import speaker_recognition
import torchaudio
import contextlib
import wave

from flask_cors import CORS

CORS(app)
api = Api(app, prefix='/humaine/humaine/')

# loading own ASR model
asr_model = EncoderDecoderASR.from_hparams(
    source="jfreiwa/asr-crdnn-german-umlaute",
    savedir="./models/asr-crdnn-german-umlaute",
    run_opts={"device": "cpu"}
    )
VAD = VAD.from_hparams(
    source="speechbrain/vad-crdnn-libriparty",
    savedir="./models/vad-crdnn-libriparty",
    run_opts={"device": "cpu"}
    )
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="./models/spkrec-ecapa-voxceleb"
    )

nlp_rq_url = "http://torchserve:8080/predictions/sismedbert"


class GetSpeakerAndTranscriptOwnASR(Resource):
    def get(self, filename):
        # Convert to Wav
        wavfile = convert_webm_to_wav(filename)

        # Segmentation
        signal, fs = torchaudio.load(wavfile)

        # run Voice Activity Detection (VAD)
        boundaries = apply_vad(wavfile=wavfile,
                               frame_duration=30,
                               vad_duration=10,
                               padding_duration=50,
                               fs=fs
                               )

        # embed the audio files
        embeddings = create_embeddings(classifier,
                                       boundaries,
                                       signal,
                                       fs
                                       )

        # identify speaker
        speaker = speaker_recognition(embeddings)

        # Transcribe
        transcript = create_transcript(
            boundaries=boundaries,
            signal=signal,
            asr_model=asr_model,
            nlp_url=nlp_rq_url,
            embeddings=embeddings,
            speaker=speaker,
            fs=fs,
            filename=filename
            )

        return {'transcript': transcript}

def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


def create_embeddings(classifier, boundaries, signal, fs):
    embeddings = []
    for i, boundary in enumerate(boundaries):
        if boundary[1] - boundary[0] > 0.1:
            segment = signal[0, int(fs * boundary[0]):int(fs*boundary[1])]
            embedding = classifier.encode_batch(segment)
            embeddings.append(embedding[0, 0, :].cpu().detach().numpy())
        else:
            del boundaries[i]

    return embeddings


def create_transcript(boundaries, signal, asr_model, nlp_url, embeddings, speaker, fs, filename):
    transcript = []
    for i, boundary in enumerate(boundaries):
        try:
            segment = signal[0, int(fs * boundary[0]):int(fs*boundary[1])]
            s1 = asr_model.audio_normalizer(segment, 16000)

            batch = s1.unsqueeze(0)
            rel_length = torch.tensor([1.0])
            predicted_words, predicted_tokens = asr_model.transcribe_batch(
                batch, rel_length
            )
            print('inside for loop: creating payload')

            payload = {
                'data': predicted_words[0],
            }

            print("starting request")
            response = httpx.post(
                url=nlp_url,
                data=payload,
                timeout=None,
                )
            nlp_class = [response.text]

            if len(embeddings) > 2:
                transcript.append({
                    "spk": "ABCDEFGHIJKLMNOPQRSTUVWXYZ?"[speaker.labels_[i]],
                    "txt": predicted_words[0],
                    "cls": str(nlp_class[0])},
                    )

            else:
                transcript.append({
                    "spk": "?",
                    "txt": predicted_words[0],
                    "cls": str(nlp_class[0]),
                    })

        except Exception as e:
            transcript.append({
                "spk": "?",
                "txt": str(e),
                "cls": "Exception",
                })

    filename = secure_filename(filename)
    json_filename = join('user_data', 'audio', filename + '.json')

    # saving result as json
    with open(json_filename, 'w') as fp:
        json.dump({'transcript': transcript}, fp)

    return transcript

api.add_resource(
    GetSpeakerAndTranscriptOwnASR,
    '/transcripts/<string:filename>'
    )