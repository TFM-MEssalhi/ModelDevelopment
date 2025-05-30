import json
import os
import pandas as pd
import re 
def prompt_clean_transcription(df):
    with open("prompts/limpiar_transcripcion.txt", "r") as archivo:
        clean_transcription = archivo.read()
    prompt = clean_transcription + "\n\n"
    for _, row in df.iterrows():
        prompt += f"Speaker {row['speaker']} ({row['start']} - {row['end']}): {row['transcription']}\n"
    return prompt


def handle_response_clean_text(json_response):
    results = []
    try:
        print("Clean text response: ", json_response)
        match = re.search(r"```json\s*(.*?)\s*```", json_response, re.DOTALL)
        
        json_str = match.group(1).strip()
        response = json.loads(json_str)
        
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


def prompt_assign_roles(df):
    with open("prompts/identificar_hablantes.txt", "r") as archivo:
        assign_roles = archivo.read()
    prompt = assign_roles + "\n\n"
    for _, row in df.iterrows():
        prompt += f"Speaker {row['speaker']} ({row['start']} - {row['end']}): {row['transcription']}\n"
    return prompt

def handle_response_assign_roles(json_response, df):
    try:
        match = re.search(r"```json\s*(.*?)\s*```", json_response, re.DOTALL)
        json_str = match.group(1).strip()
        response = json.loads(json_str)
        for speaker, role in response.items():
            df["speaker"] = df["speaker"].replace(speaker, role)
        return df
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def prompt_clinic_segmentation(df):
    with open("prompts/segmentación_clinica.txt", "r") as archivo:
        clinical_segmentation = archivo.read()
    prompt = clinical_segmentation + "\n\n"
    for _, row in df.iterrows():
        prompt += f"Speaker {row['speaker']} ({row['start']} - {row['end']}): {row['transcription']}\n"
    return prompt

def handle_response_clinic_segmentation(json_response):
    try:
        match = re.search(r"```json\s*(.*?)\s*```", json_response, re.DOTALL)
        json_str = match.group(1).strip()
        clinic_segmentation = json.loads(json_str)
        return clinic_segmentation
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
        

def prompt_sympthoms(df):
    with open("prompts/extraer_sintomas_dss.txt", "r") as archivo:
        extract_sympthoms = archivo.read()
    prompt = extract_sympthoms + "\n\n"
    for _, row in df.iterrows():
        prompt += f"Speaker {row['speaker']} ({row['start']} - {row['end']}): {row['transcription']}\n"
    return prompt

def handle_response_sympthoms(json_response):
    try:
        match = re.search(r"```json\s*(.*?)\s*```", json_response, re.DOTALL)
        json_str = match.group(1).strip()
        response = json.loads(json_str)
        # Busca la clave 'Paciente' y devuelve la lista asociada
        if "Paciente" in response:
            return response
        else:
            print("No 'Paciente' key found in the response.")
            return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None