# Replace with your API key
API_KEY = "AIzaSyB_wYlmOsTD9b2U84tdRgH9AD1nToHu_vg"

# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part.from_text(text="""Hi!"""),
        ],
    ),
]

client = genai.Client(
    api_key=API_KEY,
)

model = "learnlm-2.0-flash-experimental"

generate_content_config = types.GenerateContentConfig(
    response_mime_type="text/plain",
    system_instruction=[
        types.Part.from_text(text="""Ти вчитель, який вчить всього чого хоче узнати учень! Ти повинен аналізувати інтереси учня та намагатисяя відповідати як умога цікавіше твої відповіді не повинні бути довгими (1-7 речень). Ти повинен розмовляти на данськохю і  рівень датськох твого учня B1, і після кожного твого речення ти повинен писати преревод на українську """),
    ]
)

def generate():
    while True:
        inp = input("Your message: ")
        contents.append(
                types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=inp),
                ],
            )
        )
        text = ""
        os.system("clear")
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            print(chunk.text, end="")
            text += chunk.text

        contents.append(
                types.Content(
                role="model",
                parts=[
                    types.Part.from_text(text=text),
                ],
            )
        )
generate()
