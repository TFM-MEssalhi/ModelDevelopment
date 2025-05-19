from durable.lang import *

# Definimos el conjunto de reglas para infecciones respiratorias complejas
with ruleset('respiratory_infection'):
    
    # Regla para fiebre alta (más de 38.5°C) durante más de 3 días
    @when_all((m.predicate == 'has') & (m.object == 'fever') & (m.duration > 3) & (m.temperature > 38.5))
    def high_fever_rule(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'has', 'object': 'severe_respiratory_infection'})

    # Regla para tos persistente (más de 7 días)
    @when_all((m.predicate == 'has') & (m.object == 'persistent_cough') & (m.duration > 7))
    def persistent_cough_rule(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'has', 'object': 'bronchitis'})

    # Regla para dificultad para respirar severa
    @when_all((m.predicate == 'has') & (m.object == 'severe_difficulty_breathing'))
    def severe_breathing_rule(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'has', 'object': 'pneumonia'})

    # Regla para dolor en el pecho acompañado de fiebre alta (indica neumonía)
    @when_all((m.predicate == 'has') & (m.object == 'chest_pain') & (m.duration > 2) & (m.predicate == 'has') & (m.object == 'fever') & (m.temperature > 38))
    def pneumonia_rule(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'has', 'object': 'pneumonia'})

    # Regla para un resfriado común (tos ligera y fiebre baja)
    @when_all((m.predicate == 'has') & (m.object == 'cough') & (m.duration <= 7) & (m.predicate == 'has') & (m.object == 'fever') & (m.temperature <= 38))
    def common_cold_rule(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'has', 'object': 'common_cold'})

    # Regla para fatiga severa y tos persistente (indica posible bronquitis o neumonía)
    @when_all((m.predicate == 'has') & (m.object == 'fatigue') & (m.duration > 5) & (m.predicate == 'has') & (m.object == 'persistent_cough'))
    def bronchitis_or_pneumonia_rule(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'has', 'object': 'bronchitis_or_pneumonia'})

    # Si hay combinación de fiebre alta y dificultad para respirar, diagnóstico de neumonía
    @when_all((m.predicate == 'has') & (m.object == 'fever') & (m.temperature > 38) & 
              (m.predicate == 'has') & (m.object == 'difficulty_breathing'))
    def pneumonia_with_fever_and_breathing(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'has', 'object': 'severe_pneumonia'})

    # Regla para el diagnóstico final basado en los hechos recolectados
    @when_all((m.predicate == 'has') & (m.object == 'severe_respiratory_infection'))
    def severe_infection(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'diagnosed_with', 'object': 'severe_respiratory_infection'})

    @when_all((m.predicate == 'has') & (m.object == 'bronchitis'))
    def bronchitis_diagnosis(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'diagnosed_with', 'object': 'bronchitis'})

    @when_all((m.predicate == 'has') & (m.object == 'pneumonia'))
    def pneumonia_diagnosis(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'diagnosed_with', 'object': 'pneumonia'})

    @when_all((m.predicate == 'has') & (m.object == 'common_cold'))
    def common_cold_diagnosis(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'diagnosed_with', 'object': 'common_cold'})

    @when_all((m.predicate == 'has') & (m.object == 'bronchitis_or_pneumonia'))
    def bronchitis_or_pneumonia_diagnosis(c):
        c.assert_fact({'subject': c.m.subject, 'predicate': 'diagnosed_with', 'object': 'bronchitis_or_pneumonia'})

    # Salida de diagnóstico final
    @when_all(+m.subject)
    def output(c):
        print(f'Patient {c.m.subject} has been diagnosed with {c.m.object}')

# Ejemplo de hechos (síntomas)
assert_fact('respiratory_infection', {'subject': 'Patient_1', 'predicate': 'has', 'object': 'fever'})
assert_fact('respiratory_infection', {'subject': 'Patient_2', 'predicate': 'has', 'object': 'persistent_cough', 'duration': 8})
assert_fact('respiratory_infection', {'subject': 'Patient_3', 'predicate': 'has', 'object': 'chest_pain', 'duration': 3})
assert_fact('respiratory_infection', {'subject': 'Patient_4', 'predicate': 'has', 'object': 'fatigue', 'duration': 6})
assert_fact('respiratory_infection', {'subject': 'Patient_5', 'predicate': 'has', 'object': 'difficulty_breathing'})
assert_fact('respiratory_infection', {'subject': 'Patient_6', 'predicate': 'has', 'object': 'cough', 'duration': 5, 'temperature': 37.5})
