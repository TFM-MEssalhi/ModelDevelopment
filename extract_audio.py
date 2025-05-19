import whisper
from pyannote.audio import Pipeline
import torch
from pydub import AudioSegment
import os
from dotenv import load_dotenv
import openai
import pandas as pd
import json
import csv
import re
from MedNER import MedNER
load_dotenv()

auth_token = os.getenv("HUGGING_FACE_KEY")

client = openai.OpenAI(
    base_url=os.getenv("OPENAI_URL"),
    api_key=os.getenv("OPEN_ROUTER_KEY")
)


CASES_FOLDER = os.getenv("CASES_FOLDER")
RESULTS_FOLDER = os.getenv("RESULTS_FOLDER")
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE")

def get_whisper_model(size="tiny"):
    if size not in ["tiny", "base", "small", "medium", "large", "turbo"]:
        raise ValueError("Invalid model size. Choose from: tiny, base, small, medium, large, turbo.")
    model = whisper.load_model(size)
    return model

def extract_text_from_audio_whisper(audio_file="Caso/Case1.wav", size="tiny"):
    model = get_whisper_model(size) # "tiny", "base", "small", "medium", "large", "turbo"
    result = model.transcribe(audio_file, language="es")
    print(result["text"])
    return result["text"]

def extract_audio_speechbrain(audio_file="Caso/Case1.wav"):
    asr_model = get_speechbrain_model()
    text = asr_model.transcribe_file(audio_file)
    print(text)
    return text

def extract_audio_segmentated_pyannote(audio_file="Caso/Case1.wav", size="tiny"): 
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=auth_token
        )
    pipeline.to(torch.device("cuda"))
    diarization = pipeline(audio_file)
    
    model = get_whisper_model(size)  

    audio = AudioSegment.from_wav(audio_file)

    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start, end = turn.start, turn.end

        segment = audio[int(start * 1000):int(end * 1000)]
        segment.export("temp.wav", format="wav")
        transcription = model.transcribe("temp.wav")["text"]
        results.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "speaker": speaker,
            "transcription": transcription.strip()
        })
    os.remove("temp.wav")

    df = pd.DataFrame(results)
    return df

def ask_model(prompt, modelo="google/gemini-2.0-flash-001"):
    try:
        respuesta = client.chat.completions.create(
                extra_headers={},
                extra_body={},
                model=modelo,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                        ]
                    }
                ]
            )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def redact_prompt_clean(df):
    prompt = 'Quiero que revises una transcripción de una conversación entre dos hablantes y devuelvas el resultado limpio y estructurado en formato JSON. Tu tarea es corregir errores ortográficos, eliminar muletillas y erratas, y presentar el contenido de manera clara y coherente, manteniendo los tiempos originales de inicio y fin para cada intervención. No añadas ningún comentario ni explicación adicional.\n'
    prompt += 'El resultado debe devolverse como un JSON válido, cuya clave principal sea "segments" y contenga una lista de objetos. Cada objeto representará una intervención y debe tener cuatro claves: "start" (segundo inicial del turno), "end" (segundo final del turno), "speaker" (identificador del hablante) y "transcription" (texto corregido del turno).\n'
    prompt += 'Es importante que reformules suavemente las frases si es necesario para que suenen naturales y profesionales, pero sin inventar información ni modificar el significado original. Si una parte de la transcripción contiene ruidos, muletillas o frases ininteligibles, simplemente omítelas.\n'
    prompt += 'A continuación, te facilito la transcripción original con los tiempos y hablantes especificados.:\n\n'

    for _, row in df.iterrows():
        prompt += f"Speaker {row['speaker']} ({row['start']} - {row['end']}): {row['transcription']}\n"
    
    return prompt

def redact_prompt_roles(df):
    prompt = (
        'A continuación, se presenta la transcripción de una consulta médica en la que participan diferentes personas. '
        'Tu tarea consiste en determinar el rol de cada hablante ("speaker") como uno de los siguientes: "medico", "especialista" o "paciente".\n\n'
        'Ten en cuenta las siguientes reglas:\n'
        '- Siempre habrá al menos un médico.\n'
        '- Puede haber, además, un paciente y un especialista, pero como máximo habrá un hablante por rol.\n'
        '- Si solo se identifica a un profesional de la salud, su rol será "medico".\n'
        '- Si hay más de un profesional de la salud, uno será "medico" y el otro deberá ser clasificado como "especialista".\n\n'
        'Devuelve únicamente un JSON con la siguiente estructura, donde cada clave es un identificador de hablante ("speaker") y su valor es su rol correspondiente:\n'
        '{"SPEAKER_00": "medico", "SPEAKER_01": "paciente", ...}\n\n'
        'Aquí tienes la transcripción con las intervenciones de cada hablante, incluyendo los tiempos correspondientes:\n\n'
    )

    for _, row in df.iterrows():
        prompt += f"Speaker {row['speaker']} ({row['start']} - {row['end']}): {row['transcription']}\n"

    return prompt



