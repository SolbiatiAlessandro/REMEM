# REMEM
Replicating the "Remem" device from the Science Fiction novel ["The Truth of Fact, the Truth of Feeling" by Ted Chiang](https://en.wikipedia.org/wiki/The_Truth_of_Fact,_the_Truth_of_Feeling).

```
"Remem", a form of lifelogging whose advanced search algorithms 
effectively grant its users eidetic memory of everything that
ever happened to them, and the ability to perfectly and objectively 
share those memories.
```

A screenshot from the Grafana of REMEM

![](https://raw.githubusercontent.com/SolbiatiAlessandro/REMEM/main/Screenshot%202020-11-11%20at%2023.20.17.png)


## Preprocessing 

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


## Infra

### Airflow Setup

Using airflow to manage the data pipelines. Setup locally with postgres following this guide https://medium.com/@Newt_Tan/apache-airflow-installation-based-on-postgresql-database-26549b154d8

On OSX the config file for postgres is at `/usr/local/var/postgres/`

There is a bunch of airflow config, I have a fish function to be copied and run
```
cp airflow_config_remem.fish ~/.config/fish/functions/
airflow_config_remem
```

### Airflow entrypoint

Once airflow is set up correctly run it with

```
set -x OBJC_DISABLE_INITIALIZE_FORK_SAFETY YES (https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr)
set -x AIRFLOW__CORE__DAGS_FOLDER /Users/lessandro/Coding/AI/REMEM/remem
airflow webserver -p 8080
(in another tab) airflow scheduler
```

Had some bugs install airflowws run this
``` 
# https://github.com/apache/airflow/issues/11965#issuecomment-719488558
pip install apache-airflow==1.10.12 \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"
```

### Monitoring
Given that this thing is resources intensive we set up some monitoring infra. This is the docker image https://github.com/hopsoft/docker-graphite-statsd#quick-start

Run the docker with the command

```
docker run -d\
      --name graphite\
      --restart=always\
      -p 80:80\
      -p 81:81\
      -p 2003-2004:2003-2004\
      -p 2023-2024:2023-2024\
      -p 8125:8125/udp\
      -p 8126:8126\
      hopsoft/graphite-statsd
```

And then go to `http://localhost:81/render?from=-10mins&until=now&target=stats.airflow.schedulerjob_start` to check that the data are being received correclty

I set up a grafana dashboard at http://localhost/dashboard/db/remem-monitoring

We monitor memory allocation in the dashboard using tracemalloc and statsd.
For some reason if I increament of `1938639 bytes` on grafana end I get `63100`
