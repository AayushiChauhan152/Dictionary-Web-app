from django.shortcuts import render
import requests


def fetch_word_data(word):
    api_url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        #  to extract audio parts
        audio_urls = [phonetic['audio'] for phonetic in data[0]['phonetics'] if 'audio' in phonetic]
        
        verb_meaning = next((meaning for meaning in data[0]['meanings'] if meaning['partOfSpeech'] == 'verb'), None)
        
        if verb_meaning:
            meaning = verb_meaning['definitions'][0]['definition']
            synonyms = ', '.join(verb_meaning.get('synonyms', []))
            antonyms = ', '.join(verb_meaning.get('antonyms', []))

        return meaning,synonyms,antonyms,audio_urls
    return None


def fetchWord(request):
    if request.method == 'POST':
        word=request.POST.get('word')
        if word:
            if fetch_word_data(word) is not None:
                meaning, synonyms, antonyms,audio_urls = fetch_word_data(word)
                return render(request, 'index.html', {
                    "word": word,
                    "meaning": meaning,
                    "synonyms": synonyms,
                    "antonyms": antonyms,
                    "audio_urls": audio_urls,
                })
            else:
                return render(request, 'index.html', {
                    "error": "Word not found",
                })
    return render(request,'index.html')
    

    