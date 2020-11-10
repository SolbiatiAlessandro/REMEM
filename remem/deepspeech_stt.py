import numpy as np
from deepspeech import Model, version
import wave
from timeit import default_timer as timer


MODEL_PATH = "./models/deepspeech-0.9.1-models.pbmm"
SCORER_PATH = "./models/deepspeech-0.9.1-models.scorer"

def predict(audio_file):
    """predict speech-to-text from audio_file .wav sampled at 16kHz"""
    print('Loading model from file {}'.format(MODEL_PATH))
    model_load_start = timer()
    # sphinx-doc: python_ref_model_start
    ds = Model(MODEL_PATH)
    # sphinx-doc: python_ref_model_stop
    model_load_end = timer() - model_load_start
    print('Loaded model in {:.3}s.'.format(model_load_end))

    desired_sample_rate = ds.sampleRate()

    if SCORER_PATH:
        print('Loading scorer from files {}'.format(SCORER_PATH))
        scorer_load_start = timer()
        ds.enableExternalScorer(SCORER_PATH)
        scorer_load_end = timer() - scorer_load_start
        print('Loaded scorer in {:.3}s.'.format(scorer_load_end))

        """
        if args.lm_alpha and args.lm_beta:
            ds.setScorerAlphaBeta(args.lm_alpha, args.lm_beta)
        """

    """
    if args.hot_words:
        print('Adding hot-words')
        for word_boost in args.hot_words.split(','):
            word,boost = word_boost.split(':')
            ds.addHotWord(word,float(boost))
    """

    fin = wave.open(audio_file, 'rb')
    fs_orig = fin.getframerate()
    if fs_orig != desired_sample_rate:
        print("YOU NEED TO HAVE SAMPLE RATE OF 16kHZ in the input file!!!!")
        print('Warning: original sample rate ({}) is different than {}hz. Resampling might produce erratic speech recognition.'.format(fs_orig, desired_sample_rate))
        fs_new, audio = convert_samplerate(audio_file, desired_sample_rate)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1/fs_orig)
    fin.close()

    print('Running inference.')
    inference_start = timer()

    """
    # sphinx-doc: python_ref_inference_start
    if args.extended:
        print(metadata_to_string(ds.sttWithMetadata(audio, 1).transcripts[0]))
    elif args.json:
        print(metadata_json_output(ds.sttWithMetadata(audio, args.candidate_transcripts)))
    else:
    """
    predictions = ds.stt(audio)
    print(predictions)
    # sphinx-doc: python_ref_inference_stop
    inference_end = timer() - inference_start
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))
    return predictions
