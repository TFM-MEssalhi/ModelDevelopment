
import os
import csv
from MedNER import MedNER
from AudioProcessor import AudioProcessor
from prompts import prompt_clean_transcription, handle_response_clean_text, prompt_assign_roles, handle_response_assign_roles, prompt_clinic_segmentation, handle_response_clinic_segmentation, prompt_sympthoms, prompt_sympthoms, handle_response_sympthoms
from dss_rules import diagnosis
from llm_model import LLMmodel
import pandas as pd
import json 
CASES_FOLDER = os.getenv("CASES_FOLDER")
RESULTS_FOLDER = os.getenv("RESULTS_FOLDER")
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE")


def clean_text(df, output_path, llm_model):
    prompt = prompt_clean_transcription(df)
    respuesta_modelo = llm_model.ask_model(prompt)
    df_cleaned = handle_response_clean_text(respuesta_modelo)
    if df_cleaned is not None:
        df_cleaned.to_csv(output_path + "_cleaned_text.csv", index=False, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
        return df_cleaned
    else:
        raise ValueError("Error while cleaning the text.")

def identify_speakers(df, output_path, llm_model):
    prompt = prompt_assign_roles(df)
    respuesta_modelo = llm_model.ask_model(prompt)
    df_roles_and_clean = handle_response_assign_roles(respuesta_modelo, df)
    if df_roles_and_clean is not None:
        df_roles_and_clean.to_csv(output_path + "_cleaned_text_and_roles.csv", index=False, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
        return df_roles_and_clean
    else:
        raise ValueError("Error while assigning roles.")

def clinic_segmentation(df, output_path, llm_model):
    prompt = prompt_clinic_segmentation(df)
    respuesta_modelo = llm_model.ask_model(prompt)
    clinic_segmentation = handle_response_clinic_segmentation(respuesta_modelo)
    if clinic_segmentation is not None:
        with open(output_path + "_clinic_segmentation.json", "w", encoding="utf-8") as f:
            json.dump(clinic_segmentation, f, ensure_ascii=False, indent=4)
        return clinic_segmentation
    else:
        raise ValueError("Error while performing temporal segmentation.")

def medical_ner(df, output_path, medner):
    medical_concepts = medner.extract_medical_concepts(df, output_path)
    return medical_concepts

def extract_sympthoms(df, output_path, llm_model):
    prompt = prompt_sympthoms(df)
    respuesta_modelo = llm_model.ask_model(prompt)
    sympthoms_json = handle_response_sympthoms(respuesta_modelo)
    if sympthoms_json is not None:
        with open(output_path + "_sympthoms.json", "w", encoding="utf-8") as f:
            json.dump(sympthoms_json, f, ensure_ascii=False, indent=4)
        return clinic_segmentation
    else:
        raise ValueError("Error while extracting symptoms.")

def diagnosis_with_dss(sympthoms_json, output_path):
    result = diagnosis(sympthoms_json)
    print(result)
    with open(output_path + "_diagnosis.json", "w", encoding="utf-8") as f:
        for res in result:
            f.write(f"{res}\n")
    return result
def main(case, llm_model, audio_processor, medner):
    case_input_path = CASES_FOLDER + case
    case_output_folder = RESULTS_FOLDER + case
    if not os.path.exists(case_output_folder):
        os.makedirs(case_output_folder)
    case_output_path = case_output_folder + "/audio"
    """
    print("Extracting audio from video")
    df = audio_processor.extract_audio_segmentated_pyannote(audio_file=case_input_path + ".wav")
    df.to_csv(case_output_path + ".csv", index=False)
    print("Cleaning text")
    df_cleaned = clean_text(df, case_output_path, llm_model)
    print("Obtaining roles")
    df_cleaned = pd.read_csv(case_output_path + "_cleaned_text.csv", encoding='utf-8')
    df_cleaned_with_speakers = identify_speakers(df_cleaned, case_output_path, llm_model)
    """
    df_cleaned_with_speakers = pd.read_csv(case_output_path + "_cleaned_text_and_roles.csv", encoding='utf-8')
    print("Performing clinic segmentation")
    clinic_segmentation(df_cleaned_with_speakers, case_output_path, llm_model)
    print("Performing medical NER")
    medical_ner(df_cleaned_with_speakers, case_output_path, medner)
    print("Extracting symptoms")
    sympthmos = extract_sympthoms(df_cleaned_with_speakers, case_output_path, llm_model)
    print("Diagnosing with DSS")
    diagnosis = diagnosis_with_dss(sympthmos, case_output_path)
if __name__ == "__main__":
    #medner = MedNER()
    llm_model = LLMmodel()
    #audio_processor = AudioProcessor(size=WHISPER_MODEL_SIZE)
    medner = None
    audio_processor = None
    cases = ["Caso1_InfeccionRespiratoria", "Caso2_Lunares", "Caso3_Quemaduras"]
    #cases = ["Caso1_InfeccionRespiratoria"]
    for case in cases:
        print("Processing case:", case)
        main(case, llm_model, audio_processor, medner)


