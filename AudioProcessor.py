import whisper
from pyannote.audio import Pipeline
import torch
from pydub import AudioSegment
import os
import pandas as pd

class AudioProcessor():
    def __init__(self, size="tiny"):
        self.auth_token = os.getenv("HUGGING_FACE_KEY")
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=self.auth_token
        )
        self.pipeline.to(torch.device("cuda"))
        self.whisper_model = self.get_whisper_model(size)
    def extract_audio_segmentated_pyannote(self, audio_file): 
        diarization = self.pipeline(audio_file)
        audio = AudioSegment.from_wav(audio_file)
        results = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start, end = turn.start, turn.end
            segment = audio[int(start * 1000):int(end * 1000)]
            segment.export("temp.wav", format="wav")
            transcription = self.whisper_model.transcribe("temp.wav")["text"]
            results.append({
                "start": round(start, 2),
                "end": round(end, 2),
                "speaker": speaker,
                "transcription": transcription.strip()
            })
        os.remove("temp.wav")
        df = pd.DataFrame(results)
        return df

    def get_whisper_model(self, size="tiny"):
        if size not in ["tiny", "base", "small", "medium", "large", "turbo"]:
            raise ValueError("Invalid model size. Choose from: tiny, base, small, medium, large, turbo.")
        model = whisper.load_model(size)
        return model

    def extract_text_from_audio_whisper(self, audio_file):
        result = self.model.transcribe(audio_file, language="es")
        return result["text"]