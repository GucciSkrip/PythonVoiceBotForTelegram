import telebot
import os
import urllib
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import re

token = ''
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    bot.reply_to(message, 'хе-хе🙃')  # отправляем ответное сообщение с текстом.


@bot.message_handler(content_types=['voice'])  # на голосовое сообщение отвечает текстом этого сообщения.
def send_voice_message(message):
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file_url = f'https://api.telegram.org/file/bot{token}/{file_info.file_path}'

    with tempfile.TemporaryDirectory() as tmpdir:
        ogg_filename = os.path.join(tmpdir, 'voice.ogg')
        wav_filename = os.path.join(tmpdir, 'voice.wav')

        urllib.request.urlretrieve(file_url, ogg_filename)

        sound = AudioSegment.from_file(ogg_filename, format='ogg')
        sound.export(wav_filename, format='wav')

        text = recognize_speech(wav_filename)

    bot.reply_to(message, text)


def recognize_speech(wav_filename):  # переводит аудио в текст.
    recognizer = sr.Recognizer()

    with sr.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)

    text = recognizer.recognize_google(wav_audio, language='ru')
    text = re.sub(r' (\b[А-ЯA-Z][А-Яа-яA-Za-z]*\b)', r'. \1', text)  # Перед заглавной буквой ставится точка.
    text = re.sub(r' \b(а|но|зато|что)\b', r', \1', text)  # Перед словами "а", "но", "зато", "что" ставится запятая.

    return text


@bot.message_handler(commands=['start'])  # на команду "старт" отвечает сообщением с именем пользователя.
def say_hi(message):
    bot.send_message(message.chat.id,
                     'Привет, ' + message.chat.first_name + '. Пришли мне голосовое сообщение и я попробую перевести, что же там намямлил твой собеседник)')


@bot.message_handler(commands=['random_fact'])  # на команду "случайный факт" отвечает сообщением с именем пользователя.
def say_hi(message):
    bot.send_message(message.chat.id,
                     message.chat.first_name + ', лови. ' + 'В женском организме содержится в 6 раз больше золота, чем в мужском.')


bot.polling(none_stop=True)
