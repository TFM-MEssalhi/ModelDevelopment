from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import os
from dotenv import load_dotenv
import json
import re
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
    def extract_medical_concepts(self, df, output_path):
        agrupado = df.groupby("speaker")["transcription"].apply(lambda x: " ".join(x)).to_dict()
        medical_concepts = {}
        for key, value in agrupado.items():
            medical_concepts[key] = {}
            resultado = self.get_ner(value)
            for entidad in resultado:
                word = self.clean_medical_concept(entidad['word'])
                entity = entidad['entity_group']
                score = entidad['score']
                medical_concepts[key].setdefault(entity, []).append(word)
        with open(output_path + "_medical_concepts.json", "w", encoding="utf-8") as archivo:
            json.dump(medical_concepts, archivo, ensure_ascii=False, indent=2)
        return medical_concepts
    def clean_medical_concept(self, text):
        texto_sin_puntuacion = re.sub(r'[.,…]', '', text)
        palabras = [palabra.lstrip() for palabra in texto_sin_puntuacion.split()]
        return ' '.join(palabras)
