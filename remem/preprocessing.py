import torch
import speech_recognition as sr
import pyaudio
import wave
from typing import List, Tuple

def transcribe_audio(audio_file: str) -> str:
    """
    can raise if the transcription breaks
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    """
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)  # read the entire audio file
    return r.recognize_sphinx(audio)

def record_audio(seconds: int, filename: str):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording..')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for eck in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def speaker_activity_detection(audio_file: str) -> List[Tuple[float, float]]:
    "return list with start and end of speaker segments in seconds"
    pipeline = torch.hub.load('pyannote/pyannote-audio', 'sad', pipeline=True)
    input_file = {'uri': 'input_file', 'audio': audio_file}
    sad_output = pipeline(audio_file)
    return [(s.start, s.end) for s in sad_output.get_timeline()]



