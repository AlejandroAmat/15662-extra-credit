@echo off

set ENV_NAME=transforms
set PYTHON_VERSION=3.11

call conda create -n %ENV_NAME% python=%PYTHON_VERSION% -y

call conda activate %ENV_NAME%

call pip install pygame