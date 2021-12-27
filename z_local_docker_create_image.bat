
@echo off 
REM
REM https://docs.docker.com/engine/reference/commandline/build/
REM 
REM Build an image from a Dockerfile
REM
REM  docker build [OPTIONS] PATH | URL | -
REM
REM --tag , -t		Name and optionally a tag in the 'name:tag' format
REM
REM 
@echo on

set image=local_ssd_image
set container=ctn_local_ssd


docker build -t %image% .

docker rm --force %container%

docker run --name %container% -dp 80:80 %image% python -m flask run --host=0.0.0.0 --port=80

pause