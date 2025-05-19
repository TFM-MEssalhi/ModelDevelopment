from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()

class MedNER:
    def __init__(self):
        self.model_name = os.getenv("MEDNER_MODEL")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_name)
        self.ner_pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0,
            aggregation_strategy="first" # Probar las otras opciones en un futuro: simple, average...
        )
    def get_ner(self, text):
        return self.ner_pipeline(text)
