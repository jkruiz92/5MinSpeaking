import os
import time
import keyboard
import pyaudio
import wave
import librosa
import numpy as np
import soundfile as sf
from vosk import Model, KaldiRecognizer


class app():
    def __init__(self):
        """
        This class configure the voice audio source and the languages for input-output conversion.
        """
        self.input = ""
        self.FORMAT = pyaudio.paInt16       # Formato de audioS
        self.CHANNELS = 1                    # Número de canales (1 para mono, 2 para estéreo)
        self.RATE = 44100                   # Frecuencia de muestreo (Hz)
        self.CHUNK = 1024                   # Tamaño de cada bloque de datos
        self.OUTPUT_DIR = os. getcwd()+"/records/"
        self.OUTPUT_FILE = "recording.wav"  # Nombre del archivo de salida
        self.language_in = ""
        self.language_out = ""
        self.file =""

    def record(self):
        """
        Function that search and connect to the selected audio source.
        """
        self.audio = pyaudio.PyAudio()

        # Abrir un flujo de entrada
        self.stream = self.audio.open(format=self.FORMAT, 
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)
        
        print("Input channel connected.\nPress 'A' key to start recording.")

        self.frames = []

        while not keyboard.is_pressed('a'):
            pass

        print("Recording...\nPress 'S' key when speech is finished.s")

        while not keyboard.is_pressed('s'):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

        print("Stopping...")

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("Record stopped.")

        # Guardar los datos en un archivo .wav
        print("Saving file...")

        try:
            os.mkdir(self.OUTPUT_DIR)
        except:
            pass

        self.file = self.OUTPUT_DIR+self.OUTPUT_FILE
        print(self.file)
        with wave.open(self.file, 'wb') as wf:
            wf.setnchannels((self.CHANNELS))
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
        print(f"File saved as {self.OUTPUT_FILE}")

        return self.file, len(self.frames)

    def speech_to_text(self,file, frames):
        """
        This functions transcribes the audio file to text.as
        """
        print(file)

        #normalize audio
        audio, sr = librosa.load(file, sr=None)
        normalized_audio = audio / np.max(np.abs(audio))
        n_file = self.OUTPUT_DIR + 'normalized_audio.wav'
        sf.write(n_file, normalized_audio, sr)

        #STT
        model = Model("model_path")
        recognizer = KaldiRecognizer(model, 44100)

        wf = wave.open(n_file, "rb")
        while True:
            data = wf.readframes(frames)
            if len(data) == 0:
                break
        if recognizer.AcceptWaveform(data):
            print(recognizer.Result())

        pass
    
    def analyse_speech(self, text):
        """
        This function analyse the speech after being converted to text.
        Can fix errors and rate the quality of the speech.
        """
        pass

    def translate_text(self,in_lang, out_lang):
        """
        This function translate the text from input language to output language
        """
        pass

    def text_to_speech(self, text):
        """
        This function speak outloud the text string enter as a parameter.
        """
        pass

    #main function

if __name__ == "__main__":
    file, frames = app().record()
    app().speech_to_text(file, frames)
