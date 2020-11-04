# REMEM
Replicating the "Remem" device from the SF novel ["The Truth of Fact, the Truth of Feeling" by Ted Chiang](https://en.wikipedia.org/wiki/The_Truth_of_Fact,_the_Truth_of_Feeling).


## MacOSX

```
brew install portaudio
pip install -r requirements
git clone https://github.com/pyannote/pyannote-audio.git
cd pyannote-audio
pip install .
```

For some reasons pyannote breaks with dataclasses from python<3.7 so you need to run
```
pip uninstall dataclasses
```