winget install -e --id Python.Python.3.12
python -m pip install --upgrade pip

REM everything below here is to setup the docker container for the script so that the generated code can't do anything truly stupid
winget install Docker.DockerCLI
