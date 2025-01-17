# Pipeline MVP

MVP project for Airflow-based scheduling of data pipeline processing for MapAction. This repository is used for local development and for running in GCP.

# Background and History

This project is one is a series of projects outlines in our ["Moonshoot" initative](https://mapaction.org/mapactions-moonshot-origins-and-ambitions). 
This seeks to automate many of the tasks in pre-emergency data preparedness and the initial tasks in map production.

In 2020 we ran two projects exploring how we could automate the acquisition of data.

First was the "Slow Data Scramble". For this we focused on just one country - Yemen. We identified 22 commonly required data artefacts. For each artefact and data source combination, we defined the acquisition and transformation necessary.

* There is a [blog post describing this project](https://mapaction.org/moonshot-part-2-the-slow-data-scramble)
* The code is here https://github.com/mapaction/datasources-etl

The second was our "Pipeline MVP" project. This took many of the concepts from the Slow Data Scramble. This generalised to multiple countries 13 countries. Additionally, it migrated the code so that it could be hosted in Google Cloud Platform using Airflow.

* This code is here https://github.com/mapaction/pipeline_mvp


## Structure

`/dags`

Folder with the DAG scripts, every DAG instance in the global namespace will be available inside Airflow.

`/plugins`

Folder with the `pipeline_plugin` that contains the custom operators and the domain logic.

`/scripts`

Scripts to automate setting up the environment for local development.

`/data`

Empty folder that is mounted in the local Docker container so that any data generated by the dags is also available in the local environment.

`/requirements.txt`

Python packages required for development in your IDE.

`/requirements-airflow.txt`

Python packages that need to be available in the Airflow server. These significantly increase startup time of your local Airflow server.

## Local development

The instructions below have been tested for setting up a local development environment on Ubuntu 20.04.
There are seperate instructions on developing on Windows Subsystem for Linux (WSL) https://github.com/mapaction/pipeline_mvp/wiki/Docker-on-Windows.

### Requirements

Docker is a dependency for running a local version of Airflow.

### Initial setup

To create a virtual environment for local development, run the following from the root folder:

`source ./scripts/setup_environment.sh`

When you add new dependencies, rerun this command to install the new dependencies in your virtual environment.

### Development

To start the Airflow server, run the following from the root folder:

`sh ./scripts/start_airflow.sh`

The Airflow server runs in a Docker container, which has the `/dags`, `/plugins` and `/data` folders mounted in there, together with the `requirements-airflow.txt` file. When starting the container, these requirements are installed. The `/data` folder is accessible from `/opt/data` folder inside the Airflow server/worker. The `/dags` folder contains all the dags and is automatically synchronized, while the `/plugins` folder contains the plugins including all the processing logic. This is also automatically synchronized but still a bit shaky, so if things are not working, restart the Docker container.

### Airflow symbolic links

Because of the way the Airflow plugin system works, the code in the DAGs refers to the plugins in a different location. To help the IDE for development, we can use symlinks to symbolically link the files in the `plugins` folder to the Airflow package so that things like autocomplete will work. Run the `airflow_symbolic_links.sh` script from the root to set things up.

## CI / CD

For Google Cloud Composer, a CI/CD pipeline is set up using Google Cloud Build. When a new push is made to master, the `cloudbuild.yaml` file is used for the workflow. The following steps are executed:

- The commit hash is used as version
- The KubernetesPodOperator image is built and labeled with this version
- The `dags` folder is synchronized to Cloud Storage, which Cloud Composer synchronizes with
- The `plugins` folder is synchronized to Cloud Storage, which Cloud Composer synchronizes with
- The commit hash is set as variable in Cloud Composer so that the Operators use the new Docker image
