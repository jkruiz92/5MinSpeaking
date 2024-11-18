import os
import pyaudio
import wave


class app():
    def __init__(self):
        """
        This class configure the voice audio source and the languages for input-output conversion.
        """
        self.input = ""
        self.FORMAT = pyaudio.paInt16       # Formato de audio
        self.HANNELS = 1                    # Número de canales (1 para mono, 2 para estéreo)
        self.RATE = 44100                   # Frecuencia de muestreo (Hz)
        self.CHUNK = 1024                   # Tamaño de cada bloque de datos
        self.OUTPUT_FILE = "recording.wav"  # Nombre del archivo de salida
        self.language_in = ""
        self.language_out = ""

    def in_source_connect(self):
        """
        Function that search and connect to the selected audio source.
        """
        pass

    def start_recording(self, source):
        """
        This function start the record of audio input
        """
        pass

    def stop_recording(self, source):
        """
        This function stops the audio input record.
        """
        pass

    def speech_to_text(self, audio_file):
        """
        This functions transcribes the audio file to text.
        """
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


