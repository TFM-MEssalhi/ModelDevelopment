from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import pandas as pd

# Carga del modelo
model_name = "medspaner/roberta-es-clinical-trials-umls-7sgs-ner"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# Crear el pipeline de NER con agregación de tokens
ner_pipeline = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    device=0,
    aggregation_strategy="first" # Probar las otras opciones en un futuro: simple, average...
)

# Texto de ejemplo

df = pd.read_csv("Results/Case1/audio_cleaned_text_and_roles.csv")
texto = " ".join(df['transcription'].tolist())

# Resultado del modelo
resultado = ner_pipeline(texto)

# Mostrar las entidades extraídas
for entidad in resultado:
    print(f"{entidad['word']} - {entidad['entity_group']} - score: {entidad['score']:.2f}")