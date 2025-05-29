import pandas as pd
from llm_model import LLMmodel
from prompts import prompt_sympthoms, handle_response_sympthoms
from dss_rules import diagnosticar_en_todos_rulesets
import os
import json
if __name__ == "__main__":
    path = "Results/Caso2_Lunares/"
    df = pd.read_csv(path + "audio_cleaned_text_and_roles.csv", encoding='utf-8')
    promp = prompt_sympthoms(df)
    llm_model = LLMmodel()

    respuesta_modelo = llm_model.ask_model(promp)
    print(respuesta_modelo)
    sympthoms_json = handle_response_sympthoms(respuesta_modelo)
    print(sympthoms_json)
    with open(path + "sympthoms.json", "w", encoding="utf-8") as f:
            json.dump(sympthoms_json, f, ensure_ascii=False, indent=4)
    """    
    with open("Results/Caso1_InfeccionRespiratoria/sympthoms.json", "r", encoding="utf-8") as f:
        sympthoms_json = json.load(f)    
    resultado = diagnosticar_en_todos_rulesets(sympthoms_json, ['infeccion_respiratoria', 'nevus_melanocitico'])
    print(resultado)
    """
    
