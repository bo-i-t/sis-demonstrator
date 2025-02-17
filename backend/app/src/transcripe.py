import json
import httpx


def transcripe_and_predict(filename, asr_model, nlp_url, nlp_spacy):
    """Run the models to transcripe text and predict the SIS categorie.

    Parameters
    ----------
    filename : str
        path to the wav audio file
    asr_model : whisper.model.Whisper
        whisper model
    nlp_url : str
        url to torch serve
    nlp_spacy : spacy.lang.de.German
        german spacy model

    Returns
    -------
    dict
        dictionary with sentencewise splited transcripts
    """

    transcripted_text = asr_model.transcribe(filename)["text"]

    doc = nlp_spacy(transcripted_text)
    transcript = []
    for sent in doc.sents:

        # skip sentenced in case of empty string
        if str(sent) == " ":
            print("empty")
            continue

        # getting SIS class
        # creating payload for classification request
        payload = {
            'data': sent,
        }

        # send post request to nlp calssificator
        response = httpx.post(
            url=nlp_url,
            data=payload,
            timeout=200,
            )

        # extract result
        nlp_class = [response.text]

        transcript.append({
            "spk": "?",
            "txt": str(sent),
            "cls": str(nlp_class[0])},
            )

    json_filename = filename.split(".wav")[0] + '.json'

    # saving result as json
    with open(json_filename, 'w', encoding='utf-8') as fp:
        json.dump({'transcript': transcript}, fp)

    return transcript
