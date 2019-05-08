from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label 
from kivy.uix.button import Button 
from kivy.lang import Builder
from kivy.app import App 
from kivy.clock import Clock 
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch 
from pygame.locals import *


import time
import threading


class ScreenOne(Screen):
    last_text_input = ObjectProperty()
    ego = NumericProperty(0)
    word = StringProperty('')
    def submit_word(self):
        self.word = self.last_text_input.text
        print("Assign word: {}".format(self.word))
        self.save()
        self.word = ''
        print("Reset word: {}".format(self.word))
        self.load()
        print("Loaded word: {}".format(self.word))

    def save(self):
        with open("word.txt", "w") as fobj:
            fobj.write(str(self.word))

    def load(self):
        with open("word.txt") as fobj:
            for word in fobj:
                self.word = word.rstrip()


class ScreenTwo(Screen):
    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)
        
        # self.start_button = self.ids['start_button']
        # self.display_label = self.ids['display_label']



    def record(*arg):
        import pyaudio
        import wave
        import pygame, sys

        pygame.init()
        pygame.display.init()
        scr = pygame.display.set_mode((250,250))
        font = pygame.font.Font('freesansbold.ttf', 12) 
        text = font.render('Click anywhere to stop recording', True, (255, 255, 255), (0,0,0))
        textRect = text.get_rect()
        textRect.center = (250 // 2, 250 // 2)
        recording = True



        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        while True:
            
            scr.fill([0,0,0])
            scr.blit(text, textRect) 
            pygame.display.update()  
            if recording:
                data = stream.read(CHUNK)
                frames.append(data)

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and recording:
                    print("* done recording")

                    stream.stop_stream()
                    stream.close()
                    p.terminate()

                    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()
                    recording = False
        
                    pygame.quit()
                    return
                    
class ScreenThree(Screen):
    f=open("score.txt", "r")
    score= f.read()
                              


class Manager(ScreenManager):

    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    screen_three = ObjectProperty(None)


class GaideApp(App):

    def build(self):
        m = Manager(transition=NoTransition())
        return m
    


if __name__ == "__main__":
    GaideApp().run()
