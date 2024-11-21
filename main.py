import os
import time
import keyboard
import pyaudio
import wave
import numpy as np
import soundfile as sf
import json
from vosk import Model, KaldiRecognizer


class app():
    def __init__(self):
        """
        This class configure the voice audio source and the languages for input-output conversion.
        """
        self.input = ""
        self.FORMAT = pyaudio.paInt16       # Formato de audioS
        self.CHANNELS = 1                    # Número de canales (1 para mono, 2 para estéreo)
        self.RATE = 16000                   # Frecuencia de muestreo (Hz)
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
        return self.file

    def normalize_audio(self,file):
        """
        This functions transcribes the audio file to text.

        """

        # load audio file
        audio_data, samplerate = sf.read(file)
    
        # Verify number of channels (mono, stereo)
        if len(audio_data.shape) > 1:
            # Normalize more rhan 1 channel
            max_val = np.max(np.abs(audio_data), axis=0)
            normalized_data = audio_data / max_val
        else:
            # Normalize mono audio
            max_val = np.max(np.abs(audio_data))
            normalized_data = audio_data / max_val

        # Save audio normalized
        output_file = file.replace("recording", "n_recording")
        sf.write(output_file, normalized_data, samplerate)
        print(f"Normalized file saved as {output_file}")
        return output_file

    def speech_to_text(self,file,model = "vosk-model-small-es-0.42" ):
        """
        Transcribe an audio file to text using Vosk.

        :param file_path: Path to the audio file (WAV format, mono, 16kHz recommended).
        :param model_path: Path to the Vosk model directory.
        :return: Transcription as a string.

        # Ensure you download a Vosk model (e.g., from https://alphacephei.com/vosk/models) and
        unzip it into /vosk_models directory
        """
        # Load the Vosk model

        model_path = (os.getcwd() + "/vosk_models/" + model)
        print(model_path)
        
        model = Model(model_path)

        # Open the audio file
        with wave.open(file, "rb") as wf:
            # Check if the audio file format is compatible
            if wf.getnchannels() != 1:
                raise ValueError("Audio file must be mono.")
            if wf.getsampwidth() != 2:
                raise ValueError("Audio file must have 16-bit samples.")
            if wf.getframerate() not in [16000, 8000]:
                raise ValueError("Audio file must have a sample rate of 8kHz or 16kHz.")

            # Initialize the recognizer
            recognizer = KaldiRecognizer(model, wf.getframerate())

            # Transcribe audio
            transcription = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    transcription.append(result.get("text", ""))

            # Get the final result
            final_result = json.loads(recognizer.FinalResult())
            transcription.append(final_result.get("text", ""))

        # Return the complete transcription
        return " ".join(transcription)
    
    
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
    file = app().record()
    n_file = app().normalize_audio(file)
    text = app().speech_to_text(n_file)
    print(text)
