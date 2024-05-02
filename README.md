ǚ# Fyle Backend Challenge

## Table of Contents:

- [Technology Stack](#technology-stack)
- [Installation](#installation)
  1. [Docker Containers](#docker-containers) 
        - [Docker Installation](#docker-installation)
        - [Build and run commands](#build-and-run-commands)
  2. [Manual Installtion](#manual-installation) 
- [Screenshots](#screenshots)

<hr> 

## Technology Stack

<div align="center"> 

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0.1-blue.svg)](https://flask.palletsprojects.com/en/3.0.x/)

[![SQLite](https://img.shields.io/badge/SQLlite-3.0-blue.svg)](https://www.sqlite.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10.11-blue.svg)](https://www.docker.com/)
[![JSON](https://img.shields.io/badge/JSON-Data-blue.svg)](https://www.json.org/)

</div> 
<hr>

## Installation

### Docker Containers

<img width="1470" alt="Docker" src="https://github.com/neellad3110/FlightVoyage/assets/92388308/8ec1c274-e431-436a-9324-2b263e4fb950">

#### What is Docker ?

[Docker](https://www.docker.com/get-started/) is a software platform that allows you to build, test, and deploy applications quickly. Docker packages software into standardized units called containers that have everything the software needs to run including libraries, system tools, code, and runtime. Using Docker, you can quickly deploy and scale applications into any environment and know your code will run.

#### How does docker works ?

Docker works by providing a standard way to run your code. Docker is an operating system for containers. Similar to how a virtual machine virtualizes (removes the need to directly manage) server hardware, containers virtualize the operating system of a server. Docker is installed on each server and provides simple commands you can use to build, start, or stop containers.

#### Docker Installation
> [!TIP]
> Check out the [docker documentation](https://docs.docker.com/desktop/install/windows-install/) to set up in your machine.  

#### Build and run commands.

1. Open a terminal in your project directory and run:

```
docker-compose build
```
<img width="1629" alt="Screenshot 2024-05-02 at 21 09 00" src="https://github.com/neellad3110/fyle-backend-task/assets/92388308/41cd11f9-cb13-4403-9b9f-bc35183e65e3"><br>


>The `docker-compose build` is a command used to build Docker images for services defined in a `docker-compose.yml` file. It reads the Dockerfile in each service's build context and creates Docker images accordingly. This command is useful for preparing Docker images before starting containers with docker-compose up.

<br>

2. Now run:

```
docker-compose up
```
<img width="1253" alt="Screenshot 2024-05-02 at 21 10 13" src="https://github.com/neellad3110/fyle-backend-task/assets/92388308/f0063eac-b7a6-4a23-ac25-00c07dd2e424">
<br>

>The `docker-compose up` command is used to start services defined in your` docker-compose.yml` file. It reads the configuration from the `docker-compose.yml` file and creates and starts containers for all services defined within it. If the containers already exist, it will attempt to start them. If the images for the services have not been built yet, it will build them first before starting the containers.


>[!NOTE]
>To get the IP address and port number of the container.

Open a new terminal and run :

```
docker ps
```
<img width="1625" alt="Screenshot 2024-05-02 at 21 38 14" src="https://github.com/neellad3110/fyle-backend-task/assets/92388308/addc1e15-d78b-4a51-865a-c5fb1a2c04db">


<br>

As per above information
<br>

> At [0.0.0.0:7755](http://0.0.0.0:7755/)  : Our Flask Web application is accessible.
<hr>
<br>
<img width="1212" alt="Screenshot 2024-05-02 at 21 50 14" src="https://github.com/neellad3110/fyle-backend-task/assets/92388308/88dfc923-e78d-44ab-abfc-e9340a69bf98">


<hr>
<br>

## Manual Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
### Reset DB

```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```
### Start Server

```
bash run.sh
```
### Run Tests

```
pytest -vvv -s tests/

#  for test coverage report

pytest --cov
coverage html 
open htmlcov/index.html
```

### Screenshots

#### 1. Pytest test cases
<img width="1583" alt="Screenshot 2024-05-02 at 19 11 15" src="https://github.com/neellad3110/fyle-backend-task/assets/92388308/8813b5b3-ae40-4a7d-9b51-3c78b3a55d67">

<br>

#### 2. Pytest coverage
<img width="1582" alt="Screenshot 2024-05-02 at 20 32 50" src="https://github.com/neellad3110/fyle-backend-task/assets/92388308/77003a49-04ad-455e-9489-99f5cb33723a">

<br>

