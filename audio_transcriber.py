# Import the subprocess and json modules
import subprocess, json

# Import the vosk.Model and vosk.KaldiRecognizer classes
from vosk import Model, KaldiRecognizer

# Deifne constants for size of data chunks and sample rate for audio data
CHUNK_SIZE = 4000
SAMPLE_RATE = 16000.0


class Transcriber:
    """ The Transcriber class transcribes audio files using Vosk"""
    
    def __init__(self, model_path):
        """ 
        __init__() initializes the Transcriber class
        
        :param model_path: relative path to Vosk language model
        """

        # Create an instance of Model using inputted model_path
        self.model = Model(model_path)
    
    def arrange(self, data):
        """
        arrange() structures and organizes the transcription results 

        :param data: JSON data string
        :return: a dictionary that holds the extracted text
        """

        # Parse the JSON data and convert to Python dictionary
        data = json.loads(data)

        # Returns the desired dicitonary format
        return {
            "text" : data["text"]
        }
    
    def resample_ffmpeg(self, infile):
        """
        resample_ffmpeg() resamples the provided audio file using FFmpeg

        :param infile: relative path to the inputted audio file
        :return: the output of the FFmpeg subprocess (stdout)
        """

        # Construct an FFmpeg command as a list of command-line args
        ffmpeg = [
            "ffmpeg",
            "-nostdin",
            "-loglevel","quiet",
            "-i", infile,
            "-ar", str(SAMPLE_RATE),
            "-ac", "1",
            "-f", "s16le",
            "-",
        ]

        # Return the stdout of the subprocess
        return subprocess.Popen(ffmpeg, stdout=subprocess.PIPE)

    def transcribe(self, filename):
        """
        transcribe() performs the audio transcription

        :param filename: relative path to the inputted audio
        :return: a dictionary containing the final transcription results
        """

        # Initailize an instance of KaldiRecognizer 
        rec = KaldiRecognizer(self.model, SAMPLE_RATE)
        #rec.SetWords(True)

        # Create an empty list to store the transcription results
        result = []

        # Try to open the audio file using FFmpeg to read th audio stream
        try: 
            stream = self.resample_ffmpeg(filename);
        except FileNotFoundError as e:
            print(e, "Missing FFMPEG, please install and try again")
            return
        
        # Loop to read the audio data from FFmpeg output stream
        while True:
            data = stream.stdout.read(CHUNK_SIZE)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result.append(self.arrange(rec.Result()))     
        result.append(self.arrange(rec.FinalResult()))

        # Return the final transcription results
        return {
            "transcription" : result
        }