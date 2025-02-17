from speechbrain.pretrained import EncoderDecoderASR
from speechbrain.pretrained import EncoderClassifier
from speechbrain.pretrained import VAD

# script to download all nesseccary speechbrain models from huggingface
# to run the ASR in the WebApp

if __name__ == '__main__':

    asr_model = EncoderDecoderASR.from_hparams(
                    source="jfreiwa/asr-crdnn-german-umlaute",
                    savedir="app/models/asr-crdnn-german-umlaute/",
                    run_opts={"device":"cpu"}
                    )

    VAD = VAD.from_hparams(
                    source="speechbrain/vad-crdnn-libriparty",
                    savedir="app/models/vad-crdnn-libriparty",
                    run_opts={"device":"cpu"}
                    )

    classifier = EncoderClassifier.from_hparams(
                    source="speechbrain/spkrec-ecapa-voxceleb",
                    savedir="app/models/spkrec-ecapa-voxceleb",
                    run_opts={"device":"cpu"}
                    )