import g4f
import g4f.Provider
import os

response = g4f.ChatCompletion.create(
    model=g4f.models.llama_3_1_405b,
    provider=g4f.Provider.Blackbox,
    messages=[
        {"role" : "system", "content" : "You are not an AI and not an assistant, you are dansk teacher for students with danish level B1-B2!"},
        {"role" : "user", "content" : "Hi! Who are you and what can you do?"},
    ],
    stream=True
    # cookies={
    #     "__Secure-1PSID" : "g.a000uAjUAPGE2J6ekF4LhheHgMDw5GYKcCDVAwXpUuPwNxhTtnOSKNjcq94JDydHwEv_6944DwACgYKAQ4SARcSFQHGX2Mi8HhBsDLzBOqq2SpNhqNE5BoVAUF8yKrQhP7gITbDFCO7DgnbQa9n0076"
    # }
)

text = ""

counter = 0
for i in response:
    text += i
    if counter > 3:
        os.system("clear")
        print(text)
        counter = 0
    counter += 1

os.system("clear")
print(text)