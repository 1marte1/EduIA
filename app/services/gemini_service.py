import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def generar_guion(topic: str):

    prompt = f"""
    Devuelve SOLO JSON válido, sin texto adicional, sin bloques de código.

    Formato exacto:

    {{
      "title": "{topic}",
      "introduccion": {{
        "text": "Texto de introducción al tema, 2-3 oraciones.",
        "duration": 10
      }},
      "explicacion": {{
        "text": "Explicación técnica del tema. Puedes usar saltos de línea \\n para separar párrafos o puntos clave.",
        "duration": 15
      }},
      "ejemplo": {{
        "text": "Descripción del ejemplo práctico.",
        "duration": 15,
        "charts": [
          {{
            "type": "bar",
            "title": "Título de la gráfica",
            "data": [
              {{"name": "Caso A", "value": 85}},
              {{"name": "Caso B", "value": 62}},
              {{"name": "Caso C", "value": 91}}
            ]
          }}
        ]
      }},
      "conclusion": {{
        "text": "Conclusión del tema. Separa los puntos clave con punto y seguido.",
        "duration": 8
      }}
    }}

    Instrucciones:
    - Los valores de "duration" son segundos, ajústalos según la cantidad de texto.
    - En "charts", incluye datos numéricos reales y relevantes al tema {topic}.
    - Puedes usar "type": "bar" o "type": "line" según lo que tenga más sentido.
    - Si el tema no tiene datos comparativos obvios, inventa datos ilustrativos coherentes.

    Tema: {topic}
    """

    response = model.generate_content(prompt)

    try:
        texto = response.candidates[0].content.parts[0].text
        print("RAW:", texto)

        limpio = texto.strip()
        if limpio.startswith("```"):
            limpio = limpio.replace("```json", "").replace("```", "").strip()

        data = json.loads(limpio)
        return data

    except Exception as e:
        print("Error parseando:", e)
        return texto  # fallback