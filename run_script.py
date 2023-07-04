# Import vosk_transcript,sys, os, and json modules
import audio_transcriber
import os, sys, json

# List of valid input and otput file extensions
valid_in_ext = [".mp3", ".mp4", ".wav"]
valid_out_ext = [".json"]

# Ensure that user provides correct number of arguments
if len(sys.argv) < 3:
    print("Provide an audio file (argv[1]) and JSON output filename (argv[2])")
    sys.exit(1)

# Get the filename and output plus their extensions
filename = sys.argv[1]
in_ext = os.path.splitext(filename)[1]
output = sys.argv[2]
out_ext = os.path.splitext(output)[1]

# Check if provided file extension is valid
if (in_ext.lower() not in valid_in_ext) or (out_ext.lower() not in valid_out_ext):
    print("Valid audio file extensions: mp3, mp4, wav")
    print("Valid output file extensions: json")
    sys.exit(1)

# Define Vosk Speech Recognition model
model_path = "vosk-model-small-en-us-0.15"

# Create an instance of the Transcriber class that passes the model_path
transcriber = audio_transcriber.Transcriber(model_path)
transcription = transcriber.transcribe(filename)

# The contents of transcription are written into json_file
with open(output, "w") as json_file:
    json.dump(transcription, json_file, indent=4)
