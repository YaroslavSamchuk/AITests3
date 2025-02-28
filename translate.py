import requests
import json
from urllib.parse import quote

# Define languages dictionary
Languages = {"af":"Afrikaans","sq":"Albanian","ar":"Arabic","az":"Azerbaijani","eu":"Basque","bn":"Bengali","be":"Belarusian","bg":"Bulgarian","ca":"Catalan","zh-cn":"Chinese Simplified","zh-tw":"Chinese Traditional","hr":"Croatian","cs":"Czech","da":"Danish","nl":"Dutch","en":"English","eo":"Esperanto","et":"Estonian","tl":"Filipino","fi":"Finnish","fr":"French","gl":"Galician","ka":"Georgian","de":"German","el":"Greek","gu":"Gujarati","ht":"Haitian Creole","iw":"Hebrew","hi":"Hindi","hu":"Hungarian","is":"Icelandic","id":"Indonesian","ga":"Irish","it":"Italian","ja":"Japanese","kn":"Kannada","ko":"Korean","la":"Latin","lv":"Latvian","lt":"Lithuanian","mk":"Macedonian","ms":"Malay","mt":"Maltese","no":"Norwegian","fa":"Persian","pl":"Polish","pt":"Portuguese","ro":"Romanian","ru":"Russian","sr":"Serbian","sk":"Slovak","sl":"Slovenian","es":"Spanish","sw":"Swahili","sv":"Swedish","ta":"Tamil","te":"Telugu","th":"Thai","tr":"Turkish","uk":"Ukrainian","ur":"Urdu","vi":"Vietnamese","cy":"Welsh","yi":"Yiddish"}

class Exception(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def translate(from_lang=None, to_lang=None, text=None):
    if from_lang is not None:
        from_lang = from_lang.lower()
    if to_lang is not None:
        to_lang = to_lang.lower()
    if text is None or len(text) == 0:
        raise Exception("Cannot translate undefined or empty text string")
    
    detectlanguage = False
    if not from_lang:
        detectlanguage = True
    elif from_lang not in Languages:
        raise Exception(f"Cannot translate from unknown language: {from_lang}")
    
    if not to_lang or to_lang not in Languages:
        raise Exception(f"Cannot translate to unknown language: {to_lang}")
    
    text_encoded = quote(text)
    
    # Construct the URL
    url = f"https://translate.google.com/translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8"
    if not detectlanguage:
        url += f"&sl={from_lang}"
    url += f"&tl={to_lang}&dt=t&q={text_encoded}&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at"
    
    headers = {
        'Accept': 'application/json;charset=utf-8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(response.json())
        response.raise_for_status()
        content = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
    
    translated = {
        'text': '',
        'isCorrect': True,
        'source': {
            'synonyms': [],
            'pronunciation': [],
            'definitions': [],
            'examples': []
        },
        'target': {
            'synonyms': []
        },
        'translations': []
    }
    
    # Check for correction
    if content[7] is not None and len(content[7]) != 0:
        translated['isCorrect'] = False
        translated['text'] = content[7][1]
        print(content[7])
    else:
        if len(content[0]) > 0 and len(content[0][0]) > 0:
            translated["text"] = str(content[0][0][0])
        
        if content[1] != None:
            # Handle target synonyms
            if len(content) > 1 and len(content[1]) > 0 and len(content[1][0]) > 1:
                for synonym in content[1][0][1]:
                    translated['target']['synonyms'].append(synonym)
        
            # Handle translations
            if len(content[1]) > 0:
                for item in content[1]:
                    trans_type = item[0]
                    trans = {'type': trans_type, 'translations': []}
                    for i in item[2]:
                        if len(i) == 2:
                            trans['translations'].append((i[0], i[1]))
                    translated['translations'].append(trans)
        
        # Handle source synonyms
        if len(content) > 11 and content[11] is not None:
            for syn in content[11][0][1]:
                if len(syn) > 0:
                    translated['source']['synonyms'].append(syn[0])
        
        # Handle pronunciation
        if len(content[0]) > 1 and content[0][1] is not None:
            for pron in content[0][1]:
                if pron is not None:
                    translated['source']['pronunciation'].append(pron)
        
        # Handle definitions
        if len(content) > 12 and content[12] is not None:
            for defin in content[12]:
                dtype = defin[0]
                definitions = []
                for d in defin[1]:
                    if len(d) >= 3:
                        definitions.append({
                            'definition': d[0],
                            'example': d[2]
                        })
                if len(definitions) > 0:
                    translated['source']['definitions'].append({
                        'type': dtype,
                        'definitions': definitions
                    })
        
        # Handle examples
        if len(content) > 13 and content[13] is not None:
            for ex in content[13][0]:
                if ex is not None and len(ex) > 0:
                    text_without_tags = ex[0].replace('<[^>]+>', '', re.M | re.S)
                    translated['source']['examples'].append(text_without_tags)
    
    return translated

if __name__ == '__main__':
    # Example usage
    try:
        result = translate(from_lang='da', to_lang='uk', text='især')
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(e.message)