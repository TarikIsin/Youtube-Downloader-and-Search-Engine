from datetime import datetime
import time
import tkinter as tk
import webbrowser
from tkinter import messagebox
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from pytube import YouTube
import random
import os


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('400x140')
        self.root.title("App")
        self.root.config(bg='#34495E')
        self.label = tk.Label(self.root, text='Welcome.', bg='#34495E', fg='#BDC3C7',
                              font=('Arial', 16))
        self.label.pack(padx=10, pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.button1 = tk.Button(self.frame, text='Video Downloader', command=self.youtube, bg='#0E6655',
                                 fg='#BDC3C7')
        self.button1.grid(row=0, column=0)

        self.button2 = tk.Button(self.frame, text='Siri', command=self.siri, bg='#0E6655',
                                 fg='#BDC3C7')
        self.button2.grid(row=0, column=1)

        self.root.protocol('WM_DELETE_WINDOW', self.close_window)
        self.root.mainloop()


    def siri(self):
        self.root = tk.Tk()
        self.root.geometry('400x150')
        self.root.config(bg='#34495E')
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.button = tk.Button(self.frame, text='Speak', command=self.response, bg='#0E6655',
                                fg='#BDC3C7')
        self.button.grid(row=0, column=3)

        self.textbox = tk.Text(self.root, height=1, width=30, bg='#0E6655',
                               fg='#BDC3C7')
        self.textbox.pack(padx=10, pady=10)
        self.textbox.insert(1.0, 'How Can I Help You?')

        self.root.mainloop()

    def record_sound(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            voice = ''
            try:
                voice = r.recognize_google(audio, language='tr-TR')
            except sr.UnknownValueError:
                message = 'I Dont Understand.'
                self.speak(message)
            except sr.RequestError:
                message = 'System Doesnt Work.'
                self.speak(message)
            return voice

    def response(self):
        voice = self.record_sound()
        if 'nasılsın' in voice:
            self.textbox.delete('1.0', 'end')
            self.textbox.insert('1.0', 'İyi, senden')
            message = 'İyi senden'
            self.speak(message)
        if 'saat kaç' in voice:
            self.textbox.delete('1.0', 'end')
            time = datetime.now().strftime('%H:%M:%S')
            self.textbox.insert('1.0', time)
            self.speak(time)
        if 'arama yap' in voice:
            self.textbox.delete('1.0', 'end')
            self.textbox.insert('1.0', 'Ne aramak istersin?')
            message = 'Ne aramak istersin?'
            self.speak(message)
            self.btn2 = tk.Button(self.frame, text='Search', command=self.search, bg='#0E6655',
                                  fg='#BDC3C7')
            self.btn2.grid(row=0, column=6)
        if 'kapat' in voice:
            self.close_window()

    def search(self):
        search = self.record_sound()
        self.speak('Looking For You')
        url = 'https://www.google.com/search?client=opera-gx&q=' + search
        webbrowser.get().open(url)


    def speak(self, string):
        tts = gTTS(string, lang='tr')
        rand = random.randint(1, 10000)
        file = 'audio-' + str(rand) + '.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)


    def youtube(self):

        self.root = tk.Tk()
        self.root.geometry('500x250')
        self.root.title("Youtube Downloader")
        self.root.config(bg='#34495E')
        self.label = tk.Label(self.root, text='URL of the video you want to download??', bg='#34495E', fg='#BDC3C7',
                              font=('Arial', 16))
        self.label.pack(padx=10, pady=10)

        self.menubar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label='Close', command=self.close_window)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Close Without Question', command=exit)

        self.action_menu = tk.Menu(self.menubar, tearoff=0)
        self.action_menu.add_command(label='Show Message', command=exit)

        self.menubar.add_cascade(menu=self.file_menu, label='File')
        self.menubar.add_cascade(menu=self.action_menu, label='Action')

        self.entry = tk.Entry(self.root, font=('Arial', 16), bg='#5D6D7E', fg='#BDC3C7')
        self.entry.pack(padx=10, pady=10)
        self.entry.bind('<KeyPress>', self.shortcut)

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.button = tk.Button(self.frame, text='Download', font=('Arial', 18), command=self.download, bg='#0E6655',
                                fg='#BDC3C7')
        self.button.grid(row=0, column=0)

        self.search_btn = tk.Button(self.frame, text='Search', font=('Arial', 18), command=self.search_video,
                                    bg='#0E6655',
                                    fg='#BDC3C7')
        self.search_btn.grid(row=0, column=1)

        self.search_with_mic_btn = tk.Button(self.frame, text='Search with mic', font=('Arial', 18),
                                             command=self.search_video_with_mic, bg='#0E6655',
                                             fg='#BDC3C7')
        self.search_with_mic_btn.grid(row=0, column=2)

        self.clear_btn = tk.Button(self.root, text='Clear', font=('Arial', 18), command=self.clear,
                                   bg='#0E6655', fg='#BDC3C7')
        self.clear_btn.pack(padx=10, pady=10)

        self.root.config(menu=self.menubar)
        self.root.quit()
        self.root.mainloop()

    def download(self):
        try:
            link = 'https://www.youtube.com/results?search_query=' + self.entry.get()
            yt = YouTube(link)

            print('Title: ', yt.title)
            print('View: ', yt.views)
            length = yt.length
            length /= 60
            print('Length: {0:.2f}'.format(length))
            message = 'Your Video Downloading...'
            self.speak(message)
            messagebox.showinfo(title='Message', message='Your video downloading...')

            yd = yt.streams.get_highest_resolution()
            yd.download('C:/Users/isint/OneDrive/Masaüstü/Youtube')

        except:
            message = 'Wrong URL!!'
            self.speak(message)

    def clear(self):
        self.entry.delete(0, 'end')
        message = 'Clearing'
        self.speak(message)

    def shortcut(self, event):
        if event.state == 12 and event.keysym == 'Return':
            self.download()

    def close_window(self):
        self.root.quit()

    def search_video(self):
        query = self.entry.get()
        search_query = query.split()

        url = "http://www.youtube.com/results?search_query="

        for word in search_query:
            url += word + "+"

        message = 'Looking in Youtube.'
        self.speak(message)
        time.sleep(0.5)
        webbrowser.open_new(url[:-1])

    def search_video_with_mic(self):
        query = self.record_sound()
        search_query = query.split()

        url = "http://www.youtube.com/results?search_query="

        for word in search_query:
            url += word + "+"

        message = 'Looking in Youtube.'
        self.speak(message)
        time.sleep(0.5)
        webbrowser.open_new(url[:-1])

App()
