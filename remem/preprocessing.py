import torch
import speech_recognition as sr
import pyaudio
import wave
from typing import List, Tuple
from db import add_transcript

AUDIO_FILES_FOLDER = 'static'
MAX_AUDIO_FILES = 3
AUDIO_LENGTH_SECONDS = 60

def transcribe_audio_operator(**kwargs):
    task_instance = kwargs['ti']
    activity_detected, filename = task_instance.xcom_pull(
            key=None,
            task_ids='speaker_activity_detection_operator')
    if not activity_detected:
        print("[transcribe_audio_operator] got no activity detected, not running ASR")
    else:
        transcription = transcribe_audio(filename)
        print("[transcribe_audio_operator] ASR results:")
        print(transcription)
        add_transcript(transcription, kwargs['ts_nodash'])

def transcribe_audio(audio_file: str) -> str:
    """
    can raise if the transcription breaks
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    """
    print("[transcribe_audio] running ASR")
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)  # read the entire audio file
    return r.recognize_sphinx(audio)

def delete_audio_operator(**kwargs):
    task_instance = kwargs['ti']
    filename = task_instance.xcom_pull(
            key=None,
            task_ids='record_audio_operator')
    if len(os.listdir(AUDIO_FILES_FOLDER)) > MAX_AUDIO_FILES:
        os.remove(filename)

def record_audio_operator(**kwargs):
    ts_nodash = kwargs['ts_nodash']
    seconds = AUDIO_LENGTH_SECONDS
    filename = AUDIO_FILES_FOLDER + "/record_" + ts_nodash + ".wav"
    record_audio(seconds, filename)
    return filename

def record_audio(seconds: int, filename: str):
    print('[record_audio]')
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

def speaker_activity_detection_operator(**kwargs):
    task_instance = kwargs['ti']
    filename = task_instance.xcom_pull(
            key=None,
            task_ids='record_audio_operator')
    activity_detected = speaker_activity_detection(filename)
    if activity_detected:
        print("[speaker_activity_detection_operator] activity detected for "+filename)
        for speech_region in activity:
            print(f'There is speech between t={speech_region[0]:.1f}s and t={speech_region[1]:.1f}s.')
    else:
        print("[speaker_activity_detection_operator] no activity detected for "+filename)
    return activity_detected, filename


def speaker_activity_detection(audio_file: str) -> List[Tuple[float, float]]:
    "return list with start and end of speaker segments in seconds"
    print("[speaker_activity_detection] running pipeline on "+audio_file)
    pipeline = torch.hub.load('pyannote/pyannote-audio', 'sad', pipeline=True)
    input_file = {'uri': 'input_file', 'audio': audio_file}
    sad_output = pipeline(input_file)
    activity_length = sum([sr.end - sr.start for sr in sad_output.get_timeline()]) 
    return activity_length > (AUDIO_LENGTH_SECONDS / 4)
