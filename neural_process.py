from transformers import pipeline
import torch
import whisper
import file_process

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
# устанавливаем количество потоков для torch
torch.set_num_threads(4)


def sound_to_text(audios):
    model = whisper.load_model("base")
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audios)
    audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # detect the spoken language
    _, probs = model.detect_language(mel)
    lang = max(probs, key=probs.get)
    print(f"Detected language: {max(probs, key=probs.get)}")
    # decode the audio
    result = model.transcribe(audios, fp16=False, language=lang)
    return result['segments'], lang


def final_process(file, file_name):
    print(f"Сохранен в директории: {file}")
    raw, detected_lang = sound_to_text(file)
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en")
    translator2 = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru")
    text = f"Перевод аудиофайла: {file_name} \n"
    text += f"В файле используется {get_language_name(detected_lang)} язык. \n"
    for segment in raw:
        text += "-------------------- \n"
        text += f"ID элемента: {segment['id']} Начало: {int(segment['start'])} --- Конец: {int(segment['end'])} \n"
        text += f"Исходный текст:{segment['text']} \n"
        if detected_lang == 'en':
            text_en = segment['text']
            translation2 = translator2(text_en)
            text += f"Перевод: {translation2[0]['translation_text']} \n"
        elif detected_lang == 'ru':
            text += ""
        else:
            translation = translator(segment['text'])
            text_en = translation[0]['translation_text']
            translation2 = translator2(text_en)
            text += f"Перевод: {translation2[0]['translation_text']} \n"

    file_process.delete_file(file)
    print(text)
    return text


def get_language_name(code):
    languages = {
        'ru': 'русский',
        'en': 'английский',
        'zh': 'китайский',
        'es': 'испанский',
        'ar': 'арабский',
        'he': 'иврит',
        'hi': 'хинди',
        'bn': 'бенгальский',
        'pt': 'португальский',
        'fr': 'французский',
        'de': 'немецкий',
        'ja': 'японский',
        'pa': 'панджаби',
        'jv': 'яванский',
        'te': 'телугу',
        'ms': 'малайский',
        'ko': 'корейский',
        'vi': 'вьетнамский',
        'ta': 'тамильский',
        'it': 'итальянский',
        'tr': 'турецкий',
        'uk': 'украинский',
        'pl': 'польский',
    }
    return languages.get(code, 'неизвестный язык')
