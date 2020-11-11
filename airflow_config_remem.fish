function airflow_config_remem
  set -x -g AIRFLOW__CORE__DAGS_FOLDER /Users/lessandro/Coding/AI/REMEM/remem
  set -x -g OBJC_DISABLE_INITIALIZE_FORK_SAFETY YES
  set -x -g AIRFLOW__SCHEDULER__STATSD_ON True
  set -x -g AIRFLOW__SCHEDULER__STATSD_HOST 127.0.0.1
  set -x -g AIRFLOW__SCHEDULER__STATSD_PORT 8125
  set -x -g AIRFLOW__SCHEDULER__STATSD_PREFIX airflow
end
