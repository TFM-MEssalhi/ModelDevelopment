from prompts import handle_response_clean_text
text = '''
```json
{
  "segment": [
    {
      "start": 1.18,
      "end": 2.29,
      "speaker": "SPEAKER_00",
      "transcription": "Paciente Torres."
    },
    {
      "start": 5.65,
      "end": 8.82,
      "speaker": "SPEAKER_00",
      "transcription": "Un momento, por favor."
    },
    {
      "start": 11.12,
      "end": 15.3,
      "speaker": "SPEAKER_00",
      "transcription": "Señorita Torres, 22 años. ¿En qué puedo ayudarle?"
    },
    {
      "start": 15.59,
      "end": 20.87,
      "speaker": "SPEAKER_01",
      "transcription": "Hace unos días tengo dolor en la zona inferior. Me molesta al ir al baño."
    },
    {
      "start": 21.55,
      "end": 23.27,
      "speaker": "SPEAKER_01",
      "transcription": "Tengo unos exámenes en casa."
    },
    {
      "start": 23.54,
      "end": 28.16,
      "speaker": "SPEAKER_00",
      "transcription": "No es necesario. Seguramente es una infección urinaria. No es grave."
    },
    {
      "start": 29.7,
      "end": 31.92,
      "speaker": "SPEAKER_01",
      "transcription": "Sí, es como si tuviera algo."
    },
    {
      "start": 33.31,
      "end": 38.98,
      "speaker": "SPEAKER_00",
      "transcription": "Las infecciones urinarias son incómodas, pero no graves."
    },
    {
      "start": 39.08,
      "end": 42.52,
      "speaker": "SPEAKER_00",
      "transcription": "Tomará antibióticos por una semana."
    },
    {
      "start": 43.06,
      "end": 51.89,
      "speaker": "SPEAKER_00",
      "transcription": "Evite relaciones para prevenir complicaciones. Si no mejora, regrese."
    },
    {
      "start": 53.71,
      "end": 54.33,
      "speaker": "SPEAKER_00",
      "transcription": "Cuando sea."
    },
    {
      "start": 54.33,
      "end": 54.99,
      "speaker": "SPEAKER_01",
      "transcription": "Gracias."
    }
  ]
}
```
'''


df = handle_response_clean_text(text)
print(df)