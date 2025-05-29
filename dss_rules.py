from durable.lang import *
from durable.engine import MessageNotHandledException

resultados = []

with ruleset('infeccion_respiratoria'):
    
    # Regla para fiebre alta (más de 38.5°C) durante más de 3 días
    @when_all((m.predicado == 'tiene') & (m.objeto == 'fiebre') & (m.duracion > 3) & (m.temperatura > 38.5))
    def regla_fiebre_alta(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'infeccion_respiratoria_severa'})

    # Regla para tos persistente (más de 7 días)
    @when_all((m.predicado == 'tiene') & (m.objeto == 'tos_persistente') & (m.duracion > 7))
    def regla_tos_persistente(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'bronquitis'})

    # Regla para dificultad para respirar severa
    @when_all((m.predicado == 'tiene') & (m.objeto == 'dificultad_respirar_severa'))
    def regla_dificultad_respirar_severa(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'neumonia'})

    # Regla para dolor en el pecho acompañado de fiebre alta (indica neumonía)
    @when_all((m.predicado == 'tiene') & (m.objeto == 'dolor_pecho') & (m.duracion > 2) &
              (m.predicado == 'tiene') & (m.objeto == 'fiebre') & (m.temperatura > 38))
    def regla_neumonia(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'neumonia'})

    # Regla para un resfriado común (tos ligera y fiebre baja)
    @when_all((m.predicado == 'tiene') & (m.objeto == 'tos') & (m.duracion <= 7))
    def regla_resfriado_comun(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'resfriado_comun'})

    # Regla para fatiga severa y tos persistente (posible bronquitis o neumonía)
    @when_all((m.predicado == 'tiene') & (m.objeto == 'fatiga') & (m.duracion > 5) &
              (m.predicado == 'tiene') & (m.objeto == 'tos_persistente'))
    def regla_bronquitis_o_neumonia(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'bronquitis_o_neumonia'})

    # Si hay combinación de fiebre alta y dificultad para respirar, diagnóstico de neumonía severa
    @when_all((m.predicado == 'tiene') & (m.objeto == 'fiebre') & (m.temperatura > 38) & 
              (m.predicado == 'tiene') & (m.objeto == 'dificultad_respirar'))
    def regla_neumonia_severa(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'neumonia_severa'})

    # Diagnósticos finales basados en los hechos recolectados
    @when_all((m.predicado == 'tiene') & (m.objeto == 'infeccion_respiratoria_severa'))
    def diagnostico_infeccion_severa(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'infeccion_respiratoria_severa'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'bronquitis'))
    def diagnostico_bronquitis(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'bronquitis'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'neumonia'))
    def diagnostico_neumonia(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'neumonia'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'resfriado_comun'))
    def diagnostico_resfriado_comun(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'resfriado_comun'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'bronquitis_o_neumonia'))
    def diagnostico_bronquitis_o_neumonia(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'bronquitis_o_neumonia'})

    # Salida de diagnóstico final
    @when_all((m.predicado == 'diagnosticado_con'))
    def salida_final(c):
        salida = f'\n✅ Diagnóstico final: El paciente {c.m.sujeto} ha sido diagnosticado con {c.m.objeto}'
        print(salida)
        resultados.append(c.m.objeto)



# Definimos el conjunto de reglas para diagnóstico de nevus melanocítico
with ruleset('nevus_melanocitico'):

    # Regla para lesión pigmentada pequeña (menor a 6 mm) con borde regular y color uniforme (benigno)
    @when_all((m.predicado == 'tiene') & (m.objeto == 'lesion_pigmentada') & (m.tamano < 6) &
              (m.borde == 'regular') & (m.color == 'uniforme'))
    def regla_nevus_benigno(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'nevus_benigno'})

    # Regla para lesión pigmentada mayor o igual a 6 mm, borde irregular o colores múltiples (posible melanoma)
    @when_all((m.predicado == 'tiene') & (m.objeto == 'lesion_pigmentada') & 
              ((m.tamano >= 6) | (m.borde == 'irregular') | (m.color == 'multiple')))
    def regla_posible_melanoma(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'posible_melanoma'})

    # Regla para lesión que ha cambiado de tamaño o forma en los últimos 6 meses
    @when_all((m.predicado == 'tiene') & (m.objeto == 'cambio_reciente') & (m.periodo_meses <= 6))
    def regla_cambio_reciente(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'lesion_sospechosa'})

    # Diagnóstico final para nevus benigno
    @when_all((m.predicado == 'tiene') & (m.objeto == 'nevus_benigno'))
    def diagnostico_nevus_benigno(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'nevus_melanocitico_benigno'})

    # Diagnóstico final para posible melanoma o lesión sospechosa
    @when_all((m.predicado == 'tiene') & ((m.objeto == 'posible_melanoma') | (m.objeto == 'lesion_sospechosa')))
    def diagnostico_sospechoso(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'lesion_sospechosa_melanoma'})

    # Salida del diagnóstico
    @when_all(+m.sujeto)
    def salida(c):
        print(f'El paciente {c.m.sujeto} ha sido diagnosticado con {c.m.objeto}')

def diagnosticar_en_todos_rulesets(sujetos_sintomas, ruleset_names):
    resultados.clear()
    for ruleset_name in ruleset_names:
        for sujeto, sintomas in sujetos_sintomas.items():
            for sintoma in sintomas:
                sintoma.setdefault('sujeto', sujeto)
                try:
                    post(ruleset_name, sintoma)
                except MessageNotHandledException:
                    pass
    return resultados
