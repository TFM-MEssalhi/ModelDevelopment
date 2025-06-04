from durable.lang import *
from durable.engine import MessageNotHandledException

resultados = []

with ruleset('infeccion_respiratoria'):
    @when_all((m.predicado == 'tiene') & (m.objeto == 'fiebre') & (m.duracion > 3) & (m.temperatura > 38.5))
    def regla_fiebre_alta(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'infeccion_respiratoria_severa'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'tos') & (m.duracion > 7))
    def regla_tos_persistente(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'bronquitis'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'dificultad_respirar') & (m.intensidad == 'severa'))
    def regla_dificultad_respirar_severa(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'neumonia'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'dolor_pecho') & (m.duracion > 2) &
              (m.temperatura > 38))
    def regla_neumonia(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'neumonia'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'tos') & (m.duracion <= 7))
    def regla_resfriado_comun(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'resfriado_comun'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'fatiga') & (m.duracion > 5) &
              (m.objeto2 == 'tos') & (m.duracion2 > 7))
    def regla_bronquitis_o_neumonia(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'bronquitis_o_neumonia'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'fiebre') & (m.temperatura > 38) &
              (m.objeto2 == 'dificultad_respirar'))
    def regla_neumonia_severa(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'neumonia_severa'})

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

    @when_all((m.predicado == 'diagnosticado_con'))
    def salida_final(c):
        salida = f'\n✅ Diagnóstico final: El paciente {c.m.sujeto} ha sido diagnosticado con {c.m.objeto}'
        print(salida)

        recomendaciones = {
            'resfriado_comun': 'Se recomienda reposo, hidratación abundante y medicamentos para aliviar los síntomas.',
            'bronquitis': 'Es aconsejable evitar el humo, descansar y, si persiste, consultar a un médico.',
            'neumonia': 'Es imprescindible acudir a un centro médico para evaluación y posible tratamiento antibiótico.',
            'infeccion_respiratoria_severa': 'Se sugiere atención médica inmediata y seguimiento profesional.',
            'bronquitis_o_neumonia': 'Debe realizarse una evaluación médica para confirmar el diagnóstico y tratar adecuadamente.',
            'neumonia_severa': 'Se recomienda atención hospitalaria urgente.'
        }
        recomendacion = recomendaciones.get(c.m.objeto, 'Se recomienda consultar a un médico para mayor orientación.')
        print(f'🩺 Recomendación: {recomendacion}')
        resultados.append(c.m.objeto)
        resultados.append(recomendacion)




with ruleset('nevus_melanocitico'):

    @when_all((m.predicado == 'tiene') & ((m.objeto == 'lesion_pigmentada') | (m.objeto == 'lunar') | (m.objeto == 'nevus')) &
              (m.tamano < 6) & (m.borde == 'regular') & (m.color == 'uniforme'))
    def regla_nevus_benigno(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'nevus_benigno'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'lesion_pigmentada') &
              ((m.tamano >= 6) | (m.borde == 'irregular') | (m.color == 'multiple')))
    def regla_posible_melanoma(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'posible_melanoma'})

    @when_all((m.predicado == 'tiene') & ((m.objeto == 'cambio_reciente') | (m.objeto == 'cambio_tamano') | (m.objeto.matches('crecimiento.*'))))
    def regla_cambio_reciente(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'lesion_sospechosa'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'nevus_benigno'))
    def diagnostico_nevus_benigno(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'nevus_melanocitico_benigno'})

    @when_all((m.predicado == 'tiene') & ((m.objeto == 'posible_melanoma') | (m.objeto == 'lesion_sospechosa')))
    def diagnostico_sospechoso(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'lesion_sospechosa_melanoma'})

    @when_all((m.predicado == 'diagnosticado_con'))
    def salida(c):
        salida = f'\n✅ Diagnóstico final: El paciente {c.m.sujeto} ha sido diagnosticado con {c.m.objeto}'
        print(salida)
        recomendaciones = {
            'nevus_melanocitico_benigno': 'Se sugiere control dermatológico anual para seguimiento preventivo.',
            'lesion_sospechosa_melanoma': 'Es imprescindible consultar con un dermatólogo lo antes posible para evaluación especializada y posible biopsia.'
        }
        recomendacion = recomendaciones.get(c.m.objeto, 'Se recomienda una valoración médica especializada.')
        print(f'🩺 Recomendación: {recomendacion}')
        resultados.append(c.m.objeto)
        resultados.append(recomendacion)



with ruleset('quemadura_solar'):

    @when_all((m.predicado == 'tiene') & (m.objeto.matches('quemadura.*')) & (m.color == 'rojo'))
    def regla_quemadura_solar(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'quemadura_solar_grado1'})


    @when_all((m.predicado == 'tiene') & (m.objeto.matches('quemadura_piel')) & ((m.sintomas == 'ardor') | (m.sintomas == 'dolor_leve')))
    def regla_quemadura_dolorosa(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'quemadura_solar_sintomatica'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'exposicion_solar') & (m.proteccion == False))
    def regla_exposicion_riesgo(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'riesgo_quemadura'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'quemadura_piel') &
              (m.predicado == 'tiene') & (m.objeto == 'dolor_cabeza'))
    def regla_sintomas_asociados(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'reaccion_solar'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'quemadura_solar_grado1') &
              (m.duracion <= 7))
    def regla_pronostico(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'pronostico', 'objeto': 'curacion_7dias'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'ampollas'))
    def regla_quemadura_grado2(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'quemadura_solar_grado2'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'zonas_oscuras'))
    def regla_quemadura_severa(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'tiene', 'objeto': 'quemadura_solar_complicada'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'quemadura_solar_grado1'))
    def diagnostico_grado1(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'quemadura_solar_leve'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'quemadura_solar_grado2'))
    def diagnostico_grado2(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'quemadura_solar_moderada'})

    @when_all((m.predicado == 'tiene') & (m.objeto == 'quemadura_solar_complicada'))
    def diagnostico_complicada(c):
        c.assert_fact({'sujeto': c.m.sujeto, 'predicado': 'diagnosticado_con', 'objeto': 'quemadura_solar_severa'})

    @when_all((m.predicado == 'diagnosticado_con') & (m.objeto.matches('quemadura_solar.*')))
    def salida(c):
        salida = f'\n✅ Diagnóstico final: El paciente {c.m.sujeto} ha sido diagnosticado con {c.m.objeto}'
        print(salida)
        recomendaciones = {
            'quemadura_solar_leve': 'Aplicar crema hidratante, evitar nueva exposición solar y mantenerse bien hidratado.',
            'quemadura_solar_moderada': 'Utilizar pomada con aloe vera o corticoides suaves. Evitar el sol hasta la recuperación completa.',
            'quemadura_solar_severa': 'Acudir a un centro de salud. No romper las ampollas y cubrir las áreas afectadas con apósitos estériles.'
        }
        recomendacion = recomendaciones.get(c.m.objeto, 'Se recomienda atención médica si los síntomas empeoran.')
        print(f'🩺 Recomendación: {recomendacion}')
        resultados.append(c.m.objeto)
        resultados.append(recomendacion)

        

def diagnosis(sujetos_sintomas):
    ruleset_names = ['infeccion_respiratoria', 'nevus_melanocitico', 'quemadura_solar']
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
