import g4f
import g4f.Provider
import os




response = g4f.ChatCompletion.create(
    model=g4f.models.glm_z1_rumination_32b,
    messages=[{"role" : "user", "content": "Яка різниця між критстиянцтвом та ісламом"}],
    # provider=g4f.Provider.PerplexityLabs,
    stream=True,
    # api_key="AIzaSyB_wYlmOsTD9b2U84tdRgH9AD1nToHu_vg"
)

text = ""

for i in response:
    text += str(i)
    os.system("clear")
    print(text)