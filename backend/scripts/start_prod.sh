#!/bin/bash
SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
ROOT_DIR="$SCRIPT_DIR/.."

# Go to root folder
cd $ROOT_DIR

echo "Waiting postgreSQL ${DISFACTORY_BACKEND_DEFAULT_DB_HOST}:${DISFACTORY_BACKEND_DEFAULT_DB_PORT}"
$ROOT_DIR/scripts/wait-for-it.sh ${DISFACTORY_BACKEND_DEFAULT_DB_HOST}:${DISFACTORY_BACKEND_DEFAULT_DB_PORT} -- bash -c "gunicorn -c gunicorn.conf.py gis_project.wsgi -b 0.0.0.0:8000"
