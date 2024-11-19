import os
import time
import pyaudio
import wave


class app():
    def __init__(self):
        """
        This class configure the voice audio source and the languages for input-output conversion.
        """
        self.input = ""
        self.FORMAT = pyaudio.paInt16       # Formato de audio
        self.CHANNELS = 1                    # Número de canales (1 para mono, 2 para estéreo)
        self.RATE = 44100                   # Frecuencia de muestreo (Hz)
        self.CHUNK = 1024                   # Tamaño de cada bloque de datos
        self.OUTPUT_FILE = "recording.wav"  # Nombre del archivo de salida
        self.language_in = ""
        self.language_out = ""

    def in_source_connect(self):
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
        
        print("Input channel connected.")

        

        self.frames = []

        print("Recording...")


        for _ in range(0, int(self.RATE / self.CHUNK * 5)):
            print(int(self.RATE / self.CHUNK * 3))
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

        print("Stopping...")

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("Record stopped.")

        # Guardar los datos en un archivo .wav
        print("Saving file...")

        with wave.open(self.OUTPUT_FILE, 'wb') as wf:
            wf.setnchannels((self.CHANNELS))
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
        print(f"File saved as {self.OUTPUT_FILE}")
        pass

    def start_recording(self):
        """
        This function start the record of audio input
        """

        print("Recording...")

        self.frames = []

        for _ in range(0, int(self.RATE / self.CHUNK * 3)):
            print (int(self.RATE / self.CHUNK * 3))
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

        pass

    def stop_recording(self):
        """
        This function stops the audio input record.
        """

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("Record stopped.")

        # Guardar los datos en un archivo .wav
        with wave.open(self.OUTPUT_FILE, 'wb') as wf:
            wf.setnchannels((self.CHANNELS))
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate((self.RATE))
            wf.writeframes(b''.join(self.frames))
        print(f"Archivo guardado como {self.OUTPUT_FILE}")
              
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

    #main function

if __name__ == "__main__":
    app().in_source_connect()
    #app().start_recording()
    #app().stop_recording()