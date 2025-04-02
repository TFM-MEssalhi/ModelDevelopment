def extract_words(text):
    #ner_pipeline = pipeline("ner", model="PlanTL-GOB-ES/roberta-base-biomedical-clinical-es")
    ner_pipeline = pipeline("ner", model="PlanTL-GOB-ES/bsc-bio-ehr-es")

    text = "Paciente con hipertensión arterial y diabetes mellitus tipo 2."
    resultados = ner_pipeline(text)
    print(resultados)