def handle_response_clean_text(json_response):
    results = []
    try:
        json_response = json_response.replace('```json', '').replace('```', '').strip()
        response = json.loads(json_response)
        
        if "segments" in response:
            segments = response["segments"]
            for segment in segments:
                start = segment.get("start")
                end = segment.get("end")
                speaker = segment.get("speaker")
                transcription = segment.get("transcription")
                results.append({
                    "start": round(start, 2),
                    "end": round(end, 2),
                    "speaker": speaker,
                    "transcription": transcription
                })
            df = pd.DataFrame(results)
            return df
        else:
            print("No segments found in the response.")
            return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def handle_response_assign_roles(json_response, df):
    try:
        json_response = json_response.replace('```json', '').replace('```', '').strip()
        response = json.loads(json_response)
        for speaker, role in response.items():
            df["speaker"] = df["speaker"].replace(speaker, role)
        return df
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def clean_text(text):
    texto_sin_puntuacion = re.sub(r'[.,…]', '', text)
    palabras = [palabra.lstrip() for palabra in texto_sin_puntuacion.split()]
    return ' '.join(palabras)


def extract_medical_concepts(df, output_path):
    medner = MedNER()
    agrupado = df.groupby("speaker")["transcription"].apply(lambda x: " ".join(x)).to_dict()
    medical_concepts = {}
    for key, value in agrupado.items():
        medical_concepts[key] = {}
        resultado = medner.get_ner(value)
        for entidad in resultado:
            word = clean_text(entidad['word'])
            entity = entidad['entity_group']
            score = entidad['score']
            medical_concepts[key].setdefault(entity, []).append(word)
    with open(output_path + "medical_concepts.json", "w", encoding="utf-8") as archivo:
        json.dump(medical_concepts, archivo, ensure_ascii=False, indent=2)

def extract_audio(case):
    model = os.getenv("OPEN_ROUTER_MODEL")
    case_input_path = CASES_FOLDER + case
    case_output_path = RESULTS_FOLDER + case
    if not os.path.exists(case_output_path):
        os.makedirs(case_output_path)
    case_output_path = RESULTS_FOLDER + case + "/audio"
    print("Extracting audio from video")
    df = extract_audio_segmentated_pyannote(audio_file=case_input_path + ".wav", size=WHISPER_MODEL_SIZE)
    df.to_csv(case_output_path + ".csv", index=False)
    print("Cleaning text")
    prompt = redact_prompt_clean(df)
    respuesta_modelo = ask_model(prompt, model)
    print(respuesta_modelo)
    df_cleaned = handle_response_clean_text(respuesta_modelo)
    if df_cleaned is not None:
        df_cleaned.to_csv(case_output_path + "_cleaned_text.csv", index=False, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
    else:
        print("Error while cleaning the text.")
    df_cleaned = pd.read_csv(case_output_path + "_cleaned_text.csv")
    print("Obtaining roles")
    prompt = redact_prompt_roles(df_cleaned)
    respuesta_modelo = ask_model(prompt, model)
    df_roles_and_clean = handle_response_assign_roles(respuesta_modelo, df_cleaned)
    if df_roles_and_clean is not None:
        df_roles_and_clean.to_csv(case_output_path + "_cleaned_text_and_roles.csv", index=False, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
    else:
        print("Error while assigning roles.")
    print("Extracting medical concepts")
    extract_medical_concepts(df_roles_and_clean, case_output_path)


def clinic_segmentation(df):
    with open("prompts/segmentación_clinica.txt", "r") as archivo:
        clinical_segmentation = archivo.read()
    prompt = clinical_segmentation + "\n\n"
    for _, row in df.iterrows():
        prompt += f"Speaker {row['speaker']} ({row['start']} - {row['end']}): {row['transcription']}\n"
    return prompt
if __name__ == "__main__":
    #cases = ["Case1", "Case2", "Case3", "Demo5G_Short_Final_540p", "Caso1_InfeccionRespiratoria", "Caso2_Lunares", "Caso3_Quemaduras"]
    #cases = ["Case1"]
    #for case in cases:
    #    print("Processing case:", case)
    #    extract_audio(case)
    df = pd.read_csv("Results/Caso1_InfeccionRespiratoria/audio_cleaned_text_and_roles.csv")
    prompt = clinic_segmentation(df)
    print(ask_model(prompt))
