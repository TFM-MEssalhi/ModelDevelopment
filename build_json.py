import csv
import json
from datetime import datetime
from uuid import uuid4

# Utilidad para convertir a segundos
def time_to_seconds(t):
    parts = list(map(int, t.split(":")))
    return parts[0] * 3600 + parts[1] * 60 + (parts[2] if len(parts) > 2 else 0)

# Leer transcripción CSV
def load_transcription(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [
            {
                "start": float(row["start"]),
                "end": float(row["end"]),
                "speaker": row["speaker"].lower(),
                "transcription": row["transcription"]
            } for row in reader
        ]

# Leer archivos JSON
def load_json(file_path):
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)

# Generar transcripción completa
def generate_clean_transcription(transcription_data):
    return " ".join([entry["transcription"] for entry in transcription_data])

# Construir estructura clinical_segments
def build_clinical_segments(fases):
    labels = {
        "🟢": "courtesy",
        "🟠": "symptoms",
        "🔵": "diagnosis",
        "🔴": "treatment",
        "⚪": "closure"
    }
    segments = {}
    for f in fases:
        key = labels.get(f["icono"], "other")
        segments[key] = {
            "time_range": f["tiempo"],
            "description": f["resumen"]
        }
    return segments

# Extraer conceptos médicos unificados
def extract_medical_concepts(data):
    all_concepts = set()
    for role in data:
        for category in data[role]:
            all_concepts.update(data[role][category])
    return sorted(all_concepts)

def extract_symptoms(hechos):
    return hechos.get("Paciente", [])


def build_transcription_structure(transcription_data):
    return {
        "segments": transcription_data
    }
    
# Crear JSON final
def build_final_json(path):    
    transcription_data = load_transcription(path+"_cleaned_text_and_roles.csv")
    resumen_fases = load_json(path+"_clinic_segmentation.json")
    anotaciones = load_json(path+"_medical_concepts.json")
    hechos = load_json(path+"_symptoms.json")
    diagnosis = load_json(path+"_diagnosis.json")
    speakers_present = sorted(set(entry["speaker"] for entry in transcription_data))

    final_json = {
        "session_id": str(uuid4()),
        "timestamp": datetime.now().isoformat(),
        "speakers": speakers_present,
        "clinical_segments": build_clinical_segments(resumen_fases["resumen_fases"]),
        "medical_concepts": {
            "especialista": anotaciones.get("especialista", {}),
            "medico": anotaciones.get("medico", {}),
            "patient": anotaciones.get("paciente", {})
        },
        "extracted_symptoms": extract_symptoms(hechos),
        "diagnosis": diagnosis,
        "transcription": build_transcription_structure(transcription_data)
    }
    with open(path + "_clinic_session.json", "w", encoding="utf-8") as out_file:
        json.dump(final_json, out_file, ensure_ascii=False, indent=2)
    return final_json