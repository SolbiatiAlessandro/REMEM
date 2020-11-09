# REMEM
Replicating the "Remem" device from the SF novel ["The Truth of Fact, the Truth of Feeling" by Ted Chiang](https://en.wikipedia.org/wiki/The_Truth_of_Fact,_the_Truth_of_Feeling).


## MacOSX

### Preprocessing 

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

To install pocketsphinx I had some error fixed with this https://github.com/bambocher/pocketsphinx-python/issues/28#issuecomment-334493324


### Infra

Using airflow to manage the data pipelines. Setup locally with postgres following this guide https://medium.com/@Newt_Tan/apache-airflow-installation-based-on-postgresql-database-26549b154d8

On OSX the config file for postgres is at `/usr/local/var/postgres/`

Once airflow is set up correctly run it with

```
set -x OBJC_DISABLE_INITIALIZE_FORK_SAFETY YES (https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr)
set -x AIRFLOW__CORE__DAGS_FOLDER /Users/lessandro/Coding/AI/REMEM/remem
airflow webserver -p 8080
(in another tab) airflow scheduler
```

