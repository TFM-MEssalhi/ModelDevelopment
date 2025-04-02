import whisper
from pyannote.audio import Pipeline
import speechbrain.inference as sb
import torch
from pydub import AudioSegment
import os
from dotenv import load_dotenv

load_dotenv()

auth_token = os.getenv("HUGGING_FACE_KEY")

def get_whisper_model(size="tiny"):
    if size not in ["tiny", "base", "small", "medium", "large", "turbo"]:
        raise ValueError("Invalid model size. Choose from: tiny, base, small, medium, large, turbo.")
    model = whisper.load_model(size)
    return model

def get_speechbrain_model():
    asr_model = sb.EncoderASR.from_hparams(
        source="speechbrain/asr-wav2vec2-commonvoice-14-es", 
        savedir="pretrained_models/asr-wav2vec2-commonvoice-14-es",
        run_opts={"device":"cuda:0"}
        )
    return asr_model

def extract_text_from_audio_whisper(audio_file="Caso/Case1.wav"):
    model = get_whisper_model("tiny") # "tiny", "base", "small", "medium", "large", "turbo"
    result = model.transcribe(audio_file)
    print(result["text"])
    return result["text"]

def extract_audio_speechbrain(audio_file="Caso/Case1.wav"):
    asr_model = get_speechbrain_model()
    text = asr_model.transcribe_file(audio_file)
    print(text)
    return text

def extract_audio_segmentated_pyannote(audio_file="Caso/Case1.wav"): 
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=auth_token
        )
    pipeline.to(torch.device("cuda"))
    diarization = pipeline(audio_file)
    
    model = get_whisper_model("turbo")  

    audio = AudioSegment.from_wav(audio_file)

    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start, end = turn.start, turn.end

        segment = audio[int(start * 1000):int(end * 1000)]
        segment.export("temp.wav", format="wav")
        transcription = model.transcribe("temp.wav")["text"]
        results.append(f"[{start:0.2f} --> {end:0.2f}] {speaker}: {transcription}")
    os.remove("temp.wav")

    for line in results:
        print(line)



if __name__ == "__main__":
    extract_audio_segmentated_pyannote()