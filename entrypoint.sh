#!/usr/bin/env bash


case "$1" in
  webserver)
    #airflow initdb
	#if [ "$AIRFLOW__CORE__EXECUTOR" = "LocalExecutor" ] || [ "$AIRFLOW__CORE__EXECUTOR" = "SequentialExecutor" ]; then
    #  airflow scheduler &
    #fi
	airflow db init &&
    exec airflow webserver
    ;;
  scheduler)
    # Give the webserver time to run initdb.
    sleep 10
    exec airflow "$@"
    ;;
  version)
    exec airflow "$@"
    ;;
  *)
    exec "$@"
    ;;
esac