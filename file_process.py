import requests
import os
from pydub.utils import mediainfo


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Файл {file_path} успешно удален.")
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при удалении файла {file_path}: {e}")


def save_audio_file(file_name, file_link):
    response = requests.get(file_link)
    # Сохраняем аудиофайл локально для последующей обработки
    sound_folder = 'sound'
    local_file_path = f"{sound_folder}/{file_name}"

    if not os.path.exists(sound_folder):
        # Если папки нет, создаем её
        os.makedirs(sound_folder)

    with open(local_file_path, 'wb') as local_file:
        local_file.write(response.content)
    return local_file_path


def save_text_to_file(file_name, trance_text):
    text_folder = 'output'
    local_file_path = f"{text_folder}/{file_name.replace('.', '_') + '.txt'}"

    if not os.path.exists(text_folder):
        # Если папки нет, создаем её
        os.makedirs(text_folder)
    # Сохраняем вывод в текстовый файл
    with open(local_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(trance_text)

    return local_file_path


def file_duration_check(file_path):
    audio_info = mediainfo(file_path)
    duration = float(audio_info['duration'])
    print(duration)
    return duration
