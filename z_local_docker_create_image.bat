
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

docker build -t local_ssd_image .

pause